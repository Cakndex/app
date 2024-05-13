"""
响应模型
"""

from typing import List

from pydantic import BaseModel

from app.models.schema import CheckInfo, UserInfo, UserMeetInfo, UserMeetingInfo


class Status(BaseModel):
    status: int = 0


class TokenResponse(Status):
    access: str = ""
    userId: int = 0
    username: str = ""
    admin: bool = False  # 判断是否为管理员（注册一律认定为否）


class AccessTokenResponse(Status):
    access: str


class UsersResponse(Status):
    list: List[UserInfo] = []


class UserInfoResponse(Status):
    userId: int = 0
    username: str = ""
    admin: bool = False
    banned: bool = False
    telephone: str = ""


class AdminCodeResponse(Status):
    inviteCode: int = 0


class MeetingResponse(Status):
    name: str = ""
    address: str = ""
    facilities: list[str] = []
    isCaptured: bool = False


class CheckResponse(Status):
    Checklist: List[CheckInfo] = []


class CreateCheckResponse(Status):
    CheckId: int = 0


class UserMeetResponse(Status):
    meetList: List[UserMeetInfo] = []


class UserMeetingResponse(Status):
    meetList: List[UserMeetingInfo] = []
