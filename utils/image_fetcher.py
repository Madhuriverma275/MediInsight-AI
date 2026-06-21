import os
import requests
from dotenv import load_dotenv

load_dotenv()

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")


def get_exercise_image(query):

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    url = (
        f"https://api.pexels.com/v1/search"
        f"?query={query}&per_page=1"
    )

    response = requests.get(
        url,
        headers=headers
    )

    data = response.json()

    if data.get("photos"):

        return data["photos"][0]["src"]["large"]

    return None