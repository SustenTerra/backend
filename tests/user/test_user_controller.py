import pytest
from sqlalchemy.orm import Session

from app.common.user.controller import UserController
from app.common.user.repository import UserRepository
from app.common.user.schema import UserCreate, UserUpdate, UserUpdatePassword
from app.models import (
    Address,
    ChapterContent,
    Course,
    CourseCategory,
    CourseChapter,
    Post,
    PostCategory,
    User,
)
from app.service.hashing import Hasher


class TestUserController:
    @pytest.fixture
    def setup(self, db_session, make_user):
        self.repository = UserRepository(User, db_session)
        self.controller = UserController(User, self.repository)

        self.created_user: User = make_user()
        self.repository.add(self.created_user)

    def test_create_user(self, setup, faker):
        create = UserCreate(
            email=faker.email(),
            full_name=faker.name(),
            password=faker.password(),
            phone="83940028922",
        )

        user = self.controller.create(create)

        assert user.id is not None
        assert user.email == create.email
        assert user.full_name == create.full_name

        found_user = self.repository.get_by_id(user.id)
        assert found_user is not None

    def test_get_user(self, setup):
        found_user = self.controller.get_by_id(self.created_user.id)
        assert found_user is not None
        assert found_user.id == self.created_user.id
        assert found_user.email == self.created_user.email
        assert found_user.full_name == self.created_user.full_name

    def test_get_all_users(self, setup):
        found_users = self.controller.get_all()
        assert len(found_users) == 1
        assert found_users[0].id == self.created_user.id
        assert found_users[0].email == self.created_user.email
        assert found_users[0].full_name == self.created_user.full_name

    def test_update_user(self, setup, faker):
        update = UserUpdate(
            email=faker.email(),
            full_name=faker.name(),
            phone="83940028923",
        )

        updated_user = self.controller.update(self.created_user.id, update)
        assert updated_user is not None
        assert updated_user.id == self.created_user.id
        assert updated_user.email == update.email
        assert updated_user.full_name == update.full_name
        assert updated_user.phone == update.phone

        found_user = self.repository.get_by_id(self.created_user.id)
        assert found_user is not None
        assert found_user.id == self.created_user.id
        assert found_user.email == update.email
        assert found_user.full_name == update.full_name
        assert found_user.phone == update.phone

    def test_update_user_password(self, setup, faker, make_user):
        old_password = faker.password()
        user: User = make_user(password=Hasher.get_password_hash(old_password))
        self.repository.add(user)

        new_password = faker.password()

        update = UserUpdatePassword(
            current_password=old_password, password=new_password
        )

        updated_user = self.controller.update_password(user.id, update)
        assert updated_user is not None
        assert updated_user.id == user.id

        found_user = self.repository.get_by_id(user.id)
        assert found_user is not None
        assert found_user.id == user.id
        assert found_user.email == user.email
        assert found_user.full_name == user.full_name
        assert found_user.phone == user.phone
        assert Hasher.verify_password(new_password, found_user.password)

    def test_delete_user(self, setup):
        self.controller.delete(self.created_user.id)

        found_user = self.repository.get_by_id(self.created_user.id)
        assert found_user is None

    def test_get_by_id(self, setup):
        found_user = self.controller.get_by_id(self.created_user.id)

        assert found_user is not None
        assert found_user.email == self.created_user.email
        assert found_user.full_name == self.created_user.full_name

    def test_delete_cascade_relationships(
        self,
        setup,
        db_session: Session,
        make_user_address,
        make_course_category,
        make_course,
        make_course_chapter,
        make_chapter_content,
        make_post_category,
        make_post,
    ):
        address: Address = make_user_address(user_id=self.created_user.id)
        db_session.add(address)
        db_session.commit()

        # Learning Module Entities
        course_category: CourseCategory = make_course_category()
        db_session.add(course_category)
        db_session.commit()

        course: Course = make_course(
            course_category=course_category, author_id=self.created_user.id
        )
        db_session.add(course)
        db_session.commit()

        course_chapter: CourseChapter = make_course_chapter(course=course, index=0)
        db_session.add(course_chapter)
        db_session.commit()

        chapter_content: ChapterContent = make_chapter_content(
            course_chapter=course_chapter, index=0
        )
        db_session.add(chapter_content)
        db_session.commit()

        # Marketplace Module Entities
        post_category: PostCategory = make_post_category()
        db_session.add(post_category)
        db_session.commit()

        post: Post = make_post(user=self.created_user, post_category=post_category)
        db_session.add(post)
        db_session.commit()

        def exists(entity, entity_id):
            return (
                db_session.query(entity).filter(entity.id == entity_id).first()
                is not None
            )

        address_id = address.id
        course_category_id = course_category.id
        course_id = course.id
        course_chapter_id = course_chapter.id
        chapter_content_id = chapter_content.id
        post_category_id = post_category.id
        post_id = post.id

        assert exists(Address, address_id)
        assert exists(CourseCategory, course_category_id)
        assert exists(Course, course_id)
        assert exists(CourseChapter, course_chapter_id)
        assert exists(ChapterContent, chapter_content_id)
        assert exists(PostCategory, post_category_id)
        assert exists(Post, post_id)
        assert exists(User, self.created_user.id)

        self.controller.delete(self.created_user.id)

        assert not exists(Address, address_id)
        assert exists(CourseCategory, course_category_id)
        assert not exists(Course, course_id)
        assert not exists(CourseChapter, course_chapter_id)
        assert not exists(ChapterContent, chapter_content_id)
        assert exists(PostCategory, post_category_id)
        assert not exists(Post, post_id)
        assert not exists(User, self.created_user.id)
