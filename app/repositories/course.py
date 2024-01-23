from app.models import Course, CourseCategory
from app.repositories.base import BaseRepository


class CourseRepository(BaseRepository[Course]):
    def get_all_by_category_name(self, category_name: str) -> list[Course]:
        return (
            self.default_query.join(Course.course_category)
            .filter_by(name=category_name)
            .all()
        )

    def get_all_by_name_or_category_name(self, term: str) -> list[Course]:
        return (
            self.default_query.join(Course.course_category)
            .filter(
                (Course.name.ilike(f"%{term}%"))
                | (CourseCategory.name.ilike(f"%{term}%"))
            )
            .all()
        )
