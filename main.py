import os  # 운영체제와의 상호작용을 돕는 다양한 기능 제공

import requests  # http, https 웹 사이트에 요청하기 위해 자주 사용되는 모듈
from bs4 import (
    BeautifulSoup,  # 웹 데이터 크롤링 도는 스크래핑을 할 때 사용하는 python 라이브러리
)
from dotenv import load_dotenv  # .env 파일에서 환경 변수를 로드하는 라이브러리

load_dotenv(dotenv_path=".env")  # 현재 작업 디렉토리에 있는 .env 파일에서 환경 변수를 로드

DISCORD_URL = os.getenv("DISCORD_URL")  # os.getenv()는 함수는 지정된 환경 변수의 값을 반환하거나, 해당 환경 변수가 존재하지 않으면 None을 반환
GEEKNEWS_BASEURL = "https://news.hada.io/"
GEEKNEWS_URL = "https://news.hada.io/new"
want_to_include = ["AI", "ai", "ML", "GPT", "LLM", "Diffusion", "인공지능", "딥러닝", "머신러닝", "사전학습", "파인튜닝"] # AI 관련 뉴스인지 판단하기 위한 지표
days_included = [f"{i}시간전" for i in range(1, 23)] # 24시간 내 뉴스인지 확인

headers = {"Content-Type": "application/json"}
messages = []

response = requests.get(GEEKNEWS_URL)
if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    topics = soup.find_all("div", class_="topic_row")
    
    for topic in topics:
        # 뉴스 내 tag 지정
        topic_title = topic.find("div", class_="topictitle") # 뉴스 제목
        topic_content = topic.find("div", class_="topicdesc") # 뉴스 내용
        topic_url = topic.find("span", class_="topicurl") # 뉴스 링크
        topic_info = topic.find("div", class_="topicinfo") # 뉴스 정보
        
        # 뉴스 제목 추출 
        if topic_title.a is None:
            title = topic_title.h1.string
        else:
            title = topic_title.a.h1.string
            # topic_link = topic_title.find("a")["href"].strip()
        
        # 뉴스 내용 추출
        description = ""
        if topic_content is not None:
            description = topic_content.a.string
            topic_link = topic_content.find("a")["href"].strip()
        else:
            topic_link = topic_title.find("a")["href"].strip()

        # 뉴스 url이 없으면 건너뀜
        if topic_url.string is None:
            continue

        # 뉴스 날짜 추출해서 24시간 내 내용인지 확인
        date_flag = False
        topic_date = topic_info.text.split(" ")[4]
        for days in days_included:
            if days == topic_date:
                date_flag = True
                break
            
        # 24시간이 지난 뉴스는 건너뜀
        if not date_flag:
            continue

        # AI 관련 뉴스인지 확인
        for word in want_to_include:
            if word in title or word in description:
                message = f"## 📎{title}\n\n 링크 : {GEEKNEWS_BASEURL + topic_link}"
                messages.append(message)
                break
else:
    print(f"Error: {response.status_code}")

# 디스코드 전송
if len(messages) != 0:
    for message in messages:
        data = {"content": message}
        response = requests.post(DISCORD_URL, json=data)
        # print(message)
        if response.status_code == 404:
            print("response code is 404, check discord url or action variable")
