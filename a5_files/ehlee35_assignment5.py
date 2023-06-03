import pandas as pd
import string
import os
import sys
from evaluation import computeAccuracy, computePrecisionRecall

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer

import numpy as np
import matplotlib.pyplot as plt

# TODO: Your custom imports here; or copy the functions to here manually.
from evaluation import computeAccuracy, computePrecisionRecall

# TODO: You may need to modify assignment 4 if you just had a main() there.
# my_naive_bayes() should take a column as input and return as output 10 floats (numbers)
# representing the metrics.
from assignment4 import my_naive_bayes

def initialize_score_list(o, c, low, no, lem, list_type):
    train = []
    test = []

    for model in [o, c, low, no, lem]:
        train.append(model['TRAIN'][list_type])
        test.append(model['TEST'][list_type])

    return train, test

def main(argv):
    data = pd.read_csv(argv[1], index_col=[0])
    # print(data.head())  # <- Verify the format. Comment this back out once done.

    # Part II:
    # Run all models and store the results in variables (dicts).
    # TODO: Make sure you imported your own naive bayes function and it works properly with a named column input!
    # TODO: See also the next todo which gives an example of a convenient output for my_naive_bayes()
    # which you can then easily use to collect different scores.
    # For example (and as illustrated below), the models (nb_original, nb_cleaned, etc.) can be not just lists of scores
    # but dicts where each score will be stored by key, like [TEST][POS][RECALL], etc.
    # But you can also just use lists, except then you must not make a mistake, which score you are accessing,
    # when you plot graphs.

    nb_original = my_naive_bayes(data, 'review')
    print('NB algorithm success! 1/5')
    nb_cleaned = my_naive_bayes(data, 'cleaned_review')
    print('NB algorithm success! 2/5')
    nb_lowercase = my_naive_bayes(data, 'lowercased')
    print('NB algorithm success! 3/5')
    nb_no_stop = my_naive_bayes(data, 'no stopwords')
    print('NB algorithm success! 4/5')
    nb_lemmatized = my_naive_bayes(data, 'lemmatized')
    print('NB algorithm success! 5/5')

    # Collect accuracies and other scores across models.
    # TODO: Harmonize this with your own naive_bayes() function!
    # The below assumes that naive_bayes() returns a fairly complex dict of scores.
    # (NB: The dicts there contain other dicts!)
    # The return statement for that function looks like this:
    # return({'TRAIN': {'accuracy': accuracy_train, 'POS': {'precision': precision_pos_train, 'recall': recall_pos_train}, 'NEG': {'precision': precision_neg_train, 'recall': recall_neg_train}}, 'TEST': {'accuracy': accuracy_test, 'POS': {'precision': precision_pos_test, 'recall': recall_pos_test}, 'NEG': {'precision': precision_neg_test, 'recall': recall_neg_test}}})
    # This of course assumes that variables like "accuracy_train", etc., were assigned the right values already.
    # You don't have to do it this way; we are giving it to you just as an example.
    train_accuracies = []
    test_accuracies = []
    # TODO: Initialize other score lists similarly. The precision and recalls, for negative and positive, train and test.

    for model in [nb_original, nb_cleaned, nb_lowercase, nb_no_stop, nb_lemmatized]:
        # TODO: See comment above about where this "model" dict comes from.
        # If you are doing something different, e.g. just a list of scores,
        # that's fine, change the below as appropriate,
        # just make sure you don't confuse where which score is.
        train_accuracies.append(model['TRAIN']['accuracy'])
        test_accuracies.append(model['TEST']['accuracy'])
        # TODO: Collect other scores similarly. The precision and recalls, for negative and positive, train and test.

    train_precision_pos, test_precision_pos = initialize_score_list(nb_original, nb_cleaned, nb_lowercase,
                                                                    nb_no_stop, nb_lemmatized, 'precision_pos')
    train_recall_pos, test_recall_pos = initialize_score_list(nb_original, nb_cleaned, nb_lowercase,
                                                              nb_no_stop, nb_lemmatized, 'recall_pos')
    train_precision_neg, test_precision_neg = initialize_score_list(nb_original, nb_cleaned, nb_lowercase,
                                                                    nb_no_stop, nb_lemmatized, 'precision_neg')
    train_recall_neg, test_recall_neg = initialize_score_list(nb_original, nb_cleaned, nb_lowercase,
                                                              nb_no_stop, nb_lemmatized, 'recall_neg')

    # TODO: Create the plot(s) that you want for the report using matplotlib (plt).
    # Use the below to save pictures as files:
    # plt.savefig('filename.png')

    for i in range(5):
        x_axis = np.array(range(10))
        y_axis = np.array([train_accuracies[i], test_accuracies[i], train_precision_pos[i], test_precision_pos[i],
                           train_recall_pos[i], test_recall_pos[i], train_precision_neg[i], test_precision_neg[i],
                           train_recall_neg[i], test_recall_neg[i]])

        plt.title(['nb_original', 'nb_cleaned', 'nb_lowercase', 'nb_no_stop', 'nb_lemmatized'][i])
        plt.xlabel("Score Types")
        plt.ylabel("Percentage %")

        colors = ['royalblue', 'cornflowerblue', 'forestgreen', 'limegreen', 'turquoise', 'aquamarine',
                  'maroon', 'firebrick', 'indianred', 'lightcoral']

        labels = ['train_accuracies', 'test_accuracies', 'train_precision_pos', 'test_precision_pos',
                  'train_recall_pos', 'test_recall_pos', 'train_precision_neg', 'test_precision_neg',
                  'train_recall_neg', 'test_recall_neg']

        plt.bar(x_axis, y_axis, color=colors, label=labels)

        for index, value in enumerate([train_accuracies[i], test_accuracies[i], train_precision_pos[i], test_precision_pos[i],
                                       train_recall_pos[i], test_recall_pos[i], train_precision_neg[i], test_precision_neg[i],
                                       train_recall_neg[i], test_recall_neg[i]]):
            plt.text(index, value, str(value))

        plt.legend(bbox_to_anchor=(1.02, 1), loc=0)

        plt.savefig(['nb_original', 'nb_cleaned', 'nb_lowercase', 'nb_no_stop', 'nb_lemmatized'][i], bbox_inches='tight')
        plt.show()


if __name__ == "__main__":
    main(sys.argv)
