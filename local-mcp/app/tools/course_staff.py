import json
from functools import lru_cache
from pathlib import Path

with Path("/data/course_staff.json").open("r", encoding="utf-8") as file:
    course_staff_data = json.load(file)
    for row in course_staff_data:
        row["professors"] = row["professors"].split("\n")
        row["assistants"] = row["assistants"].split("\n")


@lru_cache(maxsize=128)
def get_available_courses_for_staff() -> list[str]:
    return [row["course"] for row in course_staff_data]


@lru_cache(maxsize=128)
def get_staff_for_course(course_name: str) -> dict:
    for row in course_staff_data:
        if row["course"] == course_name:
            return row

    return {
        "course": course_name,
        "professors": [],
        "assistants": [],
        "error": "Course not found",
    }
