import os

import requests
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("DISCORD_URL")

headers = {"Content-Type": "application/json"}

data = {"content": "test_msg"}

response = requests.post(url, json=data)
print(response)
