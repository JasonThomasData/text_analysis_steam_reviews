#! usr/bin/env python3

import sqlite3

def create_reviews_table(db):
    cur = db.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS steam_reviews (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT, app_num INTEGER, date_scraped TEXT, classified INTEGER, user_recommendation TEXT, user_review_text TEXT, user_name TEXT);')

def drop_reviews_table(db):
    cur = db.cursor()
    cur.execute('DROP TABLE steam_reviews;')

def insert_data_reviews_table(db, url, app_num, date_scraped, classified, user_recommendation, user_review_text, user_name):
    cur = db.cursor()
    query = "INSERT INTO steam_reviews (url, app_num, date_scraped, classified, user_recommendation, user_review_text, user_name) VALUES (?,?,?,?,?,?,?);"
    data = (url, app_num, date_scraped, classified, user_recommendation, user_review_text, user_name)
    cur.execute(query, data)

def retrieve_data_reviews_table(db, user_recommendation, classified):
    cur = db.cursor()
    query = "SELECT * FROM steam_reviews WHERE user_recommendation=? AND classified=?;"
    data = (user_recommendation, classified)
    cur.execute(query, data)
    return cur.fetchone()

def retrieve_last_reviews_table(db):
    cur = db.cursor()
    query = "SELECT * FROM steam_reviews ORDER BY id DESC LIMIT 1;"
    cur.execute(query)
    return cur.fetchone()
