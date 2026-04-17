import os
import time
import requests
import urllib3
from bs4 import BeautifulSoup
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
DELAY_MINUTES = int(os.getenv("DELAY_MINUTES", 5))
FEED_NUMBERS_RAW = os.getenv("FEED_NUMBERS", "")
RSS_FEED_NUMBERS_RAW = os.getenv("RSS_FEED_NUMBERS", "")

LOGIN_URL = "https://concerto-lally.cs.rpi.edu/users/sign_in"
REMOTE_FEED_REFRESH_URL_TEMPLATE = "https://concerto-lally.cs.rpi.edu/remote_feeds/{feed_number}/refresh"
RSS_FEED_REFRESH_URL_TEMPLATE = "https://concerto-lally.cs.rpi.edu/rss_feeds/{feed_number}/refresh"

session = requests.Session()


def parse_feed_numbers(feed_numbers_raw, env_name):
    feed_numbers = [value.strip() for value in feed_numbers_raw.split(",") if value.strip()]
    if not feed_numbers:
        return []

    invalid_feed_numbers = [value for value in feed_numbers if not value.isdigit()]
    if invalid_feed_numbers:
        raise ValueError(
            f"{env_name} contains invalid values: {', '.join(invalid_feed_numbers)}"
        )

    return [int(feed_number) for feed_number in feed_numbers]


FEED_NUMBERS = parse_feed_numbers(FEED_NUMBERS_RAW, "FEED_NUMBERS")
RSS_FEED_NUMBERS = parse_feed_numbers(RSS_FEED_NUMBERS_RAW, "RSS_FEED_NUMBERS")

if not FEED_NUMBERS and not RSS_FEED_NUMBERS:
    raise ValueError("Set FEED_NUMBERS or RSS_FEED_NUMBERS with at least one feed number")


def get_authenticity_token():
    resp = session.get(LOGIN_URL, verify=False)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    token_input = soup.select_one("form#new_user input[name='authenticity_token']")

    if not token_input:
        raise Exception("Authenticity token not found")

    return token_input.get("value")


def login():
    token = get_authenticity_token()

    payload = {
        "authenticity_token": token,
        "user[email]": EMAIL,
        "user[password]": PASSWORD,
        "user[remember_me]": "0",
        "commit": "Log in"
    }

    resp = session.post(LOGIN_URL, data=payload, verify=False)
    resp.raise_for_status()

    if "Invalid Email or password" in resp.text:
        raise Exception("Login failed")


def refresh_loop():
    while True:
        for feed_number in FEED_NUMBERS:
            refresh_url = REMOTE_FEED_REFRESH_URL_TEMPLATE.format(feed_number=feed_number)
            try:
                resp = session.get(refresh_url, verify=False)
                resp.raise_for_status()
                print(f"Refreshed remote feed {feed_number}")
            except requests.RequestException as e:
                print(f"Error refreshing remote feed {feed_number}: {e}")

        for feed_number in RSS_FEED_NUMBERS:
            refresh_url = RSS_FEED_REFRESH_URL_TEMPLATE.format(feed_number=feed_number)
            try:
                resp = session.get(refresh_url, verify=False)
                resp.raise_for_status()
                print(f"Refreshed RSS feed {feed_number}")
            except requests.RequestException as e:
                print(f"Error refreshing RSS feed {feed_number}: {e}")

        time.sleep(DELAY_MINUTES * 60)


if __name__ == "__main__":
    login()
    refresh_loop()
