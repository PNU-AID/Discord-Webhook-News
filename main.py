import os  # os모듈 불러오기 (운영체제와의 상호작용을 돕는 다양한 기능 제공 )

import requests  # requests모듈 불러오기(http, https 웹 사이트에 요청하기 위해 자주 사용되는 모듈)
from bs4 import (
    BeautifulSoup,  # 웹 데이터 크롤링 도는 스크래핑을 할 때 사용하는 python 라이브러리
)
from dotenv import load_dotenv  # .env 파일에서 환경 변수를 로드하는 라이브러리

load_dotenv(dotenv_path=".env")  # 현재 작업 디렉토리에 있는 .env 파일에서 환경 변수를 로드
DISCORD_URL = os.getenv("DISCORD_URL")  # os.getenv()는 함수는 지정된 환경 변수의 값을 반환하거나, 해당 환경 변수가 존재하지 않으면 None을 반환
GEEKNEWS_BASEURL = "https://news.hada.io/"  #
GEEKNEWS_URL = "https://news.hada.io/new"
want_to_include = ["AI", "ai", "ML", "GPT", "LLM", "Diffusion", "인공지능", "딥러닝", "머신러닝", "사전학습", "파인튜닝"]
days_included = [f"{i}분전" for i in range(1, 20)]


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

        if topic_title.a is None:
            title = topic_title.h1.string
        else:
            title = topic_title.a.h1.string
            # topic_link = topic_title.find("a")["href"].strip()

        description = ""
        if topic_content is not None:
            description = topic_content.a.string
            topic_link = topic_content.find("a")["href"].strip()
        else:
            topic_link = topic_title.find("a")["href"].strip()
        flag = False

        if topic_url.string is None:
            continue

        for days in days_included:
            if days == topic_date:
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
        if response.status_code == 404:
            print("response code is 404, check discord url or action variable")
