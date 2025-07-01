import httpx
from bs4 import BeautifulSoup

URL = "https://konsultacii.finki.ukim.mk"


async def get_staff() -> str | list[str]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(URL)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            cards = soup.select("div.card-style > h5")

            if not cards:
                return "Не се пронајдени записи."

            result: list[str] = []

            for person in cards:
                name = person.get_text(strip=True)
                result.append(name)
            return result

    except Exception as e:
        return f"Настана грешка: {e!s}"
