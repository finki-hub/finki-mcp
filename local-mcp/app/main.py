from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from starlette.requests import Request
from starlette.responses import PlainTextResponse

from app.schemas.staff import StaffData
from app.tools.course_staff import (
    get_available_courses_for_staff,
    get_staff_for_course,
)
from app.utils.query_matcher import (
    match_query_to_candidates,
)
from app.utils.settings import Settings

settings = Settings()


def make_app(settings: Settings) -> FastMCP:
    mcp = FastMCP(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        version=settings.API_VERSION,
        port=settings.PORT,
        host=settings.HOST,
    )

    @mcp.custom_route("/health", methods=["GET", "HEAD"])
    async def health_check(request: Request) -> PlainTextResponse:
        return PlainTextResponse("OK")

    @mcp.tool(
        name="get_available_courses_with_staff_data",
        description="Get a list of available courses for staff.",
        annotations=ToolAnnotations(
            title="Get Available Courses for Staff",
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
            readOnlyHint=True,
        ),
    )
    async def get_courses_with_staff_data() -> list[str]:
        result = get_available_courses_for_staff()

        return result

    @mcp.tool(
        name="get_staff_data_for_course",
        description="Get staff data for a specific course.",
        annotations=ToolAnnotations(
            title="Get Staff Data for Course",
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=True,
            readOnlyHint=True,
        ),
    )
    async def get_staff_data_for_course(course_name: str) -> StaffData:
        course_names = get_available_courses_for_staff()
        result = match_query_to_candidates(course_name, course_names)
        if result["match"]:
            staff_data = get_staff_for_course(result["match"])
            staff_data["match_info"] = {
                "original_query": course_name,
                "matched_course": result["match"],
                "similarity_score": result["score"],
                "match_type": result["match_type"],
            }
            return StaffData(**staff_data)

        suggestions = result.get("suggestions")
        if not isinstance(suggestions, list):
            suggestions = None

        return StaffData(
            course=course_name,
            professors=[],
            assistants=[],
            error=f"Course '{course_name}' not found",
            suggestions=suggestions,
            match_info=None,
        )

    return mcp


app = make_app(settings)
