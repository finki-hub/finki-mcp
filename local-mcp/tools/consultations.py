import httpx
from bs4 import BeautifulSoup

URL = "https://konsultacii.finki.ukim.mk"


async def get_consultations_for_staff(staff_name: str) -> str | list[str]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(URL)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            cards = soup.select("div.card-style")

            if not cards:
                return "Не се пронајдени записи."

            correct_card = None

            for card in cards:
                name = card.select_one("h5")

                if name is None:
                    continue

                name_text = name.get_text(strip=True)

                if name_text.lower() == staff_name.lower():
                    correct_card = card
                    break

            if correct_card is None:
                return f"Не се пронајдени записи за {staff_name}."

            link = correct_card.select_one("a")

            if link is None:
                return f"Не се пронајдени записи за {staff_name}."

            url = link.get("href")

            if not isinstance(url, str):
                return f"Не се пронајдени записи за {staff_name}."

            consultations = await client.get(URL + url)
            consultations.raise_for_status()
            consultations_soup = BeautifulSoup(consultations.content, "html.parser")

            rows = consultations_soup.select("table tr")

            if not rows:
                return f"Нема закажани консултации за {staff_name}."

            results: list[str] = []

            for row in rows:
                cells = row.select("td")

                if not cells:
                    continue

                date = cells[0].get_text(strip=True)
                time = cells[1].get_text(strip=True)
                location = cells[2].get_text(strip=True)

                results.append(
                    f"{staff_name} има закажани консултации на датум {date} во време {time} на локација {location}.",
                )

            if not results:
                return f"Нема закажани консултации за {staff_name}."

            return results

    except Exception as e:
        return f"Настана грешка: {e!s}"
