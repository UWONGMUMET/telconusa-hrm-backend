from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from core.config import Settings

engine = create_engine(Settings().database_url)
SessionLocal = sessionmaker(bind=engine)

def get_db() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session