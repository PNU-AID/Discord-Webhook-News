from html.parser import HTMLParser
from urllib.request import urlopen


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr, value in attrs:
                if attr == "href" and "/competitions/official/" in value:
                    self.hrefs.append(value)

    def handle_endtag(self, tag, attrs=None):
        pass

    def handle_data(self, data):
        pass


class TextParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)

    def handle_data(self, data):
        print(data.strip())


# 웹 페이지 불러오기
base_url = "http://www.dacon.io"
response = urlopen(base_url)
html_content = response.read().decode("utf-8")

parser = MyHTMLParser()
parser.feed(html_content)

for href in parser.hrefs:
    target_url = base_url + href
    print("Trying to fetch:", target_url)
    try:
        response = urlopen(target_url)
        html_content = response.read().decode("utf-8")
        text_parser = TextParser()
        text_parser.feed(html_content)
    except Exception as e:
        print("Failed to fetch:", target_url)
        print("Error:", e)
