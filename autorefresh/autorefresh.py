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

LOGIN_URL = "https://concerto-lally.cs.rpi.edu/users/sign_in"
REFRESH_URL = "https://concerto-lally.cs.rpi.edu/remote_feeds/4/refresh"

session = requests.Session()


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
        try:
            resp = session.get(REFRESH_URL, verify=False)
            resp.raise_for_status()
            print("Refreshed")
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(DELAY_MINUTES * 60)


if __name__ == "__main__":
    login()
    refresh_loop()
