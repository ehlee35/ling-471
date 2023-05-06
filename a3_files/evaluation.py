'''
Recommended functions to implement.
You can do things differently if you like, so long as you get correct results.

The function takes two lists (arrays), one of system predictions and one of gold labels.
The assumption is that the lists are of equal length and the order of elements in both lists
corresponds to the order of data points in the dataset. It is the responsibility of 
the function caller to ensure that is the case; otherwise the function won't return
anything meaningful.

The function computes the accuracy by comparing the predicted labels to gold labels.
Accuracy = correct predictions / total predictions
Consider also recording the indices of the data points for which a wrong prediction was made.
The function can then return a tuple: (accuracy, mistakes) where accuracy is a float
and mistakes is a list of integers.

'''


def computeAccuracy(predictions, gold_labels):
    # The assert statement will notify you if the condition does not hold.
    assert len(predictions) == len(gold_labels)

    mistakes = []  # Consider keeping a record of the indices of the errors.

    for index in range(len(predictions)):
        if predictions[index] != gold_labels[index]:
            mistakes.append(index)

    accuracy = (len(predictions) - len(mistakes)) / len(predictions)

    return (accuracy, mistakes)


'''
Recommended function scec to implement. 
You can do things differently if you like (including changing what is passed in), 
so long as you get correct results.

As suggested, the function takes three arguments. 
The first two are arrays, one of predicted labels and one of actual (gold) labels.
The third argument is a string indicating which class the precision is computed for.
This is the confusing part! You can compute precision and recall wrt the positive reviews 
or wrt the negative reviews! What is considered a "true positive" depends on what the relevant class is!

The function then computes precision as per definition: true positives / (true positives + false positives)
And it computes recall as per definition: true positives / (true positives + false negatives)

It returns a tuple of floats
: (presision, recall)
'''


def computePrecisionRecall(predictions, gold_labels, relevant_class):
    assert len(predictions) == len(gold_labels)

    true_positives = 0
    false_positives = 0
    false_negatives = 0

    for index in range(len(predictions)):
        # working

        if predictions[index] == gold_labels[index] and gold_labels[index] == relevant_class:
            true_positives += 1
        if predictions[index] != gold_labels[index] and predictions[index] == relevant_class:
            false_positives += 1
        if predictions[index] != gold_labels[index] and gold_labels[index] == relevant_class:
            false_negatives += 1

    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)

    return (precision, recall)
