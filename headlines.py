"""Fetch and print up to five unique headlines from BBC News."""

import sys

import requests
from bs4 import BeautifulSoup

URL = "https://www.bbc.com/news"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )
}
HEADLINE_SELECTOR = 'h2[data-testid="card-headline"]'
HEADLINE_LIMIT = 5


def main() -> int:
    try:
        response = requests.get(URL, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.RequestException as exc:
        print(f"Error fetching news page: {exc}", file=sys.stderr)
        return 1

    soup = BeautifulSoup(response.text, "html.parser")
    headlines = []
    seen = set()

    for element in soup.select(HEADLINE_SELECTOR):
        headline = " ".join(element.get_text(" ", strip=True).split())
        if not headline:
            continue

        duplicate_key = headline.casefold()
        if duplicate_key in seen:
            continue

        seen.add(duplicate_key)
        headlines.append(headline)

        if len(headlines) == HEADLINE_LIMIT:
            break

    if not headlines:
        print(
            "No headlines were found. The page structure may have changed "
            "or the headlines may require JavaScript.",
            file=sys.stderr,
        )
        return 1

    for number, headline in enumerate(headlines, start=1):
        print(f"{number}. {headline}")

    if len(headlines) < HEADLINE_LIMIT:
        print(
            f"Warning: found only {len(headlines)} unique, non-empty "
            f"headline(s); expected {HEADLINE_LIMIT}.",
            file=sys.stderr,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
