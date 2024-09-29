from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

from ._logger import logger


def new_connection(conn_str):
    engine = create_engine(conn_str, pool_size=NullPool)
    logger.debug(f"connection: {engine.url}")
    session_factory = sessionmaker(bind=engine, future=True)
    session = session_factory()
    return session


def exec_sql(session, sql_text):
    logger.debug(sql_text)
    return session.execute(text(sql_text))
