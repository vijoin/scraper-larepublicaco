import requests
from lxml import html

HOME_URL = 'https://www.larepublica.co/'

# XPATHs
XPATH_ARTICLE_LINK = '//h2/a/@href'
XPATH_ARTICLE_TITLE = '//div[@class="row OpeningPostNormal"]/div/div/h2/a/text()'
XPATH_ARTICLE_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_ARTICLE_BODY = '//div[@class="html-content"]/p/text()'


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.ok:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            article_links = parsed.xpath(XPATH_ARTICLE_LINK)
            print(article_links)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as e:
        print(e)


def run():
    parse_home()


if __name__ == '__main__':
    run()