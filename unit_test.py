#! usr/bin/env python3

import unittest
import sqlite3
from application import database_manager, scraper

"""
These first tests are for the database_manager module. We need the DB before scraping any data.
"""

class TestCreateDB(unittest.TestCase):
    '''
    Tests the function to create a DB in sqlite3 is working.
    We now have a database with nothing in it.
    '''

    def setUp(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.create_steam_reviews(db)

    def test(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            cur = db.cursor()
            response = cur.execute("SELECT 1 FROM steam_reviews LIMIT 1;")
            response_no_data = response.fetchone()
            assert response_no_data is None

    def tearDown(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.drop_steam_reviews(db)


class TestInsertOneData(unittest.TestCase):
    '''
    Tests we can insert one piece of data into this db.
    '''

    def setUp(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.create_steam_reviews(db)

    def test(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:

            url = 'url'
            app_num = 300000
            date_scraped = 'today'
            user_recommendation = 'great'
            user_review_text = 'great'
            user_name = 'Bob'
            classified = 0
            database_manager.insert_data_steam_reviews(db, url, app_num, date_scraped, classified, user_recommendation, user_review_text, user_name)

            cur = db.cursor()
            response = cur.execute("SELECT * FROM steam_reviews;")
            response_one_data = response.fetchone()
            assert response_one_data == (1, 'url', 300000, 'today', 0, 'great', 'great', 'Bob')

    def tearDown(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.drop_steam_reviews(db)


class TestInsertTwoData(unittest.TestCase):
    '''
    Tests we can insert two pieces of data into this db.
    '''

    def setUp(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.create_steam_reviews(db)

    def test(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:

            url = 'url'
            app_num = 300000
            date_scraped = 'today'
            user_recommendation = 'great'
            user_review_text = 'great'
            user_name = 'Bob'
            classified = 0
            database_manager.insert_data_steam_reviews(db, url, app_num, date_scraped, classified, user_recommendation, user_review_text, user_name)
            database_manager.insert_data_steam_reviews(db, url, app_num, date_scraped, classified, user_recommendation, user_review_text, user_name)

            cur = db.cursor()
            response = cur.execute("SELECT * FROM steam_reviews;")
            response_all_data = response.fetchall()
            assert response_all_data[0] == (1, 'url', 300000, 'today', 0, 'great', 'great', 'Bob')
            assert response_all_data[1] == (2, 'url', 300000, 'today', 0, 'great', 'great', 'Bob')

    def tearDown(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.drop_steam_reviews(db)


class TestRetrieveData(unittest.TestCase):
    '''
    Tests we can retrieve data from db.
    '''

    def setUp(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.create_steam_reviews(db)

    def test(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:

            url = 'url'
            app_num = 300000
            date_scraped = 'today'
            user_recommendation = 'Recommended'
            user_review_text = 'great'
            user_name = 'Bob'
            classified = 0
            database_manager.insert_data_steam_reviews(db, url, app_num, date_scraped, classified, user_recommendation, user_review_text, user_name)

            response = database_manager.retrieve_data_steam_reviews(db, 'Recommended', 0)
            assert response == (1, 'url', 300000, 'today', 0, 'Recommended', 'great', 'Bob')

    def tearDown(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.drop_steam_reviews(db)


class TestRetrieveDataFail1(unittest.TestCase):
    '''
    The previous test works, but this returns None because the WHERE condition in the function is false, 
    because of recommendation.
    '''

    def setUp(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.create_steam_reviews(db)

    def test(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:

            url = 'url'
            app_num = 300000
            date_scraped = 'today'
            user_recommendation = 'Not Recommended'
            user_review_text = 'great'
            user_name = 'Bob'
            classified = 0
            database_manager.insert_data_steam_reviews(db, url, app_num, date_scraped, classified, user_recommendation, user_review_text, user_name)

            response = database_manager.retrieve_data_steam_reviews(db, 'Recommended', 0)
            assert response is None

    def tearDown(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.drop_steam_reviews(db)


class TestRetrieveDataFail2(unittest.TestCase):
    '''
    The previous test works, but this returns None because the WHERE condition in the function is false, 
    because of categorised.
    '''

    def setUp(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.create_steam_reviews(db)

    def test(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:

            url = 'url'
            app_num = 300000
            date_scraped = 'today'
            user_recommendation = 'Recommended'
            user_review_text = 'great'
            user_name = 'Bob'
            classified = 1
            database_manager.insert_data_steam_reviews(db, url, app_num, date_scraped, classified, user_recommendation, user_review_text, user_name)

            response = database_manager.retrieve_data_steam_reviews(db, 'Recommended', 0)
            assert response is None

    def tearDown(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.drop_steam_reviews(db)


class TestRetrieveLastRow(unittest.TestCase):
    '''
    Tests we can retrieve the last row in the table. We need this as a record of what has been scraped.
    '''

    def setUp(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.create_steam_reviews(db)

    def test(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:

            database_manager.insert_data_steam_reviews(db, 'url_1', 300000, '2011-01-01', 0, 'Recommended', 'It was great', 'Destroyer')
            database_manager.insert_data_steam_reviews(db, 'url_2', 300020, '2011-01-01', 0, 'Not Recommended', 'It was bad', 'Dismantler')
            database_manager.insert_data_steam_reviews(db, 'url_3', 300025, '2011-01-01', 0, 'Recommended', 'OMG', 'Makiavelli')

            response = database_manager.retrieve_last_steam_reviews(db)
            assert response == (3, 'url_3', 300025, '2011-01-01', 0, 'Recommended', 'OMG', 'Makiavelli')

    def tearDown(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.drop_steam_reviews(db)



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
        assert scraper.get_recommendation_from_image_link(image_link_string) == 'Recommended'


class TestScraperDetectNotRecommended(unittest.TestCase):
    '''
    Each review has a link to a thumbs up or thumbs down. 
    Check a link to see it detect "Not recommended"
    '''

    def test(self):
        image_link_string = '<img height="40" src="http://store.akamai.steamstatic.com/public/shared/images/userreviews/icon_thumbsDown_v6.png" width="40"></img></div>'
        assert scraper.get_recommendation_from_image_link(image_link_string) == 'Not Recommended'


class TestScraperNoRecommendationDetected(unittest.TestCase):
    '''
    Each review has a link to a thumbs up or thumbs down. 
    Check to see a link not contain the data we need
    '''

    def test(self):
        image_link_string = '<img height="40" src="http://store.akamai.steamstatic.com/public/shared/images/userreviews/icon_thumbsSideways_v6.png" width="40"></img></div>'
        assert scraper.get_recommendation_from_image_link(image_link_string) == 'Issue detecting recommendation'


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
