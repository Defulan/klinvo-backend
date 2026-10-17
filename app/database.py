from datetime import datetime
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
    bio: Mapped[str | None] = mapped_column(Text)
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
    words: Mapped[list["Word"]] = relationship(back_populates="language")


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    language: Mapped["Language"] = relationship(back_populates="notes")


class Word(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(primary_key=True)
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"), nullable=False)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
    position: Mapped[str] = mapped_column(nullable=False)
    value: Mapped[str] = mapped_column(String(255), nullable=False)
    meaning: Mapped[str] = mapped_column(String(255), nullable=False)

    language: Mapped["Language"] = relationship(back_populates="words")
    category = Mapped["Category"] = relationship(back_populates="words")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"), nullable=False)
    position: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String(255))

    words = Mapped["Word"] = relationship(back_populates="category")


def get_user_by_id(db, user_id) -> User | None:
    return db.scalars(select(User).where(User.id == user_id)).first()


def get_language_by_id(db, language_id) -> Language | None:
    return db.scalars(select(Language).where(Language.id == language_id)).first()


def get_note_by_id(db, note_id) -> Note | None:
    return db.scalars(select(Note).where(Note.id == note_id)).first()


def is_language_available_for_user(language: Language, user_id: int):
    if not language.is_private:
        return True
    
    return language.author_id == user_id
