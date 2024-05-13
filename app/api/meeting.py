from datetime import datetime

from fastapi import APIRouter, Body, Path, Response

from app.constants import Error
from app.data import common as common_data
from app.database.db import SessionLocal, redis_db
from app.database.db_models import IsCaptured, Meeting, User
from app.depends import AuthedUser
from app.models.request import CheckRequest, MeetingAddRequest, MeetingApplyRequest
from app.models.response import (
    CheckResponse,
    CreateCheckResponse,
    UserMeetingResponse,
    UserMeetResponse,
)
from app.models.schema import CheckInfo, UserMeetInfo, UserMeetingInfo
from app.service.status import return_response, return_status

meetRouter = APIRouter(
    prefix="/meeting",
    tags=["meeting"],
)


@meetRouter.post("/add", dependencies=[AuthedUser(admin=True)])
async def meeting_add(response: Response, *, meeting_body: MeetingAddRequest = Body()):
    """添加会议室"""
    room = Meeting(
        name=meeting_body.name,
        address=meeting_body.address,
        facility=",".join(meeting_body.facilities),
    )
    common_data.add(room)
    return return_status(Error.NoError, response)


@meetRouter.post("/change", dependencies=[AuthedUser(admin=True)])
async def meeting_change(
    response: Response, *, meeting_body: MeetingAddRequest = Body()
):
    """修改会议室"""
    with SessionLocal() as sess:
        room = sess.query(Meeting).filter_by(meetingId=meeting_body.id).first()
    if room is None:
        return return_status(Error.MeetingNotExist, response)
    room.name = meeting_body.name
    room.address = meeting_body.address
    room.facility = ",".join(meeting_body.facilities)
    common_data.update(room)
    return return_status(Error.NoError, response)


@meetRouter.post("/delete/{{meetId}}", dependencies=[AuthedUser(admin=True)])
async def meeting_delete(response: Response, *, meetId: int = Path()):
    """删除会议室"""
    with SessionLocal() as sess:
        room = sess.query(Meeting).filter_by(meetingId=meetId).first()
    if room is None:
        return return_status(Error.MeetingNotExist, response)
    common_data.remove_single(room)
    return return_status(Error.NoError, response)


@meetRouter.get("/list", dependencies=[AuthedUser(admin=False)])
async def meeting_list(
    response: Response,
):
    """获取会议室列表"""
    with SessionLocal() as sess:
        rooms = sess.query(Meeting).all()
    return rooms


@meetRouter.post("/check", dependencies=[AuthedUser(admin=True)])
async def meeting_check(response: Response, *, CheckBody: CheckRequest = Body()):
    """审核会议室申请"""
    with SessionLocal() as sess:
        check = (
            sess.query(IsCaptured).filter_by(CapturedId=CheckBody.CapturedId).first()
        )
        if check is None:
            return return_status(Error.CheckNotExist, response)
        room = sess.query(Meeting).filter_by(meetingId=check.meetingId).first()
        if room is None:
            return return_status(Error.MeetingNotExist, response)

    check.isPassed = CheckBody.isCheck
    check.reason = CheckBody.reason
    common_data.update(check)
    return return_status(Error.NoError, response)


@meetRouter.get(
    "/checklist", response_model=CheckResponse, dependencies=[AuthedUser(admin=True)]
)
async def meeting_checklist(response: Response):
    """获取审核列表"""
    checkList = []
    with SessionLocal() as sess:
        checks = (
            sess.query(IsCaptured)
            .join(User, User.userId == IsCaptured.userId)
            .join(Meeting, Meeting.meetingId == IsCaptured.meetingId)
            .all()
        )
    if checks is None:
        return return_status(Error.CheckNotExist, response)
    for check in checks:
        check1 = CheckInfo(
            username=check.username,
            meetingName=check.name,
            meetingStartTime=check.StartTime,
            meetingEndTime=check.EndTime,
            meetingAddress=check.address,
            checkReason=check.reason,
            isPassed=check.isPass,
            number=check.number,
        )
        checkList.append(check1)

    return return_response(
        CheckResponse(Checklist=checkList, status=Error.NoError), response
    )


""""ai ai ai"""


@meetRouter.post("/apply/{meetId}")
async def apply_meeting(
    response: Response,
    meetId: int = Path(..., title="会议室ID"),
    request: MeetingApplyRequest = Body(),
    user: User = AuthedUser(admin=False),
):
    """预约会议"""
    # 查看会议室是否存在
    with SessionLocal() as sess:
        room = sess.query(Meeting).filter_by(meetingId=meetId).first()
    if room is None:
        return return_status(Error.MeetingNotExist, response)
    # 确认该会议室在该时间段是否被预约
    with SessionLocal() as sess:
        is_replied = (
            sess.query(IsCaptured)
            .filter_by(meetingId=meetId)
            .filter(IsCaptured.StartTime < request.EndTime)
            .filter(IsCaptured.EndTime > request.StartTime)
            .all()
        )
    if not is_replied:
        return return_status(Error.MeetingRoomIsCaptured, response)
    # 添加预约记录
    captured = IsCaptured(
        userId=user.userId,
        meetingId=meetId,
        StartTime=request.StartTime,
        EndTime=request.EndTime,
        number=request.number,
        reason=request.summary,
    )
    captured = common_data.add(captured)
    if captured is None:
        return return_status(Error.MeetingRoomIsCaptured, response)
    # redis记录参与会议的人名
    try:
        redis_db.sadd(f"meeting:{IsCaptured.CapturedId}", user.username)
    except Exception:
        return return_status(Error.RedisError, response)
    # 返回captureId
    return return_response(
        CreateCheckResponse(CheckId=captured.CapturedId, status=Error.NoError), response
    )


@meetRouter.get("/{meetid}", dependencies=[AuthedUser(admin=False)])
async def meeting_info(response: Response, *, meetingId: int = Path()):
    """获取会议室信息"""
    with SessionLocal() as sess:
        room = sess.query(Meeting).filter_by(meetingId=meetingId).first()
    if room is None:
        return return_status(Error.MeetingNotExist, response)
    return room


@meetRouter.get(
    "/meet_list",
    response_model=UserMeetResponse,
    dependencies=[AuthedUser(admin=False)],
)
async def meet_list(response: Response):
    """获取会议室列表"""
    m_li = []

    # 获取当前所有会议室
    with SessionLocal() as sess:
        rooms = sess.query(Meeting).all()
    for room in rooms:
        # 判断当前时间
        with SessionLocal() as sess:
            meet_status = (
                sess.query(IsCaptured)
                .filter_by(meetingId=room.meetingId)
                .filter(IsCaptured.StartTime < datetime.now())
                .filter(IsCaptured.EndTime > datetime.now())
                .filter(IsCaptured.isPass == 1)
                .all()
            )
        is_ok = True
        if meet_status is not []:
            is_ok = False
        m_li.append(
            UserMeetInfo(
                meetingId=room.meetingId,
                name=room.name,
                isCaptured=is_ok,
            )
        )
    return return_response(
        UserMeetResponse(MeetList=m_li, status=Error.NoError), response
    )


@meetRouter.get("/join/{IsCapturedId}")
async def join_meeting(
    response: Response,
    IsCapturedId: int = Path(..., title="预约ID"),
    user: User = AuthedUser(admin=False),
):
    """加入会议"""
    # 获取预约
    with SessionLocal() as sess:
        captured = sess.query(IsCaptured).filter_by(CapturedId=IsCapturedId).first()
    if captured is None:
        return return_status(Error.MeetingNotExist, response)

    if captured.isPass == 0:
        return return_status(Error.MeetingIsNotPassed, response)

    # 判断是否在会议时间内
    if datetime.now() >= captured.StartTime:
        return return_status(Error.MeetingIsStarted, response)
    # redis记录参与会议的人名
    try:
        redis_db.sadd(f"meeting:{IsCaptured.CapturedId}", user.username)
    except Exception:
        return return_status(Error.RedisError, response)


@meetRouter.get("/me/meet", response_model=UserMeetingResponse)
async def meetings_info(response: Response, *, user: User = AuthedUser(admin=False)):
    """获取该会议信息"""
    with SessionLocal() as sess:
        captures = (
            sess.query(IsCaptured)
            .filter_by(userId=user.userId)
            .filter_by(isPass=1)
            .all()
        )
    if captures is []:
        return return_status(Error.RecordNotFound, response)
    meet_list = []
    for capture in captures:
        with SessionLocal() as sess:
            room = sess.query(Meeting).filter_by(meetingId=capture.meetingId).first()
        meet_list.append(
            UserMeetingInfo(
                meetingId=capture.CapturedId,
                meeting_name=room.name,
                description=capture.summary,
                startTime=capture.StartTime,
                endTime=capture.EndTime,
                username=redis_db.smembers(f"meeting:{capture.CapturedId}"),
            )
        )
    return return_response(
        UserMeetingResponse(MeetList=meet_list, status=Error.NoError), response
    )
