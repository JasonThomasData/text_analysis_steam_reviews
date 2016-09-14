#!/usr/bin/python3

import sys

from application import scraper, database_manager, train_classify_data

if int(sys.version_info.major) < 3:
    sys.stdout.write('You must use Python3 with this program, exiting... \n')
    sys.exit()


def inputs_feedback():
    feedback = '''
    Wrong number of inputs. These are valid:
    - python3 run_app.py scrape_reviews continue OR
    - python3 run_app.py scrape_reviews new OR
    - python3 run_app.py classify_data OR
    - python3 run_app.py make_report OR
    '''

    return feedback


def process_inputs(inputs):
    '''
    Check the inputs are valid and load the appropriate functions.
    '''

    db_location = 'database_steam_reviews.db'
    input_length = len(inputs)

    if inputs[1] == 'scrape_reviews':
        if input_length == 2:
            scraper.get_reviews(db_location)
        elif inputs[2] == 'continue':
            scraper.get_reviews(db_location)
        elif inputs[2] == 'new':
            database_manager.drop_steam_reviews()
            scraper.get_reviews(db_location)
        else:
            return inputs_feedback()

    elif inputs[1] == 'classify_data':
        train_classify_data.classify_reviews(db_location)

    else:
        return inputs_feedback()


def receive_inputs():
    inputs = sys.argv
    return process_inputs(inputs)

print(receive_inputs())
sys.exit()
