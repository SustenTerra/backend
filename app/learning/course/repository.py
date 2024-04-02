from sqlalchemy import func

from app.common.base.repository import BaseRepository
from app.models import Course, CourseCategory, CourseChapter, UserContentStatus


class CourseRepository(BaseRepository[Course]):
    @property
    def query_for_list_view(self):
        return (
            self.session.query(
                Course.id,
                Course.name,
                Course.image_key,
                Course.author_name,
                CourseCategory.name.label("category_name"),
                func.count(CourseChapter.id).label("chapters_count"),
                Course.created_at,
                Course.updated_at,
            )
            .join(Course.course_chapters, isouter=True)
            .join(Course.course_category)
            .group_by(Course.id, CourseCategory.name)
            .filter(Course.published_at.isnot(None))
        )

    @property
    def query_list_view_for_teachers(self):
        return (
            self.session.query(
                Course.id,
                Course.name,
                Course.image_key,
                Course.author_name,
                Course.author_id,
                CourseCategory.name.label("category_name"),
                func.count(CourseChapter.id).label("chapters_count"),
                Course.created_at,
                Course.updated_at,
            )
            .join(Course.course_chapters, isouter=True)
            .join(Course.course_category)
            .group_by(Course.id, CourseCategory.name)
        )

    def get_all(self):
        return self.query_for_list_view.all()

    def get_all_by_category_name(self, category_name: str):
        return self.query_for_list_view.filter(
            CourseCategory.name == category_name,
        ).all()

    def get_all_by_name_or_category_name(self, term: str):
        return self.query_for_list_view.filter(
            (Course.name.ilike(f"%{term}%"))
            | (CourseCategory.name.ilike(f"%{term}%"))
        ).all()

    def get_all_in_progress(self, user_id: int):
        return (
            self.query_for_list_view.join(CourseChapter.chapter_contents)
            .join(UserContentStatus)
            .filter(UserContentStatus.user_id == user_id)
            .all()
        )

    def get_all_by_teacher_id(self, user_id: int):
        return self.query_list_view_for_teachers.filter(
            Course.author_id == user_id
        ).all()
