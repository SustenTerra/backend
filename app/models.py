import enum
from datetime import datetime
from typing import List

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    declarative_base,
    mapped_column,
    relationship,
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(nullable=False)
    full_name: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    posts: Mapped[List["Post"]] = relationship(back_populates="user")
    favorited_posts: Mapped[List["FavoritedPost"]] = relationship(
        back_populates="user"
    )


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    image_url: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    views: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="posts")
    category_id: Mapped[int] = mapped_column(ForeignKey("post_categories.id"))
    category: Mapped["PostCategory"] = relationship(back_populates="posts")


class FavoritedPost(Base):
    __tablename__ = "favorited_posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="favorited_posts")
    post: Mapped["Post"] = relationship()


class PostCategory(Base):
    __tablename__ = "post_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    posts: Mapped[List["Post"]] = relationship(back_populates="category")


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    author_name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    course_chapters: Mapped[List["CourseChapter"]] = relationship(
        back_populates="course",
        lazy="joined",
        order_by="CourseChapter.index",
    )
    course_category_id: Mapped[int] = mapped_column(
        ForeignKey("course_categories.id")
    )
    course_category: Mapped["CourseCategory"] = relationship(
        back_populates="courses",
        lazy="joined",
    )


class CourseCategory(Base):
    __tablename__ = "course_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    courses: Mapped[List["Course"]] = relationship(
        back_populates="course_category"
    )


class CourseChapter(Base):
    __tablename__ = "course_chapters"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    index: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    course: Mapped["Course"] = relationship(back_populates="course_chapters")

    chapter_contents: Mapped[List["ChapterContent"]] = relationship(
        back_populates="course_chapter",
        lazy="joined",
        order_by="ChapterContent.index",
    )


class ChapterContent(Base):
    __tablename__ = "chapter_contents"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    index: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    video_url: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    course_chapter_id: Mapped[int] = mapped_column(
        ForeignKey("course_chapters.id")
    )
    course_chapter: Mapped["CourseChapter"] = relationship(
        back_populates="chapter_contents"
    )


class ContentStatusEnum(enum.Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"


class UserContentStatus(Base):
    __tablename__ = "user_content_status"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    chapter_content_id: Mapped[int] = mapped_column(
        ForeignKey("chapter_contents.id")
    )
    status: Mapped[ContentStatusEnum] = mapped_column(
        Enum(ContentStatusEnum),
        nullable=False,
        default=ContentStatusEnum.not_started,
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped["User"] = relationship()
    chapter_content: Mapped["ChapterContent"] = relationship()
