#! usr/bin/env python3

from application import data_prep

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.svm import SVC, LinearSVC
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import classification_report

def train_mnd(training_vectors, training_classes):
    '''
    Trains the Multinomial Naive Bayes classifier and returns the result, so we can test it.
    '''

    classifier_mnb = MultinomialNB()
    classifier_mnb.fit(training_vectors, training_classes)
    return classifier_mnb

def train_svc(training_vectors, training_classes):
    '''
    Trains the Scaled Vector Machine classifier and returns the result, so we can test it.
    '''

    classifier_svc = SVC()
    classifier_svc.fit(training_vectors, training_classes)
    return classifier_svc

def classify_reviews(db_location):
    '''
    This is the function to control this module, but it would take some time to run through the data, and I'm not sure how to test it.
    Our database has 5000 records we can test, so do that.
    '''

    start_interval = 100
    end_interval = 4900 #Put this in the run_app module, which is the user's interface.
    reviews_to_test = 100

    for reviews_to_train in range(start_interval, end_interval, reviews_to_test):

        reviews_to_retrieve = reviews_to_train + reviews_to_test

        training_documents, testing_documents, training_classes, testing_classes = data_prep.prep_for_classifiers(db_location, reviews_to_retrieve, reviews_to_test)

        vectorizer = TfidfVectorizer()
        training_vectors = vectorizer.fit_transform(training_documents)
        test_vectors = vectorizer.transform(testing_documents)

        trained_mnd = train_mnd(training_vectors, training_classes)
        trained_svc = train_svc(training_vectors, training_classes)