#! usr/bin/env python3

import requests
from bs4 import BeautifulSoup


def scrape_app_page(base_url, app_num):
    """
    Fetches page and parses it to an HTML tree. 
    BeautifulSoup will always receive valid html, since Steam will redirect the user on an invalid request.
    """

    url_to_scrape = '%s%s/' %(base_url, app_num)
    r = requests.get(url_to_scrape)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup

def page_has_reviews(html_from_page):
    """
    Makes sure the page contains reviews.
    """

    review_header = html_from_page.find('div', {'class': 'user_reviews_header'})
    if review_header is not None:
        return True
    return False