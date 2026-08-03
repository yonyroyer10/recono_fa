from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from core.config import DATABASE_URL


def _build_engine():
    engine_kwargs = {"pool_pre_ping": True}
    if DATABASE_URL.startswith("sqlite"):
        engine_kwargs["connect_args"] = {"check_same_thread": False}
    return create_engine(DATABASE_URL, **engine_kwargs)


engine = _build_engine()
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = scoped_session(session_factory)
Base = declarative_base()


def init_db():
    import database.models
    Base.metadata.create_all(bind=engine)


def get_session():
    return Session()
