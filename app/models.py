import enum
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    declarative_base,
    mapped_column,
    relationship,
)

from app.common.utils import datetime_now

Base = declarative_base()


class BaseTable(Base):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(default=datetime_now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime_now)


class AddressBaseTable(BaseTable):
    __abstract__ = True

    street: Mapped[str] = mapped_column(nullable=False)
    number: Mapped[str] = mapped_column(nullable=False)
    neighborhood: Mapped[str] = mapped_column(nullable=False)
    complement: Mapped[Optional[str]] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=False)
    state: Mapped[str] = mapped_column(nullable=False)
    cep: Mapped[str] = mapped_column(nullable=False)


class User(BaseTable):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    teacher_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(nullable=False)
    full_name: Mapped[str] = mapped_column(nullable=False)

    courses: Mapped[List["Course"]] = relationship()

    posts: Mapped[List["Post"]] = relationship(back_populates="user")
    favorited_posts: Mapped[List["FavoritedPost"]] = relationship(back_populates="user")

    address: Mapped["Address"] = relationship(back_populates="user")


class Post(BaseTable):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    image_key: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    post_type: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[Optional[int]] = mapped_column(nullable=True)
    views: Mapped[int] = mapped_column(server_default="0")
    available_quantity: Mapped[int] = mapped_column(nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="posts")
    category_id: Mapped[int] = mapped_column(ForeignKey("post_categories.id"))
    category: Mapped["PostCategory"] = relationship(back_populates="posts")


class FavoritedPost(BaseTable):
    __tablename__ = "favorited_posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))

    user: Mapped["User"] = relationship(back_populates="favorited_posts")
    post: Mapped["Post"] = relationship()


class PostCategory(BaseTable):
    __tablename__ = "post_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    posts: Mapped[List["Post"]] = relationship(back_populates="category")


class Course(BaseTable):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    author_name: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    image_key: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    published_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    course_chapters: Mapped[List["CourseChapter"]] = relationship(
        back_populates="course",
        lazy="joined",
        order_by="CourseChapter.index",
    )
    course_category_id: Mapped[int] = mapped_column(ForeignKey("course_categories.id"))
    course_category: Mapped["CourseCategory"] = relationship(
        back_populates="courses",
        lazy="joined",
    )


class CourseCategory(BaseTable):
    __tablename__ = "course_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    courses: Mapped[List["Course"]] = relationship(back_populates="course_category")


class CourseChapter(BaseTable):
    __tablename__ = "course_chapters"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    index: Mapped[int] = mapped_column(nullable=False)

    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    course: Mapped["Course"] = relationship(back_populates="course_chapters")

    chapter_contents: Mapped[List["ChapterContent"]] = relationship(
        back_populates="course_chapter",
        lazy="joined",
        order_by="ChapterContent.index",
    )


class ChapterContent(BaseTable):
    __tablename__ = "chapter_contents"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    index: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    video_url: Mapped[Optional[str]] = mapped_column(nullable=True)

    course_chapter_id: Mapped[int] = mapped_column(ForeignKey("course_chapters.id"))
    course_chapter: Mapped["CourseChapter"] = relationship(
        back_populates="chapter_contents"
    )


class ContentStatusEnum(enum.Enum):
    not_started = "not_started"
    in_progress = "in_progress"
    completed = "completed"


class UserContentStatus(BaseTable):
    __tablename__ = "user_content_status"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    chapter_content_id: Mapped[int] = mapped_column(ForeignKey("chapter_contents.id"))
    status: Mapped[ContentStatusEnum] = mapped_column(
        Enum(ContentStatusEnum),
        nullable=False,
        default=ContentStatusEnum.not_started,
    )

    user: Mapped["User"] = relationship()
    chapter_content: Mapped["ChapterContent"] = relationship()


class Address(AddressBaseTable):
    __tablename__ = "addresses"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="address")


class Order(BaseTable):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    order_address_id: Mapped[int] = mapped_column(ForeignKey("order_addresses.id"))
    total: Mapped[int] = mapped_column(nullable=False)

    user: Mapped["User"] = relationship()
    post: Mapped["Post"] = relationship()
    address: Mapped["OrderAddress"] = relationship()


class OrderAddress(AddressBaseTable):
    __tablename__ = "order_addresses"
    id: Mapped[int] = mapped_column(primary_key=True)
