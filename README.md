# 인공지능 관련 뉴스 전달 (Discord Webhook)

> 이 스크립트는 **[GeekNews](https://news.hada.io/new) 페이지**에서 AI 관련 뉴스를 스크래핑하여 Discord Webhook을 통해 특정 Discord 채널로 알림을 전송합니다.

## 기능

- Git Actions을 통해 매일 오전 10시에 main.py 실행
- Python 라이브러리인 BeautifulSoup를 사용하여 GeekNews에서 24시간 이내 올라온 뉴스 확인
- 뉴스 내용 중에 AI 관련 용어가 포함되었는지 확인 후 스크래핑
- 뉴스 제목과 링크를 Discord로 전송

## 사용 방법

1. .env 파일 생성

```bash
DISCORD_URL=<YOUR_DISCORD_WEB_HOOK_URL>
```

2. 요구사항 설치

```bash
pip intsall -r requirments.txt
```

## 출력 예시

```
## 📎Flash AID - LLM을 모든 파이프라인에 연동하기

 링크 : https://news.hada.io/topic?id=12345
## 📎Open-AID: LLM으로 컴퓨터를 제어하기

 링크 : https://news.hada.io/topic?id=67890
## 📎Show AID: AID AI - 반응형 GPT 웹 인터페이스

 링크 : https://news.hada.io/topic?id=00000
```
