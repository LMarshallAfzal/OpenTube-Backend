""" Builds SQLAlchemy engine from settings & handling thread-safety """
from __future__ import annotations

from sqlalchemy.engine import Engine, URL
from sqlalchemy import create_engine
from typing import Dict

from core.settings import settings


def _sqlite_connect_args() -> Dict[str, object]:
    return {"check_same_thread": False}


def create_db_engine():
    """
    Builds an SQLAlchemy engine based on application settings

    Returns
    -------
    Engine
        An SQLAlchemy engine instance ready to be used by sqlmodel.Session
    """
    connect_args: Dict[str, object] = {}

    if settings.DB_DRIVER == "sqlite":
        connect_args.update(_sqlite_connect_args())

    # `echo` is turned off in production; override via env var if needed.
    echo_flag = settings.SQLALCHEMY_ECHO or False

    return create_engine(
        settings.DATABASE_URL,
        connect_args=connect_args,
        echo=echo_flag,
        future=True,
    )


engine: Engine = create_db_engine()
