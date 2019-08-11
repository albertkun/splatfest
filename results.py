import urllib.request
import json
import requests
from config import Config

hosts = ["albertk"]

def get_matches(username):
    url = "https://stat.ink/api/v2/battle"

    parameters = {'screen_name':username}

    response = requests.get(url, params=parameters)
    data = json.loads(response.text)
    print(data)
    return(data)


matches = get_matches("albertk")
