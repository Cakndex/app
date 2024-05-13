"""数据库实例化"""

from redis import StrictRedis
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.settings import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
# 初始化数据库
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
# REDIS创建
redis_db = StrictRedis.from_url(settings.REDIS_URL, decode_responses=True)


def init_database():
    return Base.metadata.create_all(bind=engine)
