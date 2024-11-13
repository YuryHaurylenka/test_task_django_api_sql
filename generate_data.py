import asyncio
import logging
import random
import string

import httpx

logger = logging.getLogger("api")

BASE_URL = "http://localhost:8000"
REGISTER_URL = f"{BASE_URL}/auth/register/"
LOGIN_URL = f"{BASE_URL}/auth/login/"
LINKS_URL = f"{BASE_URL}/api/links/"


def generate_random_params():
    params = {
        "utm_source": random.choice(["google", "newsletter", "facebook", "twitter"]),
        "utm_medium": random.choice(["email", "social", "cpc", "organic"]),
        "utm_campaign": "".join(random.choices(string.ascii_lowercase, k=8)),
        "ref": "".join(random.choices(string.ascii_letters + string.digits, k=5)),
        "session_id": random.randint(1, 100),
        "user_id": random.randint(1, 100),
    }
    return "&".join([f"{key}={value}" for key, value in params.items()])


BASE_URLS = [
    "https://www.apple.com",
    "https://www.microsoft.com",
    "https://www.salesforce.com",
    "https://github.com/python/cpython",
    "https://pypi.org/project/requests/",
    "https://www.goodreads.com/book/show/13496.A_Game_of_Thrones",
    "https://www.goodreads.com/book/show/4671.The_Great_Gatsby",
    "https://openlibrary.org/works/OL82563W/War_and_Peace",
    "https://openlibrary.org/works/OL45883W/Pride_and_Prejudice",
    "https://www.bbc.com/news/world-europe-66858850",
    "https://news.ycombinator.com/",
    "https://realpython.com/python-requests/",
    "https://developer.mozilla.org/en-US/docs/Web/HTML",
    "https://www.last.fm/music/The+Beatles/_/Hey+Jude",
    "https://soundcloud.com/user-532218444/who-we-are",
    "https://soundcloud.com/radiohead/creep",
    "https://soundcloud.com/the-weeknd/blinding-lights",
    "https://soundcloud.com/edsheeran/shape-of-you",
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://vimeo.com/76979871",
    "https://music.youtube.com/watch?v=Zi_XLOBDo_Y",
    "https://music.youtube.com/watch?v=3JZ_D3ELwOQ",
    "https://www.apple.com/macbook-air/",
    "https://www.salesforce.com",
    "https://www.rottentomatoes.com/m/inception",
]


def generate_urls_with_params(base_urls, count=100):
    urls = set()
    while len(urls) < count:
        base_url = random.choice(base_urls)
        params = generate_random_params()
        if "?" in base_url:
            full_url = f"{base_url}&{params}"
        else:
            full_url = f"{base_url}?{params}"
        urls.add(full_url)
    return list(urls)


def generate_random_email():
    return f"user{random.randint(1, 99999)}@example.com"


def generate_random_password():
    return "testpassword"


async def send_request(url, method="post", data=None, headers=None):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(method, url, json=data, headers=headers)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"HTTP error: {exc.response.status_code} - {exc.response.text}"
            )
        except Exception as e:
            logger.error(f"Request failed: {e}")
        return None


async def register_user():
    email = generate_random_email()
    password = generate_random_password()
    data = {"email": email, "password": password}
    response = await send_request(REGISTER_URL, data=data)
    if response and response.status_code == 201:
        logger.info(f"User registered: {email}")
        return email, password
    return None, None


async def login_user(email, password):
    data = {"email": email, "password": password}
    response = await send_request(LOGIN_URL, data=data)
    if response and response.status_code == 200:
        tokens = response.json()
        access_token = tokens.get("access")
        logger.info(f"User logged in: {email}")
        return access_token
    return None


async def create_links_for_user(access_token, num_links):
    headers = {"Authorization": f"Bearer {access_token}"}
    urls = generate_urls_with_params(BASE_URLS, num_links)

    for url in urls:
        url_data = {"url": url}
        response = await send_request(LINKS_URL, data=url_data, headers=headers)
        if response and response.status_code == 201:
            logger.info(f"Link created: {url}")
        else:
            logger.error(f"Failed to create link")


async def process_user(min_links, max_links):
    email, password = await register_user()
    if not email or not password:
        return

    access_token = await login_user(email, password)
    if not access_token:
        return

    num_links = random.randint(min_links, max_links)
    logger.info(f"Creating {num_links} links for user {email}")
    await create_links_for_user(access_token, num_links)


async def main(num_users=25, min_links=0, max_links=50):
    tasks = [process_user(min_links, max_links) for _ in range(num_users)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
