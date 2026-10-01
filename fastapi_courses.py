from fastapi import FastAPI, APIRouter, HTTPException, status
from pydantic import BaseModel, RootModel

app = FastAPI()

# Создаём роутер с общим префиксом и тегом для Swagger
courses_router = APIRouter(
    prefix="/api/v1/courses",  # Добавляет /api/v1/courses ко всем путям в этом роутере
    tags=["courses-service"]  # Группирует маршруты под тегом "courses-service" в документации
)


class CourseIn(BaseModel):
    """
    Модель для приёма входных данных (создание и обновление курса).
    """
    title: str  # Название курса
    max_score: int  # Максимальный балл
    min_score: int  # Минимальный проходной балл
    description: str  # Краткое описание курса


class CourseOut(CourseIn):
    """
    Модель для отдачи данных о курсе, включая его ID.
    """
    id: int  # Уникальный идентификатор курса


class CoursesStore(RootModel):
    """
    In-memory хранилище курсов вместо реальной БД.
    """
    root: list[CourseOut]  # Список всех курсов

    def find(self, course_id: int) -> CourseOut | None:
        """
        Находит курс по ID.
        Возвращает CourseOut или None, если не найден.
        """
        return next(filter(lambda course: course.id == course_id, self.root), None)

    def create(self, course_in: CourseIn) -> CourseOut:
        """
        Создаёт новый курс, генерируя для него следующий ID.
        ID берётся на единицу больше максимального из существующих,
        чтобы после удаления курсов идентификаторы не повторялись.
        """
        course_id = max((course.id for course in self.root), default=0) + 1
        course = CourseOut(id=course_id, **course_in.model_dump())
        self.root.append(course)
        return course

    def update(self, course_id: int, course_in: CourseIn) -> CourseOut:
        """
        Обновляет существующий курс по ID.
        """
        # Находим индекс существующей записи
        index = next(index for index, course in enumerate(self.root) if course.id == course_id)
        # Создаём новый объект с тем же ID и обновлёнными полями
        updated = CourseOut(id=course_id, **course_in.model_dump())
        # Заменяем в списке
        self.root[index] = updated
        return updated

    def delete(self, course_id: int) -> None:
        """
        Удаляет курс по ID, фильтруя список.
        """
        self.root = [course for course in self.root if course.id != course_id]


# Инициализируем хранилище пустым списком
store = CoursesStore(root=[])


@courses_router.get("/{course_id}", response_model=CourseOut)
async def get_course(course_id: int):
    """
    GET /api/v1/courses/{course_id}
    Возвращает курс по ID или 404, если не найден.
    """
    if not (course := store.find(course_id)):
        raise HTTPException(
            detail=f"Course with id {course_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

    return course


@courses_router.get("", response_model=list[CourseOut])
async def get_courses():
    """
    GET /api/v1/courses
    Возвращает список всех курсов.
    """
    return store.root


@courses_router.post("", response_model=CourseOut, status_code=status.HTTP_201_CREATED)
async def create_course(course: CourseIn):
    """
    POST /api/v1/courses
    Создаёт новый курс и возвращает его данные с ID.
    """
    return store.create(course)


@courses_router.put("/{course_id}", response_model=CourseOut)
async def update_course(course_id: int, course: CourseIn):
    """
    PUT /api/v1/courses/{course_id}
    Обновляет данные курса по ID или возвращает 404, если не существует.
    """
    if not store.find(course_id):
        raise HTTPException(
            detail=f"Course with id {course_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

    return store.update(course_id, course)


@courses_router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int):
    """
    DELETE /api/v1/courses/{course_id}
    Удаляет курс по ID или возвращает 404, если не существует.
    """
    if not store.find(course_id):
        raise HTTPException(
            detail=f"Course with id {course_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

    store.delete(course_id)
    # При status_code=204 тело ответа пустое


# Подключаем роутер к основному приложению
app.include_router(courses_router)
