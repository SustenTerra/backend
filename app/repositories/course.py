from sqlalchemy import func

from app.models import Course, CourseCategory, CourseChapter
from app.repositories.base import BaseRepository


class CourseRepository(BaseRepository[Course]):
    @property
    def base_query_for_list_view(self):
        return (
            self.session.query(
                Course.id,
                Course.name,
                Course.author_name,
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
        return self.base_query_for_list_view.all()

    def get_all_by_category_name(self, category_name: str):
        return self.base_query_for_list_view.filter(
            CourseCategory.name == category_name,
        ).all()

    def get_all_by_name_or_category_name(self, term: str):
        return self.base_query_for_list_view.filter(
            (Course.name.ilike(f"%{term}%"))
            | (CourseCategory.name.ilike(f"%{term}%"))
        ).all()
