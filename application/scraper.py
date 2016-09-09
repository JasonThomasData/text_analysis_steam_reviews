#! usr/bin/env python3

import requests
from bs4 import BeautifulSoup


def scrape_app_page(base_url, app_num):
    '''
    Fetches page and parses it to an HTML tree. 
    BeautifulSoup will always receive valid html, since Steam will redirect the user on an invalid request.
    '''

    url_to_scrape = '%s%s/' %(base_url, app_num)
    r = requests.get(url_to_scrape)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup


def page_has_reviews(html_from_page):
    '''
    Makes sure the page contains reviews.
    '''

    review_header = html_from_page.find('div', {'class': 'user_reviews_header'})
    if review_header is not None:
        return True
    return False


def get_recommendation_from_image_link(image_div_string):
    '''
    Check the image link to see if the image is thumbs up or thumbs down.
    If it's thumbs up, then that's a good review. THumbs down images are loaded into bad review divs.
    '''

    if 'thumbsUp' in image_div_string:
        return 'Recommended'
    elif 'thumbsDown' in image_div_string:
        return 'Not Recommended'
    return 'Issue detecting recommendation'


def string_parser(soup_to_parse):
    all_text_in_elem = soup_to_parse.find_all(text=True)
    string_of_all_text = ' '.join(all_text_in_elem).strip()
    return string_of_all_text


def remove_duplicates(review_data):
    '''
    The intention here is to convert each dict to a tuple, so we can use set() to remove duplicates.
    Dictionaries are not hashable, which is a requirement of the set() function.
    '''

    seen = set()
    indeces_of_duplicates = []

    #find the indices of duplicate dicts
    for i, data in enumerate(review_data):
        tuple_of_dict = tuple(data.items())
        if tuple_of_dict not in seen:
            seen.add(tuple_of_dict)
        else:
            indeces_of_duplicates.append(i)

    #go through original list of dicts backwards and remove those.
    for i in sorted(indeces_of_duplicates, reverse=True):
            del review_data[i]

    return review_data


def get_reviews_on_page(html_from_page):
    '''
    For each review, turn that into a dict, and place in an array of dicts
    This should be accessed once the app has verified the page has reviews on it.
    '''

    review_data = []
    review_boxes = html_from_page.find_all('div', {'class': 'review_box'})

    for one_review in review_boxes:

        image_div = one_review.find('div', {'class': 'thumb'})
        image_div_string = str(image_div)

        user_recommendation = get_recommendation_from_image_link(image_div_string)
        user_review_text = one_review.find('div', {'class': 'content'})
        user_name = one_review.find('div', {'class': 'persona_name'})

        data_for_one_review = {
            "user_recommendation": user_recommendation,
            "user_review_text": string_parser(user_review_text),
            "user_name": string_parser(user_name)
        }

        review_data.append(data_for_one_review)

    review_data_unique = remove_duplicates(review_data)
    return review_data_unique