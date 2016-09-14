#! usr/bin/env python3

'''
For some reason, these classifiers have performed badly. I don't know why that is.
I'm going to use the partial fit method with the MultinomialNB and save the instance 
'''

from application import data_prep

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.svm import SVC, LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import classification_report


def train_mnb(training_vectors, training_classes):
    '''
    Trains a classifier and returns the result, so we can test it.
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

def train_linear_svc(training_vectors, training_classes):
    '''
    Trains the Linear Scaled Vector Machine classifier and returns the result, so we can test it.
    '''

    classifier_linear_svc = LinearSVC()
    classifier_linear_svc.fit(training_vectors, training_classes)
    return classifier_linear_svc

def train_logistic_regression(training_vectors, training_classes):
    '''
    Trains the Logistic Regression classifier and returns the result, so we can test it.
    '''

    classifier_logistic_regression = LogisticRegression()
    classifier_logistic_regression.fit(training_vectors, training_classes)
    return classifier_logistic_regression


def test_classifier(classifier, test_vectors, testing_classes, reviews_to_test):
    '''
    Tests a classifier with the testing data from the scraped reviews, which were retrieved from db.
    '''

    running_correct_number = 0
    for i, _ignore in enumerate(testing_classes):
        prediction = classifier.predict(test_vectors[i])

        if prediction == testing_classes[i]:
            running_correct_number += 1

    return (running_correct_number / reviews_to_test) * 100


def classify_reviews(db_location):
    '''
    This is the function to control this module, but it would take some time to run through the data, and I'm not sure how to test it.
    Our database has 5000 records we can test, so do that.
    '''

    end_interval = 4500 #Put this in the run_app module, which is the user's interface.
    reviews_to_test = 500

    for reviews_to_train in range(reviews_to_test, end_interval, reviews_to_test):

        reviews_to_retrieve = reviews_to_train + reviews_to_test

        training_documents, testing_documents, training_classes, testing_classes = data_prep.prep_for_classifiers(db_location, reviews_to_retrieve, reviews_to_test)

        vectorizer = TfidfVectorizer()
        training_vectors = vectorizer.fit_transform(training_documents)
        test_vectors = vectorizer.transform(testing_documents)

        trained_mnb = train_mnb(training_vectors, training_classes)
        trained_svc = train_svc(training_vectors, training_classes)
        trained_linear_svc = train_svc(training_vectors, training_classes)
        trained_logistic_regression = train_logistic_regression(training_vectors, training_classes)

        mnb_result = test_classifier(trained_mnb, test_vectors, testing_classes, reviews_to_test)
        svc_result = test_classifier(trained_svc, test_vectors, testing_classes, reviews_to_test)
        linear_svc_result = test_classifier(trained_linear_svc, test_vectors, testing_classes, reviews_to_test)
        logistic_result = test_classifier(trained_logistic_regression, test_vectors, testing_classes, reviews_to_test)

        result_string = '%.1f, %.1f, %.1f, %.1f' %(mnb_result, svc_result, linear_svc_result, logistic_result)
        print(result_string)
