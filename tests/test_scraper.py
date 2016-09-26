#! usr/bin/env python3

import os
import sys
import unittest
import sqlite3
import atexit

# Here we're moving the context into the parent folder
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)

from application import database_manager
from application import scraper

from archive import data_prep
from archive import train_classify_data

from sklearn.feature_extraction.text import TfidfVectorizer

@atexit.register
def goodbye():
    try:
        os.remove('database_test.db')
    except FileNotFoundError:
        pass

"""
These tests check the scraper is taking content down from the web as it should.
"""

class TestScrapeOneGamePage(unittest.TestCase):
    '''
    Tests the scraper fetches a page and passes it to HTML with BeautifulSoup.
    Tests Beautiful Soup passes our data to an object for use.
    A BS object will have a title and body attribute.
    '''

    def test(self):
        request_response = scraper.scrape_app_page('http://store.steampowered.com/app/', 334190)
        assert hasattr(request_response, 'title')
        assert hasattr(request_response, 'body')


class TestScrapedPageHasReviews(unittest.TestCase):
    '''
    The only pages we're interested in are those that have reviews.
    So we need a function to test if the page has a review.
    This page certainly does have them.
    '''

    def test(self):
        request_response = scraper.scrape_app_page('http://store.steampowered.com/app/', 80)
        assert scraper.page_has_reviews(request_response) == True


class TestScrapedPageHasNoReviews(unittest.TestCase):
    '''
    When an invalid request is made, Steam sends us to a different page, these pages won't have reviews.
    Check reviews are missing    
    '''

    def test(self):
        request_response = scraper.scrape_app_page('http://store.steampowered.com/app/', 's')
        assert scraper.page_has_reviews(request_response) == False


class TestScraperGetAllReviews(unittest.TestCase):
    '''
    Get all reviews on this page and put those in an array, we'll need them later.
    '''

    def test(self):
        request_response = scraper.scrape_app_page('http://store.steampowered.com/app/', 500)
        reviews = scraper.get_reviews_on_page(request_response)
        assert len(reviews) > 0


class TestScraperDetectRecommended(unittest.TestCase):
    '''
    Each review has a link to a thumbs up or thumbs down. 
    Check a link to see it detect "Recommended"
    '''

    def test(self):
        image_link_string = '<img height="40" src="http://store.akamai.steamstatic.com/public/shared/images/userreviews/icon_thumbsUp_v6.png" width="40"></img></div>'
        assert scraper.get_image_link_recommendation(image_link_string) == 'Recommended'


class TestScraperDetectNotRecommended(unittest.TestCase):
    '''
    Each review has a link to a thumbs up or thumbs down. 
    Check a link to see it detect "Not recommended"
    '''

    def test(self):
        image_link_string = '<img height="40" src="http://store.akamai.steamstatic.com/public/shared/images/userreviews/icon_thumbsDown_v6.png" width="40"></img></div>'
        assert scraper.get_image_link_recommendation(image_link_string) == 'Not Recommended'


class TestScraperNoRecommendationDetected(unittest.TestCase):
    '''
    Each review has a link to a thumbs up or thumbs down. 
    Check to see a link not contain the data we need
    '''

    def test(self):
        image_link_string = '<img height="40" src="http://store.akamai.steamstatic.com/public/shared/images/userreviews/icon_thumbsSideways_v6.png" width="40"></img></div>'
        assert scraper.get_image_link_recommendation(image_link_string) == 'Issue detecting recommendation'


class TestScraperReviewFormatting(unittest.TestCase):
    '''
    Test scraper is returning the data from each box that we need
    '''

    def test(self):
        request_response = scraper.scrape_app_page('http://store.steampowered.com/app/', 500)
        reviews = scraper.get_reviews_on_page(request_response)

        assert len(reviews[0]['user_recommendation']) > 0
        assert len(reviews[0]['user_review_text']) > 0
        assert len(reviews[0]['user_name']) > 0


if __name__ == '__main__':
    unittest.main()
