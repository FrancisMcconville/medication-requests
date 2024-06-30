from pathlib import Path

from pytest import fixture
from sqlalchemy.orm import Session

from alembic import command
from alembic.config import Config
from src.database.main import session_factory
from src.database.models import Base

PROJECT_ROOT = Path(__file__).resolve().parent.parent


@fixture
def run_alembic():
    alembic_ini_path = PROJECT_ROOT / "alembic.ini"
    alembic_cfg = Config(alembic_ini_path.as_posix())
    command.upgrade(alembic_cfg, "head")


@fixture(autouse=True)
def session(run_alembic) -> Session:
    with session_factory() as session:
        yield session
        for table in reversed(Base.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()
