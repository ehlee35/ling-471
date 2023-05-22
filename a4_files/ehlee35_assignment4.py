# Skeleton for Assignment 4
# Ling471 Spring 2023

import pandas as pd
import string
import sys

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# These are your own functions you wrote for Assignment 3:
from evaluation import computePrecisionRecall, computeAccuracy
# Note: If you did not put your functions into the `evaluation.py` file
# import the functions however you need, or copy and paste them into this file
# (and you would then need  to delete the `from evaluation import...` line above)

# Constants
ROUND = 4
GOOD_REVIEW = 1
BAD_REVIEW = 0
ALPHA = 1


# This function will be reporting errors due to variables which were not assigned any value.
# Your task is to get it working! You can comment out things which aren't working at first.
def main(argv):

    # Read in the data. NB: You may get an extra Unnamed column with indices; this is OK.
    # If you like, you can get rid of it by passing a second argument to the read_csv(): index_col=[0].
    data = pd.read_csv(argv[1], index_col=[0])
    # print(data.head()) # <- Verify the format. Comment this back out once done.

    # TODO: Change as appropriate, if you stored data differently (e.g. if you put train data first).
    # You may also make use of the "type" column here instead! E.g. you could sort data by "type".
    # At any rate, make sure you are grabbing the right data! Double check with temporary print statements,
    # e.g. print(test_data.head()).

    train_data = data[:25000]  # Assuming the first 25,000 rows are training data.

    # print(train_data.head())

    # Assuming the second 25,000 rows are testing data. Double check!
    test_data = data[25000:50000]

    # print(test_data.head())

    # TODO: Set the below 4 variables to contain:
    # X_train: the training data; y_train: the training data labels;
    # X_test: the test data; y_test: the test data labels.
    # Access the data frames by the appropriate column names.
    X_train = train_data.review
    y_train = train_data.label
    X_test = test_data.review
    y_test = test_data.label

    # print(X_train.head())

    # The next three lines are performing feature extraction and word counting. 
    # They are choosing which words to count frequencies for, basically, to discard some of the noise.
    # If you are curious, you could read about TF-IDF,
    # e.g. here: https://www.geeksforgeeks.org/tf-idf-model-for-page-ranking/
    # or here: https://en.wikipedia.org/wiki/Tf%E2%80%93idf
    # TODO: Add a general brief comment on why choosing which words to count may be important.
    # Choosing the right words will help identify whether a review is positive or negative more accurately, whereas choosing the wrong words could impact the accuracy of the program and muddle the data. For example, focusing on the word "the" which can appear in very similar frequencies between negative and positive reviews might not provide any crucial information to the prediction.

    # print(X_train.values)

    tf_idf_vect = TfidfVectorizer(ngram_range=(1, 2))
    tf_idf_train = tf_idf_vect.fit_transform(X_train.values)
    tf_idf_test = tf_idf_vect.transform(X_test.values)

    # TODO COMMENT: The hyperparameter alpha is used for Laplace Smoothing.
    # Add a brief comment, trying to explain, in your own words, what smoothing is for.
    # You may want to read about Laplace smoothing here: https://towardsdatascience.com/laplace-smoothing-in-na%C3%AFve-bayes-algorithm-9c237a8bdece
    # With the addition of the hyperparameter alpha, smoothing allows the computer to realize that some probability of a word does exist in the likelihood multiplication calculation, even if that word does not appear in the data set. This prevents the algorithm from returning an incorrect result due to using a 0% probability. For example, if the training data for good reviews does not include the word "intrigued" while the training data for bad reviews contain the words "not intrigued", a review that said that the movie "intrigued me" (denoting good) might be instantly categorized as bad as the train data would claim that there is a 0% probability of the word "intrigued" appearing in the text.

    clf = MultinomialNB(alpha=ALPHA)
    # TODO COMMENT: Add a comment explaining in your own words what the "fit()" method is doing.
    # "fit()" is determining the weights of each of the coefficients that the algorithm multiplies the given vector (a vector from the list of vectors tf_idf_train) against to get closest to the true value (y_train). These weights/coefficients are stored in clf.
    clf.fit(tf_idf_train, y_train)

    # TODO COMMENT: Add a comment explaining in your own words what the "predict()" method is doing in the next two lines.
    # "predict()" will output the result of the "fit()" function, which is a single value that will be used to compare against the true values (y_train). In other words, "predict()" uses the weights determined by "fit()" to generate a value or prediction. In the case of this algorithm, predict will return a list of values for each vector.
    y_pred_train = clf.predict(tf_idf_train)
    y_pred_test = clf.predict(tf_idf_test)

    # TODO: Compute accuracy, precision, and recall, for both train and test data.
    # Import and call your methods from evaluation.py (or wherever) which you wrote for HW3.
    # Note: If you methods there accept lists, you will probably need to cast your pandas label objects to simple python lists:
    # e.g. list(y_train) -- when passing them to your accuracy and precision and recall functions.

    accuracy_test = computeAccuracy(list(y_pred_test), list(y_test))[0]
    accuracy_train = computeAccuracy(list(y_pred_train), list(y_train))[0]
    precision_pos_test, recall_pos_test = computePrecisionRecall(list(y_pred_test), list(y_test), 'pos')
    precision_neg_test, recall_neg_test = computePrecisionRecall(list(y_pred_test), list(y_test), 'neg')
    precision_pos_train, recall_pos_train = computePrecisionRecall(list(y_pred_train), list(y_train), 'pos')
    precision_neg_train, recall_neg_train = computePrecisionRecall(list(y_pred_train), list(y_train), 'neg')

    # Report the metrics via standard output.
    # Please DO NOT modify the format (for grading purposes).
    # You may change the variable names of course, if you used different ones above.

    print("Train accuracy:           \t{}".format(round(accuracy_train, ROUND)))
    print("Train precision positive: \t{}".format(
        round(precision_pos_train, ROUND)))
    print("Train recall positive:    \t{}".format(
        round(recall_pos_train, ROUND)))
    print("Train precision negative: \t{}".format(
        round(precision_neg_train, ROUND)))
    print("Train recall negative:    \t{}".format(
        round(recall_neg_train, ROUND)))
    print("Test accuracy:            \t{}".format(round(accuracy_test, ROUND)))
    print("Test precision positive:  \t{}".format(
        round(precision_pos_test, ROUND)))
    print("Test recall positive:     \t{}".format(
        round(recall_pos_test, ROUND)))
    print("Test precision negative:  \t{}".format(
        round(precision_neg_test, ROUND)))
    print("Test recall negative:     \t{}".format(
        round(recall_neg_test, ROUND)))


if __name__ == "__main__":
    main(sys.argv)
