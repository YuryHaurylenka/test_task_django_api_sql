import logging

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger("api")


def fetch_og_data(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        og_data = {
            "title": (
                soup.find("meta", property="og:title")["content"]
                if soup.find("meta", property="og:title")
                else None
            ),
            "description": (
                soup.find("meta", property="og:description")["content"]
                if soup.find("meta", property="og:description")
                else None
            ),
            "image": (
                soup.find("meta", property="og:image")["content"]
                if soup.find("meta", property="og:image")
                else None
            ),
            "type": (
                soup.find("meta", property="og:type")["content"]
                if soup.find("meta", property="og:type")
                else "website"
            ),
        }

        if not og_data["title"]:
            og_data["title"] = soup.title.string if soup.title else "No title available"
        if not og_data["description"]:
            og_data["description"] = (
                soup.find("meta", attrs={"name": "description"})["content"]
                if soup.find("meta", attrs={"name": "description"})
                else "No description available"
            )
        if not og_data["image"]:
            og_data["image"] = "https://example.com/default-image.jpg"

        return og_data

    except Exception as e:
        logger.error(f"Failed to fetch Open Graph data for {url}: {e}")
        return {
            "title": "No title available",
            "description": "No description available",
            "image": "https://example.com/default-image.jpg",
            "type": "website",
        }
