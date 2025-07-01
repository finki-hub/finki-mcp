from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent, ToolAnnotations
from starlette.requests import Request
from starlette.responses import PlainTextResponse

from tools.consultations import get_consultations_for_staff
from tools.staff import get_staff
from utils.settings import Settings

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
        name="get_staff",
        description="Преземи листа од наставниот кадар на ФИНКИ",
        annotations=ToolAnnotations(
            title="Преземи наставен кадар",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=False,
        ),
    )
    async def get_staff_tool() -> list[TextContent]:
        result = await get_staff()

        if isinstance(result, str):
            return [TextContent(type="text", text=result)]

        return [TextContent(type="text", text=name) for name in result]

    @mcp.tool(
        name="get_consultations_for_staff",
        description="Преземи закажани термини за консултации за член на наставниот кадар на ФИНКИ",
        annotations=ToolAnnotations(
            title="Преземи термини за консултации",
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=False,
        ),
    )
    async def get_consultations_for_staff_tool(staff_name: str) -> list[TextContent]:
        result = await get_consultations_for_staff(staff_name)

        if isinstance(result, str):
            return [TextContent(type="text", text=result)]

        return [TextContent(type="text", text=consultation) for consultation in result]

    return mcp


app = make_app(settings)
