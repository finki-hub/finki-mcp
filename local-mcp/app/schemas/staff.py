from pydantic import BaseModel, Field


class StaffData(BaseModel):
    course: str = Field(
        ...,
        description="The name of the course",
        examples=["Структурно програмирање"],
    )
    professors: list[str] = Field(
        ...,
        description="List of professors teaching the course",
        examples=[["Ѓорѓи Маџаров", "Ана Мадевска Богданова"]],
    )
    assistants: list[str] = Field(
        ...,
        description="List of assistants for the course",
        examples=[["Александар Тенев", "Влатко Спасев"]],
    )
    error: str | None = Field(
        None,
        description="Error message if the course is not found or other issues",
        examples=["Course 'структурно програмирање' not found"],
    )
    suggestions: list[str] | None = Field(
        None,
        description="List of suggested course names if no exact match is found",
        examples=[["Структурно програмирање", "Програмирање 1"]],
    )
    match_info: dict | None = Field(
        None,
        description="Metadata about the matching process, including original query, matched course, similarity score, and match type",
        examples=[
            {
                "original_query": "структурно програмирање",
                "matched_course": "Структурно програмирање",
                "similarity_score": 95,
                "match_type": "fuzzy",
            },
        ],
    )
