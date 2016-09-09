#! usr/bin/env python3

import unittest, sqlite3, os, atexit
from application import database_manager, scraper, data_prep


@atexit.register
def goodbye():
    try:
        print('Tests done, removing database_test.db')
        os.remove('database_test.db')
    except FileNotFoundError:
        pass

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


class TestRetrieveDataOne(unittest.TestCase):
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

            response = database_manager.retrieve_steam_reviews(db, 'Recommended', 0, 1)
            assert response[0] == (1, 'url', 300000, 'today', 0, 'Recommended', 'great', 'Bob')

    def tearDown(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.drop_steam_reviews(db)


class TestRetrieveDataOneFail1(unittest.TestCase):
    '''
    The previous test works, but this returns len(response) == 0 because the WHERE condition in the function is false, 
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

            response = database_manager.retrieve_steam_reviews(db, 'Recommended', 0, 1)
            assert len(response) == 0

    def tearDown(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.drop_steam_reviews(db)


class TestRetrieveDataOneFail2(unittest.TestCase):
    '''
    The first of these tests works, but this returns len(response) == 0 because the WHERE condition in the function is false, 
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

            response = database_manager.retrieve_steam_reviews(db, 'Recommended', 0, 1)
            assert len(response) == 0

    def tearDown(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.drop_steam_reviews(db)


class TestRetrieveDataBatch1(unittest.TestCase):
    '''
    Test batch retrieval of data from db.    
    '''

    def setUp(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.create_steam_reviews(db)

    def test(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:

            database_manager.insert_data_steam_reviews(db, 'url_1', 300000, '2011-01-01', 0, 'Not Recommended', 'It was great', 'Destroyer')
            database_manager.insert_data_steam_reviews(db, 'url_2', 300020, '2011-01-01', 0, 'Not Recommended', 'It was bad', 'Dismantler')
            database_manager.insert_data_steam_reviews(db, 'url_3', 300025, '2011-01-01', 0, 'Not Recommended', 'OMG', 'Makiavelli')
            database_manager.insert_data_steam_reviews(db, 'url_4', 300040, '2011-01-01', 0, 'Not Recommended', 'I want to cry myself to sleep', 'GiveMeSugar')
            database_manager.insert_data_steam_reviews(db, 'url_5', 300040, '2011-01-01', 0, 'Not Recommended', 'When I get out of this padded cell I will bake a cake', 'Sluggish666')
            database_manager.insert_data_steam_reviews(db, 'url_6', 300000, '2011-01-01', 0, 'Recommended', 'It was great', 'Destroyer')
            database_manager.insert_data_steam_reviews(db, 'url_7', 300020, '2011-01-01', 0, 'Recommended', 'It was bad', 'Dismantler')
            database_manager.insert_data_steam_reviews(db, 'url_8', 300025, '2011-01-01', 0, 'Recommended', 'OMG', 'Makiavelli')
            database_manager.insert_data_steam_reviews(db, 'url_9', 300040, '2011-01-01', 0, 'Recommended', 'I want to cry myself to sleep', 'GiveMeSugar')
            database_manager.insert_data_steam_reviews(db, 'url_10', 300040, '2011-01-01', 0, 'Recommended', 'When I get out of this padded cell I will bake a cake', 'Sluggish666')

            response = database_manager.retrieve_steam_reviews(db, 'Not Recommended', 0, 3)
            assert len(response) == 3

    def tearDown(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.drop_steam_reviews(db)


class TestRetrieveDataBatch2(unittest.TestCase):
    '''
    Test batch retrieval of data from db.    
    '''

    def setUp(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.create_steam_reviews(db)

    def test(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:

            database_manager.insert_data_steam_reviews(db, 'url_1', 300000, '2011-01-01', 0, 'Not Recommended', 'It was great', 'Destroyer')
            database_manager.insert_data_steam_reviews(db, 'url_2', 300020, '2011-01-01', 0, 'Not Recommended', 'It was bad', 'Dismantler')
            database_manager.insert_data_steam_reviews(db, 'url_3', 300025, '2011-01-01', 0, 'Not Recommended', 'OMG', 'Makiavelli')
            database_manager.insert_data_steam_reviews(db, 'url_4', 300040, '2011-01-01', 0, 'Not Recommended', 'I want to cry myself to sleep', 'GiveMeSugar')
            database_manager.insert_data_steam_reviews(db, 'url_5', 300040, '2011-01-01', 0, 'Not Recommended', 'When I get out of this padded cell I will bake a cake', 'Sluggish666')
            database_manager.insert_data_steam_reviews(db, 'url_6', 300000, '2011-01-01', 0, 'Recommended', 'It was great', 'Destroyer')
            database_manager.insert_data_steam_reviews(db, 'url_7', 300020, '2011-01-01', 0, 'Recommended', 'It was bad', 'Dismantler')
            database_manager.insert_data_steam_reviews(db, 'url_8', 300025, '2011-01-01', 0, 'Recommended', 'OMG', 'Makiavelli')
            database_manager.insert_data_steam_reviews(db, 'url_9', 300040, '2011-01-01', 0, 'Recommended', 'I want to cry myself to sleep', 'GiveMeSugar')
            database_manager.insert_data_steam_reviews(db, 'url_10', 300040, '2011-01-01', 0, 'Recommended', 'When I get out of this padded cell I will bake a cake', 'Sluggish666')

            response = database_manager.retrieve_steam_reviews(db, 'Recommended', 0, 7)
            assert len(response) == 5

    def tearDown(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.drop_steam_reviews(db)


class TestRetrieveDataBatch3(unittest.TestCase):
    '''
    Test batch retrieval of data from db.    
    '''

    def setUp(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.create_steam_reviews(db)

    def test(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:

            database_manager.insert_data_steam_reviews(db, 'url_1', 300000, '2011-01-01', 0, 'Not Recommended', 'It was great', 'Destroyer')
            database_manager.insert_data_steam_reviews(db, 'url_2', 300020, '2011-01-01', 0, 'Not Recommended', 'It was bad', 'Dismantler')
            database_manager.insert_data_steam_reviews(db, 'url_3', 300025, '2011-01-01', 0, 'Not Recommended', 'OMG', 'Makiavelli')
            database_manager.insert_data_steam_reviews(db, 'url_4', 300040, '2011-01-01', 0, 'Not Recommended', 'I want to cry myself to sleep', 'GiveMeSugar')
            database_manager.insert_data_steam_reviews(db, 'url_5', 300040, '2011-01-01', 0, 'Not Recommended', 'When I get out of this padded cell I will bake a cake', 'Sluggish666')
            database_manager.insert_data_steam_reviews(db, 'url_6', 300000, '2011-01-01', 0, 'Recommended', 'It was great', 'Destroyer')
            database_manager.insert_data_steam_reviews(db, 'url_7', 300020, '2011-01-01', 0, 'Recommended', 'It was bad', 'Dismantler')
            database_manager.insert_data_steam_reviews(db, 'url_8', 300025, '2011-01-01', 0, 'Recommended', 'OMG', 'Makiavelli')
            database_manager.insert_data_steam_reviews(db, 'url_9', 300040, '2011-01-01', 0, 'Recommended', 'I want to cry myself to sleep', 'GiveMeSugar')
            database_manager.insert_data_steam_reviews(db, 'url_10', 300040, '2011-01-01', 0, 'Recommended', 'When I get out of this padded cell I will bake a cake', 'Sluggish666')

            response = database_manager.retrieve_steam_reviews(db, 'Recommended', 0, 2)
            assert len(response) == 2

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


class TestDeleteDuplicatesInDB(unittest.TestCase):
    '''
    Tests duplicate rows in the DB will be deleted.
    Some pages will have double-ups of the same review, we need to delete those.
    '''

    def setUp(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.create_steam_reviews(db)

    def test(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:

            database_manager.insert_data_steam_reviews(db, 'url_1', 300000, '2011-01-01', 0, 'Recommended', 'It was great', 'Destroyer')
            database_manager.insert_data_steam_reviews(db, 'url_1', 300000, '2011-01-01', 0, 'Recommended', 'It was great', 'Destroyer')
            database_manager.insert_data_steam_reviews(db, 'url_1', 300000, '2011-01-01', 0, 'Recommended', 'It was great', 'Destroyer')
            database_manager.remove_duplicates_steam_reviews(db)

            cur = db.cursor()
            response = cur.execute("SELECT * FROM steam_reviews WHERE app_num = 300000;")

    def tearDown(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.drop_steam_reviews(db)


class TestScraperDeleteDuplicateReviews(unittest.TestCase):
    '''
    Tests duplicate reviews in the DB will be deleted.
    Some pages will have double-ups of the same review, we need to delete those.
    This test has two duplicates.
    '''

    def test(self):
        list_of_reviews = [
            {
                'user_recommendation': 'Recommended',
                'user_review_text': 'It is great',
                'user_name': 'bahumbug'
            },
            {
                'user_recommendation': 'Recommended',
                'user_review_text': 'It is great',
                'user_name': 'bahumbug'
            },
            {
                'user_recommendation': 'Not Recommended',
                'user_review_text': 'This is the worst thing that has ever happened.',
                'user_name': 'WhatYouWantSonny'
            },
            {
                'user_recommendation': 'Recommended',
                'user_review_text': 'DAMN BUY THIS GAME',
                'user_name': 'pimplePopper61'
            },
            {
                'user_recommendation': 'Not Recommended',
                'user_review_text': 'This is the worst thing that has ever happened.',
                'user_name': 'WhatYouWantSonny'
            }
        ]

        reviews_no_duplicates = scraper.remove_duplicates(list_of_reviews)
        assert len(reviews_no_duplicates) == 3

        try:
            assert reviews_no_duplicates[0]['user_recommendation'] == 'Recommended'
            assert reviews_no_duplicates[1]['user_recommendation'] == 'Not Recommended'
        except TypeError:
            assert False #this means the responses are not dicts, which means this fails

"""
These tests are for the data_prep module.
"""

class TestDataPrepRetrieveEqual(unittest.TestCase):
    '''
    Tests the function that retrieves an equal number of 'Recommended' and 'Not Recommended' reviews.
    '''

    def setUp(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.create_steam_reviews(db)
            database_manager.insert_data_steam_reviews(db, 'url_1', 300000, '2011-01-01', 0, 'Not Recommended', 'It was great', 'Destroyer')
            database_manager.insert_data_steam_reviews(db, 'url_2', 300020, '2011-01-01', 0, 'Not Recommended', 'It was bad', 'Dismantler')
            database_manager.insert_data_steam_reviews(db, 'url_3', 300025, '2011-01-01', 0, 'Not Recommended', 'OMG', 'Makiavelli')
            database_manager.insert_data_steam_reviews(db, 'url_4', 300040, '2011-01-01', 0, 'Not Recommended', 'I want to cry myself to sleep', 'GiveMeSugar')
            database_manager.insert_data_steam_reviews(db, 'url_5', 300040, '2011-01-01', 0, 'Not Recommended', 'When I get out of this padded cell I will bake a cake', 'Sluggish666')
            database_manager.insert_data_steam_reviews(db, 'url_6', 300000, '2011-01-01', 0, 'Recommended', 'It was great', 'Destroyer')
            database_manager.insert_data_steam_reviews(db, 'url_7', 300020, '2011-01-01', 0, 'Recommended', 'It was bad', 'Dismantler')
            database_manager.insert_data_steam_reviews(db, 'url_8', 300025, '2011-01-01', 0, 'Recommended', 'OMG', 'Makiavelli')
            database_manager.insert_data_steam_reviews(db, 'url_9', 300040, '2011-01-01', 0, 'Recommended', 'I want to cry myself to sleep', 'GiveMeSugar')
            database_manager.insert_data_steam_reviews(db, 'url_10', 300040, '2011-01-01', 0, 'Recommended', 'When I get out of this padded cell I will bake a cake', 'Sluggish666')


    def test(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            recommended_reviews, not_recommended_reviews = data_prep.retrieve_reviews_balanced(db, 4)
            assert len(recommended_reviews) == 2
            assert len(not_recommended_reviews) == 2
            assert not_recommended_reviews[0][5] == 'Not Recommended'
            assert not_recommended_reviews[1][5] == 'Not Recommended'
            assert recommended_reviews[0][5] == 'Recommended'
            assert recommended_reviews[1][5] == 'Recommended'

    def tearDown(self):
        db_location = 'database_test.db'
        with sqlite3.connect(db_location, timeout=20) as db:
            database_manager.drop_steam_reviews(db)


class TestDataPrepFormListsForTraining(unittest.TestCase):
    '''
    Tests the function that splits the lists of Recommended and Not Recommended reviews and combines
    them into a list of training_data (large) and test_data (size equal to interval).
    Both are equally formed of 'Recommended' and 'Not Recommended'
    '''

    def test(self):
        recommended_reviews = ['Recommeded review'] * 300
        not_recommended_reviews = ['Not recommeded review'] * 300
        interval = 100

        training_data, test_data = data_prep.form_training_test_lists(recommended_reviews, not_recommended_reviews, interval)

        assert len(training_data) == 500
        assert len(test_data) == 100


class TestDataPrepTransposeLists(unittest.TestCase):
    '''
    Tests our data is transposed as expected.
    '''

    def test(self):
        training_data = [('row id', 'url_10', 300040, '2011-01-01', 0, 'Recommended', 'It was great', 'Sluggish666')] * 100
        testing_data = [('row id', 'url', 300000, '2011-01-01', 0, 'Not Recommended', 'It was bad', 'Destroyer')] * 100

        training_data_transposed, testing_data_transposed = data_prep.transpose_data(training_data, testing_data)

        assert training_data_transposed[5][20] == 'Recommended'
        assert training_data_transposed[6][40] == 'It was great'
        assert training_data_transposed[5][50] == 'Recommended'
        assert testing_data_transposed[5][60] == 'Not Recommended'
        assert testing_data_transposed[6][70] == 'It was bad'
        assert testing_data_transposed[5][80] == 'Not Recommended'

class TestDataPrepExtractClasses(unittest.TestCase):
    '''
    Tests our training_data_classes and testing_data_classes are returned as expected.
    '''

    def test(self):
        training_data = [('row id', 'url_10', 300040, '2011-01-01', 0, 'Recommended', 'It was great', 'Sluggish666')] * 100
        testing_data = [('row id', 'url', 300000, '2011-01-01', 0, 'Not Recommended', 'It was bad', 'Destroyer')] * 100

        training_data_transposed, testing_data_transposed = data_prep.transpose_data(training_data, testing_data)

        training_data_classes, testing_data_classes = data_prep.extract_classes(training_data_transposed, testing_data_transposed)

        assert len(training_data_classes) == 100
        assert len(testing_data_classes) == 100


class TestDataPrepExtractClasses(unittest.TestCase):
    '''
    Tests our training_data_documents and testing_data_documents are returned as expected.
    '''

    def test(self):
        training_data = [('row id', 'url_10', 300040, '2011-01-01', 0, 'Recommended', 'It was great', 'Sluggish666')] * 100
        testing_data = [('row id', 'url', 300000, '2011-01-01', 0, 'Not Recommended', 'It was bad', 'Destroyer')] * 100

        training_data_transposed, testing_data_transposed = data_prep.transpose_data(training_data, testing_data)

        training_data_documents, testing_data_documents = data_prep.extract_reviews(training_data_transposed, testing_data_transposed)

        assert len(training_data_documents) == 100
        assert len(testing_data_documents) == 100


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

