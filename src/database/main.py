import logging
import sys
from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

log = logging.getLogger()


def _get_db_url() -> str:
    username = environ.get("DB_USER")
    password = environ.get("DB_PASS")
    host = environ.get("DB_HOST")
    port = environ.get("DB_PORT")
    db_name = environ.get("DB_NAME")

    # Breaking dependency inversion because I only plan on using postgres
    # Could probably make this respect DIP by not hardcoding the driver
    return f"postgresql://{username}:{password}@{host}:{port}/{db_name}"


try:
    engine = create_engine(_get_db_url())
    session_factory = sessionmaker(autoflush=False, autocommit=False, bind=engine)
except:  # noqa
    log.critical("Failed to connect to database")
    sys.exit(1)


def get_session(**kwargs) -> Session:
    with session_factory(**kwargs) as session:
        yield session
