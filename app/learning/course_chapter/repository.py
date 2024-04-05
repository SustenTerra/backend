from app.common.base.repository import BaseRepository
from app.models import CourseChapter


class CourseChapterRepository(BaseRepository[CourseChapter]):
    def get_all_chapters_by_course_id(self, course_id: int):
        return self.default_query.filter(
            CourseChapter.course_id == course_id
        ).all()
