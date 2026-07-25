"""SQLAlchemy engine, session factory, and schema helpers."""

from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import Settings, get_settings


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""


def _sqlalchemy_database_url(url: str) -> str:
    if url.startswith("postgresql+psycopg://") or url.startswith("postgresql+psycopg2://"):
        return url
    if url.startswith("postgresql://"):
        return "postgresql+psycopg://" + url.removeprefix("postgresql://")
    if url.startswith("postgres://"):
        return "postgresql+psycopg://" + url.removeprefix("postgres://")
    return url


def create_db_engine(settings: Settings | None = None) -> Engine:
    cfg = settings or get_settings()
    return create_engine(_sqlalchemy_database_url(cfg.database_url), pool_pre_ping=True)


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


@contextmanager
def session_scope(engine: Engine) -> Generator[Session, None, None]:
    factory = create_session_factory(engine)
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def ensure_vector_extension(engine: Engine) -> None:
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))


def create_tables(engine: Engine) -> None:
    from app.db import models as _models  # noqa: F401

    Base.metadata.create_all(bind=engine)


def init_schema(engine: Engine) -> None:
    ensure_vector_extension(engine)
    create_tables(engine)
