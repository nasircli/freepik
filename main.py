from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time

app = Flask(__name__)

def get_tags_from_url(url, tag_selector):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        with requests.Session() as session:
            response = session.get(url, headers=headers)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        tags = [tag_element.get_text(strip=True) for tag_element in soup.select(tag_selector)]
        return tags
    except requests.exceptions.HTTPError as e:
        if response.status_code == 403:
            print(f'Error 403: Access forbidden for URL: {url}')
        elif response.status_code == 404:
            print(f'Error 404: URL not found: {url}')
        else:
            print(f'HTTP Error: {response.status_code} - {e}')
        return None
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        return None

def get_crawled_data(main_input, tag_selector):
    try:
        parsed_url = urlparse(main_input)
        if parsed_url.scheme and parsed_url.netloc:
            main_url = main_input
        else:
            keyword = main_input.replace(' ', '-')
            main_url = f'https://www.freepik.com/free-photos-vectors/{keyword}'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        with requests.Session() as session:
            response = session.get(main_url, headers=headers)
            response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        main_tags = get_tags_from_url(main_url, tag_selector)

        unique_tags = set(main_tags)

        if main_tags:
            print('-' * 50)
            print('BEST TAGS FOR: - {}:'.format(main_url))
            print(', '.join(main_tags))
            print('-' * 50)

        links = [urljoin(main_url, link['href']) for link in soup.select('body.new-resource-list .filter-tags-row .tag-slider--list li a, body.new-resource-list .no-results--popular .tag-slider--list li a')]

        for link in links:
            tags = get_tags_from_url(link, tag_selector)
            if tags:
                unique_tags.update(tags)
                time.sleep(1)

        return list(unique_tags)

    except requests.exceptions.HTTPError as e:
        if response.status_code == 403:
            print(f'Error 403: Access forbidden for URL: {main_url}')
        elif response.status_code == 404:
            print(f'Error 404: URL not found: {main_url}')
        else:
            print(f'HTTP Error: {response.status_code} - {e}')
        return None
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/crawl', methods=['POST'])
def crawl():
    main_input = request.form['mainInput']
    tag_selector = '.showcase .showcase__item.showcase__item--buttons .showcase__thumbnail .tags-container ul.tags>li>.tag-item'

    try:
        crawled_data = get_crawled_data(main_input, tag_selector)
        return render_template('result.html', crawled_data=crawled_data)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return render_template('result.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
