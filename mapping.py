import os
import requests
from dotenv import load_dotenv
env = load_dotenv()

API_KEY = os.environ['MAPQUEST_API_KEY']


def get_map_url(address):
    """Get MapQuest URL for a static map for this location."""

    base = f"https://www.mapquestapi.com/staticmap/v5/map?key={API_KEY}"
    where = f"{address},Richmond,CA"

    return f"{base}&center={where}&size=600,400@2x&locations={where}"


def save_map(id, address):
    """Get static map and save in static/maps directory of this app."""
    try:
        map_img = get_map(address)

        path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         'static',
                         'maps',
                         f'map_{id}.png'
                         ))

        with open(path, 'wb') as file:
            file.write(map_img)

        return path

    except Exception:
        print(f"Error saving map: {Exception}")
        return None


def get_map(address):
    """ Makes request to API to get the map img. Returns img or error"""

    map_url = get_map_url(address)
    resp = requests.get(map_url)

    if resp.status_code == 200:
        map_img = resp.content

        return map_img

    else:
        resp.raise_for_status()
