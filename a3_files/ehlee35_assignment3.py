# This is a skeleton for your assignment 2 script.
# It contains the program structure, function names,
# the main function already written,
# and comment instructions regarding what you should write.

# SUMMARY OF WHAT YOU NEED TO DO:
# You will only need to fill in several lines of code.
# The program looks long because of the comments; it is actually very short.
# Look for TODO items! (But read the comments, too :) ).


# Import the system module
import sys

# Import regular expressions module
import re

# Import the string module to access its punctuation set
import string


# The function below should be called on a file name.
# It should open the file, read its contents, and store it in a variable.
# Then it should remove punctuation marks and return the "cleaned" text.

def cleanFileContents(f):
    # The two lines below open the file and read all the text from it
    # storing it into a variable called "text".
    # You do not need to modify the below two lines; they are already working as needed.
    with open(f, 'r', encoding='utf-8') as f:
        text = f.read()

    # The line below will clean the text of punctuation marks.
    # Ask if you are curious about how it works! But you can just use it as is.
    # Observe the effect of the function by inspecting the debugger pane while stepping over.
    clean_text = text.translate(str.maketrans('', '', string.punctuation))

    # Now, we will want to replace all tabs with spaces, and also all occurrences of more than one
    # space in a row with a single space. Review the regular expression slides/readings, and
    # write a statement below which replaces all occurrences of one or more whitespace-group characters
    # (that will include tabs) with a single space. You want the re.sub function.
    # The shortcut for all whitespace characters is \s. The regex operator for "one or more" is +.
    # Read re.sub()'s documentation to understand which argument goes where in the parentheses.

    # TODO: Your call to the re.sub function of the regular expression module here.
    # As is, the value of clean_text does not change.
    clean_text = re.sub('\s+', ' ', clean_text)
    clean_text = re.sub('  ', ' ', clean_text)

    # Do not forget to return the result!
    return clean_text


'''
The below function takes a string as input, breaks it down into word tokens by space, and stores, in a dictionary table,
how many times each word occurred in the text. It returns the dictionary table.
'''


def countTokens(text):
    # Initializing an empty dictionary. Do not modify the line below, it is already doing what is needed.
    token_counts = {}

    # Use the split() function, defined for strings, to split the text by space.
    # Store the result in a variable, e.g. called "tokens".
    # See what the split() function returns and stores in your variable
    # as you step through the execution in the debugger.

    # TODO: Write a statement below calling split() on your text and storing the
    # result in a new variable.

    tokens = text.split()

    # Now, we need to iterate over each word in the list of tokens
    # (write a for loop over the list that split() returned).
    # Inside the loop, that is, for each word, we will perform some conditional logic:
    #   If the word is not yet stored in the dictionary
    #   we called "token_counts" as a key, we will store it there now,
    #   and we will initialize the key's value to 0.
    # Outside that if statement: now that we are sure
    # the word is stored as a key, we will increment the count by 1.

    # TODO: Write a for loop here, doing what is described above.

    for word in tokens:
        if word in token_counts.keys():
            token_counts[word] += 1
        else:
            token_counts[word] = 1

    # Do not forget to return the result!
    return token_counts


# This silly "prediction function" will do the following "rudimentary data science":
# If a review contains more of the word "good" than of the word "bad", 
# the function predicts "positive" (by returning a string "POSITIVE").
# If it contains more of the word "bad" than of the word "good",
# the function predicts "negative". 
# If the count is equal (note that this includes zero count),
# the function cannot make a prediction and returns a string "NONE".


# Constants. Constants are important to avoid typo-related bugs, among other reasons.
# Use these constants as return values for the below function.

POS_REVIEW = "POSITIVE"
NEG_REVIEW = "NEGATIVE"
NONE = "NONE"
POS = 'good'
NEG = 'bad'


def predictSimplistic(counts):
    # This line retrieves the count for "good". If the word "good" is not found in "counts", it returns 0.
    pos_count = counts.get(POS, 0)
    # TODO: Write a similar statement below to retrieve the count of "bad".
    neg_count = counts.get(NEG, 0)

    # TODO: Write an if-elif-else block here, following the logic described in the function description.
    # Do not forget to return the prediction! You will be returning one of the constants declared above.
    # You may choose to store a prediction in a variable and then write the return statement outside
    # of the if-else block, or you can have three return statements within the if-else block.
    if pos_count > neg_count:
        return POS_REVIEW
    elif pos_count < neg_count:
        return NEG_REVIEW
    else:

        # TODO: You will modify the below return statement or move it into your if-else block when you write it.
        return NONE


def simplisticPrediction(filename):
    clean_text = cleanFileContents(filename)
    tokens_with_counts = countTokens(clean_text)
    prediction = predictSimplistic(tokens_with_counts)

    return prediction


# The main function is the entry point of the program.
# When debugging, if you want to start from the very beginning,
# start here. NB: Put the breakpoint not on the "def" line but below it.
# Do not modify this function; we already wrote it for you.
# You need to modify the functions which it calls, not the main() itself.


def main(argv):
    # PART 2

    from pathlib import Path

    from review_vector import reviewVec

    txt_files_pos = list(Path(argv[1]).glob('*.txt'))

    reviewed_pos_txt_files = []
    reviewed_neg_txt_files = []

    for file in txt_files_pos:
        prediction = simplisticPrediction(file)
        reviewed_pos_txt_files.append(reviewVec(prediction, POS_REVIEW))
        # print("The prediction for file {} is {}".format(file, prediction))

    txt_files_neg = list(Path(argv[2]).glob('*.txt'))

    for file in txt_files_neg:
        prediction2 = simplisticPrediction(file)
        reviewed_neg_txt_files.append(reviewVec(prediction2, NEG_REVIEW))
        # print("The prediction for file {} is {}".format(file, prediction2))

    # PART 3
    # ACCURACY

    from evaluation import computeAccuracy

    pos_class_predictions = []
    pos_class_gold_labels = []

    for item in reviewed_pos_txt_files:
        pos_class_predictions.append(item.text)

    for item in reviewed_pos_txt_files:
        pos_class_gold_labels.append(item.correct_label)

    neg_class_predictions = []
    neg_class_gold_labels = []

    for item in reviewed_neg_txt_files:
        neg_class_predictions.append(item.text)

    for item in reviewed_neg_txt_files:
        neg_class_gold_labels.append(item.correct_label)

    all_predictions = pos_class_predictions + neg_class_predictions
    all_gold_labels = pos_class_gold_labels + neg_class_gold_labels

    print(round(computeAccuracy(all_predictions, all_gold_labels)[0], 4))

    # PRECISION POSITIVE

    from evaluation import computePrecisionRecall

    print(round(computePrecisionRecall(all_predictions, all_gold_labels, POS_REVIEW)[0], 4))
    print(round(computePrecisionRecall(all_predictions, all_gold_labels, POS_REVIEW)[1], 4))
    print(round(computePrecisionRecall(all_predictions, all_gold_labels, NEG_REVIEW)[0], 4))
    print(round(computePrecisionRecall(all_predictions, all_gold_labels, NEG_REVIEW)[1], 4))

# The code below is needed so that this file can be used as a module,
# which we will (more or less) be doing in future assignments.
if __name__ == "__main__":
    main(sys.argv)
