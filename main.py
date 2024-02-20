import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

DISCORD_URL = os.environ.get("DISCORD_URL")
GEEKNEWS_BASEURL = "https://news.hada.io/"
GEEKNEWS_URL = "https://news.hada.io/new"
want_to_include = [
    "AI", "ai", "ML", "GPT", "LLM",
    "인공지능", "딥러닝", "머신러닝"
]
days_included = [f"{i}분전" for i in range(1, 16)]

headers = {"Content-Type": "application/json"}
messages = []

response = requests.get(GEEKNEWS_URL)
if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    topics = soup.find_all("div", class_="topic_row")

    for topic in topics:
        topic_title = topic.find("div", class_="topictitle")
        topic_content = topic.find("div", class_="topicdesc")
        topic_url = topic.find("span", class_="topicurl")
        topic_info = topic.find("div", class_="topicinfo")
        topic_date = topic_info.text.split(" ")[4]
        topic_link = topic_content.find("a")["href"].strip()
        title = topic_title.a.h1.string
        description = topic_content.a.string
        flag = False

        if topic_url.string is None:
            continue
        
        for days in days_included:
            if days in topic_date:
                flag = True
                break
            
        if not flag:
            continue

        for word in want_to_include:
            if word in title or word in description:
                message = f"## 📎{title}\n\n 링크 : {GEEKNEWS_BASEURL + topic_link}"
                messages.append(message)
                break

else:
    print(f"Error: {response.status_code}")

if len(messages) != 0:
    for message in messages:
        data = {"content": message}
        response = requests.post(DISCORD_URL, json=data)
messages.clear()
