"""数据库实例化"""

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.constants import WAITING
from app.database.db import Base


class User(Base):
    __tablename__ = "users"

    userId = Column(Integer, primary_key=True, autoincrement=True, index=True)
    # user might log in via either username or email
    username = Column(String(64), unique=True, index=True, nullable=False)
    password = Column(String(64), nullable=False)  # sha256 hashed password
    admin = Column(Boolean, nullable=False, default=False)  # is admin
    banned = Column(Boolean, nullable=False, default=False)  # is banned
    telephone = Column(String(16), nullable=False)

    __table_args__ = {"mysql_charset": "utf8mb4"}


class Meeting(Base):
    __tablename__ = "meetings"

    meetingId = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(64), nullable=False)
    address = Column(String(256), nullable=False)
    # 设施，如投影仪，白板，麦克风等
    facility = Column(String(256), nullable=False)

    __table_args__ = {"mysql_charset": "utf8mb4"}


class IsCaptured(Base):
    """会议室预约记录"""

    __tablename__ = "is_captured"

    CapturedId = Column(Integer, primary_key=True, autoincrement=True, index=True)
    userId = Column(Integer, nullable=False, index=True)
    meetingId = Column(Integer, nullable=False, index=True)
    StartTime = Column(DateTime, nullable=False)
    EndTime = Column(DateTime, nullable=False)
    # 人数
    number = Column(Integer, nullable=False)
    # 审核
    isPass = Column(Integer, nullable=False, default=WAITING)
    reason = Column(String(256), nullable=False, default=" ")
    __table_args__ = {"mysql_charset": "utf8mb4"}
