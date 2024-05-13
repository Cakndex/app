"""
请求模型
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RegisterInRequest(BaseModel):
    code: Optional[str]
    isAdmin: bool = False
    password: str
    telephone: str
    username: str


class LoginRequest(BaseModel):
    password: str
    username: str  # 使用用户名或者邮箱登录


# user
class UserToggleRequest(BaseModel):
    userId: int = 0
    value: bool = False


class ScoreBoardRequest(BaseModel):
    category: str = "All"
    userGroup: int = 0


class HiddenBodyRequest(BaseModel):
    levelId: int = 0
    hidden: bool = True


class ChangePasswordRequest(BaseModel):
    NewPassword: str
    userId: int


class MeetingAddRequest(BaseModel):
    id: int = 0
    name: Optional[str]
    address: Optional[str]
    facilities: Optional[list[str]]


class CheckRequest(BaseModel):
    CapturedId: int = 0
    isCheck: bool = False
    reason: str = ""


class MeetingApplyRequest(BaseModel):
    StartTime: datetime
    EndTime: datetime
    number: int = 0
    summary: str = ""
