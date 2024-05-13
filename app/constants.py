"""一些常量"""

from enum import IntEnum


class Error(IntEnum):
    NoError = 0
    # Register
    UserAlreadyExists = 1
    TelephoneAlreadyExists = 2
    IllegalUsername = 4
    IllegalPassword = 5
    MeetingNotExist = 6
    IllegalTelephone = 7
    CheckNotExist = 8
    # Code_Check
    RegisterCodeError = 9
    CodeError = 10
    LimitSendingCode = 11
    ReCAPTCHA_Error = 12
    # Email
    EmailSendingError = 13
    # login
    UserNotFound = 14
    PasswordError = 15
    UserBanned = 16
    # Ban
    BanAdmin = 17
    # PERMISSION
    PermissionDenied = 25
    # INVITATION
    CodeReadError = 30
    CodeWriteError = 27
    # RECORD
    RecordNotFound = 28
    DeleteError = 29
    # ...
    MeetingRoomIsCaptured = 31
    RedisError = 32
    # ...
    IllegalQQID = 26
    MeetingIsNotPassed = 33
    MeetingIsStarted = 35


# 错误HTTP状态码名称
class WrongFlag:
    WRONG_FLAG = -114


# 审查状态
WAITING = -1
ACCEPTED = 1
REJECTED = 0
