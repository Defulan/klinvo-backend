from datetime import datetime
import sqlalchemy
from sqlalchemy import String, Integer, select, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped, DeclarativeBase, sessionmaker
from sqlalchemy.sql import func
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

    languages: Mapped[list["Language"]] = relationship(back_populates="author")


class Language(Base):
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    author: Mapped["User"] = relationship(back_populates="languages")
    notes: Mapped[list["Note"]] = relationship(back_populates="language")


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    language: Mapped["Language"] = relationship(back_populates="notes")


def get_user_by_id(db, user_id) -> User | None:
    return db.scalars(select(User).where(User.id == user_id)).first()


def get_language_by_id(db, language_id) -> User | None:
    return db.scalars(select(Language).where(Language.id == language_id)).first()

