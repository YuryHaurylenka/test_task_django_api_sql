import csv
import logging
import re

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger("api")


def fetch_og_data(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        og_type = (
            soup.find("meta", property="og:type")["content"]
            if soup.find("meta", property="og:type")
            else None
        )

        if og_type:
            og_type = og_type.lower()
            if "music" in og_type:
                content_type = "music"
            elif "book" in og_type:
                content_type = "book"
            elif "article" in og_type or "blog" in og_type:
                content_type = "article"
            elif "video" in og_type:
                content_type = "video"
            elif "object" in og_type:
                content_type = "object"
            else:
                content_type = "website"
        else:
            content_type = "website"

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
                else "https://example.com/default-image.jpg"
            ),
            "type": content_type,
        }

        if not og_data["title"]:
            og_data["title"] = soup.title.string if soup.title else "No title available"

        if not og_data["description"]:
            og_data["description"] = (
                soup.find("meta", attrs={"name": "description"})["content"]
                if soup.find("meta", attrs={"name": "description"})
                else "No description available"
            )

        return og_data

    except Exception as e:
        logger.error(f"Failed to fetch Open Graph data for {url}: {e}")
        return {
            "title": "Failed to fetch Open Graph data",
            "description": "Failed to fetch Open Graph data",
            "image": "Failed to fetch Open Graph data",
            "type": "error",
        }


def extract_uri(url):
    url = re.sub(r"^https?://(www\.)?", "", url, flags=re.IGNORECASE)
    return url.split("/", 1)[-1] if "/" in url else url


def save_to_csv(data, file_path):
    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "email",
            "count_links",
            "website",
            "book",
            "article",
            "music",
            "video",
            "object",
            "error",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
