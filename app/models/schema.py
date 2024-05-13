"""
其他模型
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class UserInfo(BaseModel):
    userId: int = 0
    admin: bool = False
    banned: bool = False
    telephone: str = ""
    username: str = ""


class MeetingInfo(BaseModel):
    name: str
    address: str
    facilities: list[str]


class CheckInfo(BaseModel):
    username: str = ""
    meetingName: str = ""
    meetingStartTime: datetime
    meetingEndTime: datetime
    meetingAddress: str = ""
    checkReason: str = ""
    isPassed: int = -1
    number: int = 0


class UserMeetInfo(BaseModel):
    meetingId: int = 0
    name: str = ""
    isCaptured: bool = False


class UserMeetingInfo(BaseModel):
    meetId: int = 0
    meeting_name: str = ""
    reason: str = ""
    startTime: datetime
    endTime: datetime
    username: list = []
    is_passed: int
