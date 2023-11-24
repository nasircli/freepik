from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time
import traceback

app = FastAPI()

# Mount the "static" folder to "/static" URL
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates configuration
templates = Jinja2Templates(directory="templates")

def handle_http_error(response, url):
    if response.status_code == 403:
        print(f'Error 403: Access forbidden for URL: {url}')
    elif response.status_code == 404:
        print(f'Error 404: URL not found: {url}')
    else:
        print(f'HTTP Error: {response.status_code} - {response.text}')

def handle_request_exception(e):
    print(f'Error: {e}')

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
        handle_http_error(response, url)
    except requests.exceptions.RequestException as e:
        handle_request_exception(e)

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
        handle_http_error(response, main_url)
    except requests.exceptions.RequestException as e:
        handle_request_exception(e)

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/crawl")
async def crawl(request: Request, mainInput: str = Form(...)):
    tag_selector = '.showcase .showcase__item.showcase__item--buttons .showcase__thumbnail .tags-container ul.tags>li>.tag-item'

    try:
        crawled_data = get_crawled_data(mainInput, tag_selector)
        return templates.TemplateResponse("index.html", {"request": request, "crawled_data": crawled_data})
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(traceback.format_exc())  # Print the traceback
        return templates.TemplateResponse("index.html", {"request": request, "error_message": error_message})
