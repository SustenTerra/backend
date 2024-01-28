import time
from random import choice, randint

from faker import Faker
from sqlalchemy.orm import Session, sessionmaker

from app.database.connection import engine
from app.hashing import Hasher
from app.models import (
    ChapterContent,
    ContentStatusEnum,
    Course,
    CourseCategory,
    CourseChapter,
    FavoritedPost,
    Post,
    PostCategory,
    User,
    UserContentStatus,
)

faker = Faker(locale="pt_BR")


def get_db_session():
    SessionLocal = sessionmaker(bind=engine)
    engine.echo = False
    session = SessionLocal()

    return session


def clear_all_tables(session: Session):
    session.query(FavoritedPost).delete()
    session.query(Post).delete()
    session.query(PostCategory).delete()
    session.query(UserContentStatus).delete()
    session.query(User).delete()
    session.query(ChapterContent).delete()
    session.query(CourseChapter).delete()
    session.query(Course).delete()
    session.query(CourseCategory).delete()

    session.commit()


def create_users(session: Session):
    user = User(
        full_name="John Doe",
        email="usuario@email.com",
        phone="123456789",
        password=Hasher.get_password_hash("12345678"),
    )
    session.add(user)

    for _ in range(10):
        user = User(
            full_name=faker.name(),
            email=faker.email(),
            phone=faker.phone_number(),
            password=faker.password(),
        )

        session.add(user)
    session.commit()


def create_post_categories(session: Session):
    for _ in range(10):
        post_category = PostCategory(
            name=faker.text(max_nb_chars=10),
        )

        session.add(post_category)
    session.commit()


def create_posts(session: Session):
    for _ in range(10):
        users = session.query(User).all()
        user = choice(users)

        categories = session.query(PostCategory).all()
        category = choice(categories)

        post = Post(
            title=faker.text(max_nb_chars=30),
            image_url=faker.image_url(),
            description=faker.text(max_nb_chars=200),
            price=faker.pyint(min_value=0, max_value=1000),
            views=faker.pyint(min_value=0, max_value=1000),
            user_id=user.id,
            category_id=category.id,
        )

        session.add(post)
    session.commit()


def create_favorited_posts(session: Session):
    for _ in range(10):
        users = session.query(User).all()
        user = choice(users)

        posts = session.query(Post).all()
        post = choice(posts)

        favorited_post = FavoritedPost(
            user_id=user.id,
            post_id=post.id,
        )

        session.add(favorited_post)
    session.commit()


def create_course_categories(session: Session):
    for _ in range(10):
        course_category = CourseCategory(
            name=faker.text(max_nb_chars=10),
        )

        session.add(course_category)
    session.commit()


def create_courses(session: Session):
    for _ in range(10):
        categories = session.query(CourseCategory).all()
        category = choice(categories)

        course = Course(
            name=faker.text(max_nb_chars=30),
            description=faker.text(max_nb_chars=200),
            author_name=faker.name(),
            course_category_id=category.id,
        )

        session.add(course)
    session.commit()


def create_course_chapters(session: Session):
    courses = session.query(Course).all()

    for course in courses:
        for i in range(randint(1, 5)):
            course_chapter = CourseChapter(
                name=faker.text(max_nb_chars=30),
                course_id=course.id,
                index=i,
            )

            session.add(course_chapter)
    session.commit()


def create_chapter_contents(session: Session):
    course_chapters = session.query(CourseChapter).all()

    for course_chapter in course_chapters:
        for i in range(randint(1, 3)):
            chapter_content = ChapterContent(
                name=faker.text(max_nb_chars=30),
                description=faker.text(max_nb_chars=200),
                video_url="https://www.youtube.com/watch?v=dTND2d0Djh4",
                course_chapter_id=course_chapter.id,
                index=i,
            )

            session.add(chapter_content)
    session.commit()


def create_user_content_statuses(session: Session):
    users = session.query(User).all()
    courses = session.query(Course).all()

    for user in users:
        for course in courses:
            chapters = session.query(CourseChapter).filter_by(
                course_id=course.id
            )
            for chapter in chapters:
                contents = session.query(ChapterContent).filter_by(
                    course_chapter_id=chapter.id
                )
                for index, content in enumerate(contents):
                    status = ContentStatusEnum.not_started
                    if index == 0:
                        status = ContentStatusEnum.in_progress

                    user_content_status = UserContentStatus(
                        user_id=user.id,
                        chapter_content_id=content.id,
                        status=status,
                    )

                    session.add(user_content_status)

    session.commit()


def main():
    answer = input(
        "This will clear all tables and seed the database.\
              Are you sure? (y/N) "
    )
    if answer.lower() != "y":
        print("Aborting...")
        return

    duration = time.time()
    session = get_db_session()

    print("Clearing all tables...")
    clear_all_tables(session)

    print("Creating users...")
    create_users(session)

    print("Creating post categories...")
    create_post_categories(session)

    print("Creating posts...")
    create_posts(session)

    print("Creating favorited posts...")
    create_favorited_posts(session)

    print("Creating course categories...")
    create_course_categories(session)

    print("Creating courses...")
    create_courses(session)

    print("Creating course chapters...")
    create_course_chapters(session)

    print("Creating chapter contents...")
    create_chapter_contents(session)

    print("Creating user content statuses...")
    create_user_content_statuses(session)

    session.close()

    duration = time.time() - duration
    print(f"Done in {duration:.2f} seconds!")


if __name__ == "__main__":
    main()
