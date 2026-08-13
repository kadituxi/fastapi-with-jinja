from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

engine = create_engine("sqlite:///db.db")
SessionLocal = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


def get_session_db():
    with SessionLocal() as session:
        yield session
