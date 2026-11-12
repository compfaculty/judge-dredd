import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

class Base(DeclarativeBase):
    pass

DATABASE_URL = os.environ.get("DREDD_DATABASE_URL", "sqlite:///./dredd.db")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def init_db():
    from . import models  # noqa: F401
    Base.metadata.create_all(bind=engine)

def get_db():
    with SessionLocal() as db:
        yield db
