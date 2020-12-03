import requests
from lxml import html
import os
from datetime import date

HOME_URL = 'https://www.larepublica.co/'

# XPATHs
XPATH_ARTICLE_LINK = '//h2/a/@href'
# XPATH_ARTICLE_TITLE = '//div[@class="row OpeningPostNormal"]/div/div/h2/a/text()'
XPATH_ARTICLE_TITLE = '//div[@class="container title-share"]/div/div/h2/a/text()'
XPATH_ARTICLE_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_ARTICLE_BODY = '//div[@class="html-content"]/p/text()'

TODAY = date.today().strftime('%Y-%m-%d')


def _parse_html(html_content):
    encoded_content = html_content.decode('utf-8')
    return html.fromstring(encoded_content)


def _write_article_file(title, summary, body):
    try:
        with open(f'{TODAY}/{title}.txt', 'w', encoding='utf-8') as f:
            f.write(title)
            f.write('\n\n')
            f.write(summary)
            f.write(title)
            f.write('\n\n')
            for p in body:
                f.write(p)
                f.write('\n')
    except Exception as e:
        print(e)


def parse_article(link):
    print(f'Parsing... {link}')
    try:
        response = requests.get(link)
        if response.ok:
            article = _parse_html(response.content)

            try:
                title = article.xpath(XPATH_ARTICLE_TITLE)[0]
                print(f'Title: {title}')

                summary = article.xpath(XPATH_ARTICLE_SUMMARY)
                print(f'Summary: {summary}')

                body = article.xpath(XPATH_ARTICLE_BODY)
                print(f'Body: {body}')

            except IndexError as e:
                print(f"Error processing xpath: {e}")
                return

            _write_article_file(title, summary, body)
            print(f'File written succesfully... {link}')
        else:
            raise ValueError(f'Error requesting link: {response.status_code}')
    except ValueError as e:
        print(e)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.ok:
            home = _parse_html(response.content)
            article_links = home.xpath(XPATH_ARTICLE_LINK)

            if not os.path.isdir(TODAY):
                os.mkdir(TODAY)

            for link in article_links:
                parse_article(link)

        else:
            raise ValueError(
                    f'Error requesting homepage: {response.status_code}')
    except ValueError as e:
        print(e)


def run():
    parse_home()


if __name__ == '__main__':
    run()
