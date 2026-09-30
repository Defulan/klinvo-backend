from datetime import datetime
import sqlalchemy
from sqlalchemy import String, Integer, select, Text
from sqlalchemy.orm import relationship, mapped_column, Mapped, DeclarativeBase, sessionmaker
from sqlalchemy.engine import create_engine, Engine

@sqlalchemy.event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SQLALCHEMY_DATABASE_URL = "sqlite:///../data.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    password_hash: Mapped[str] = mapped_column(String)


class Language(Base):
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column()


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    language_id: Mapped[int] = mapped_column()
    content: Mapped[Text] = mapped_column()
    created_at: Mapped[datetime] = mapped_column()


def get_user_by_id(db, user_id) -> User | None:
    return db.scalars(select(User).where(User.id == user_id)).first()


def get_language_by_id(db, language_id) -> User | None:
    return db.scalars(select(Language).where(Language.id == language_id)).first()

