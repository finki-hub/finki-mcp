import json
from functools import lru_cache
from pathlib import Path

with Path("/data/course_participants.json").open("r", encoding="utf-8") as file:
    course_participants_data = json.load(file)


@lru_cache(maxsize=128)
def get_available_courses_for_participants() -> list[str]:
    return [row["course"] for row in course_participants_data]


@lru_cache(maxsize=128)
def get_participants_for_course(course_name: str) -> dict:
    for row in course_participants_data:
        if row["course"] == course_name:
            return row
    return {
        "course": course_name,
        "error": "Course not found",
    }
