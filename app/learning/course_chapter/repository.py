from app.common.base.repository import BaseRepository
from app.models import CourseChapter


class CourseChapterRepository(BaseRepository[CourseChapter]):
    @property
    def query_for_list_view(self):
        return self.session.query(
            CourseChapter.id, CourseChapter.name, CourseChapter.index
        )

    def get_all_by_course_id(self, course_id: int):
        return self.query_for_list_view.filter(
            CourseChapter.course_id == course_id
        ).all()
