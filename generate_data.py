import logging
import random
import string
import time

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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
    "https://www.bbc.com/news/world-europe-66858850",
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://www.last.fm/music/The+Beatles/_/Hey+Jude",
    "https://en.wikipedia.org/wiki/Open_Graph_protocol",
    "https://soundcloud.com/user-532218444/who-we-are",
    "https://vimeo.com/76979871",
    "https://www.goodreads.com/book/show/13496.A_Game_of_Thrones",
    "https://github.com/python/cpython",
    "https://realpython.com/python-requests/",
    "https://developer.mozilla.org/en-US/docs/Web/HTML",
    "https://pypi.org/project/requests/",
    "https://news.ycombinator.com/",
    "https://www.rottentomatoes.com/m/inception",
    "https://www.apple.com/macbook-air/",
]


def generate_urls_with_params(base_urls, count=100):
    urls = set()
    while len(urls) < count:
        base_url = random.choice(base_urls)
        params = generate_random_params()
        full_url = f"{base_url}?{params}"
        urls.add(full_url)
    return list(urls)


def generate_random_email():
    return f"user{random.randint(1, 99999)}@example.com"


def generate_random_password():
    return "testpassword"


def register_user():
    email = generate_random_email()
    password = generate_random_password()
    data = {"email": email, "password": password}
    response = requests.post(REGISTER_URL, json=data)

    if response.status_code == 201:
        logger.info(f"User registered: {email}")
        return email, password
    else:
        logger.error(f"Failed to register user: {response.text}")
        return None, None


def login_user(email, password):
    data = {"email": email, "password": password}
    response = requests.post(LOGIN_URL, json=data)

    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens.get("access")
        logger.info(f"User logged in: {email}")
        return access_token
    else:
        logger.error(f"Failed to log in user {email}: {response.text}")
        return None


def create_links_for_user(access_token, num_links):
    headers = {"Authorization": f"Bearer {access_token}"}
    used_urls = set()

    for _ in range(num_links):
        available_urls = list(set(generate_urls_with_params(BASE_URLS)))
        if not available_urls:
            break

        url_data = {"url": random.choice(available_urls)}
        response = requests.post(LINKS_URL, json=url_data, headers=headers)

        if response.status_code == 201:
            logger.info(f"Link created: {url_data['url']}")
            used_urls.add(url_data["url"])
        else:
            logger.error(f"Failed to create link: {response.text}")


def process_user(min_links=1, max_links=10):
    email, password = register_user()
    if not email or not password:
        return

    access_token = login_user(email, password)
    if not access_token:
        return

    num_links = random.randint(min_links, max_links)
    logger.info(f"Creating {num_links} links for user {email}")
    create_links_for_user(access_token, num_links)


def main(num_users=10, min_links=0, max_links=20, delay=0.5):
    for _ in range(num_users):
        process_user(min_links, max_links)
        time.sleep(delay)


if __name__ == "__main__":
    main()
