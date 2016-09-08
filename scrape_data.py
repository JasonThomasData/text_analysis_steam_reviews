#! usr/bin/env python3

#Note, exit this script with ctrl+c from terminal, never ctrl+z, or you risk a db lock.

import sqlite3, datetime, time
from application import database_manager, scraper

db_location = 'database_steam_reviews.db'
db = sqlite3.connect(db_location, timeout=20)

database_manager.create_steam_reviews(db)

last_record = database_manager.retrieve_last_steam_reviews(db)

if last_record is None:
    last_app_num = 300000
else:
    last_app_num = last_record[2]

while(True):

    """
    This process of scraping Steam continues until it is disrupted.
    """

    time.sleep(1) #This is mearly a consideration for Steam, as to not burden their servers

    last_app_num += 5

    base_url = 'http://store.steampowered.com/app/'

    content_from_steam = scraper.scrape_app_page(base_url, last_app_num)
    date_scraped = datetime.datetime.now()

    if scraper.page_has_reviews(content_from_steam) == True:
        reviews_on_page = scraper.get_reviews_on_page(content_from_steam)
        print('Found %s reviews for app number %s' %(len(reviews_on_page), last_app_num))
    else:
        reviews_on_page = []
        print('No review element found for number %s' %(last_app_num))

    for review in reviews_on_page:
        url = '%s%s/' %(base_url, last_app_num)
        classified = 0
        user_recommendation = review['user_recommendation']
        user_review_text = review['user_review_text']
        user_name = review['user_name']

        database_manager.insert_data_steam_reviews(db, url, last_app_num, date_scraped, classified, user_recommendation, user_review_text, user_name)
