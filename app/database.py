from datetime import datetime
from typing import Optional
from sqlalchemy import String, select, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, mapped_column, Mapped, DeclarativeBase, sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.engine import create_engine
from app.config import settings


engine = create_engine(settings.DATABASE_URL)
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
    bio: Mapped[Optional[str]] = mapped_column(Text)
    password_hash: Mapped[str] = mapped_column(String)

    languages: Mapped[list["Language"]] = relationship(back_populates="author")


class Language(Base):
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_private: Mapped[bool] = mapped_column(default=True, nullable=False)

    author: Mapped["User"] = relationship(back_populates="languages")
    notes: Mapped[list["Note"]] = relationship(back_populates="language")


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    language: Mapped["Language"] = relationship(back_populates="notes")


def get_user_by_id(db, user_id) -> User | None:
    return db.scalars(select(User).where(User.id == user_id)).first()


def get_language_by_id(db, language_id) -> Language | None:
    return db.scalars(select(Language).where(Language.id == language_id)).first()


def get_note_by_id(db, note_id) -> Note | None:
    return db.scalars(select(Note).where(Note.id == note_id)).first()

