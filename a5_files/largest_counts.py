import sys
import pandas as pd

# From Assignment 2, copied manually here just to remind you
# that you can copy stuff manually if importing isn't working out.
# You can just use this or you can replace it with your function.


def countTokens(text):
    token_counts = {}
    tokens = text.split(' ')
    for word in tokens:
        if not word in token_counts:
            token_counts[word] = 0
        token_counts[word] += 1
    return token_counts

def sort_freq(dict):
    dict_keys = dict.keys()
    dict_values = dict.values()

    zipped_list = list(zip(dict_keys, dict_values))
    zipped_list.sort(key=lambda x: x[1], reverse=True)

    return zipped_list

def table_production(list1, list2, list3, list4):
    table_data = []

    for index in range(20):
        table_data.append([list1[index][0], list1[index][1], list2[index][0], list2[index][1],
                           list3[index][0], list3[index][1], list4[index][0], list4[index][1]])

    return table_data

def condensed_sort_write(data, sent, f):
    original = countTokens(data["review"].str.cat())
    cleaned = countTokens(
        data["cleaned_review"].str.cat())
    lowercased = countTokens(
        data["lowercased"].str.cat())
    no_stop = countTokens(
        data["no stopwords"].str.cat())
    lemmatized = countTokens(
        data["lemmatized"].str.cat())

    original_sorted = sort_freq(original)
    cleaned_sorted = sort_freq(cleaned)
    lowercased_sorted = sort_freq(lowercased)
    no_stop_sorted = sort_freq(no_stop)
    lemmatized_sorted = sort_freq(lemmatized)

    f.write('Original {} reviews:\n'.format(sent))
    for k, v in original_sorted[:20]:
        f.write('{}\t{}\n'.format(k, v))
    f.write('Cleaned {} reviews:\n'.format(sent))
    for k, v in cleaned_sorted[:20]:
        f.write('{}\t{}\n'.format(k, v))
    f.write('Lowercased {} reviews:\n'.format(sent))
    for k, v in lowercased_sorted[:20]:
        f.write('{}\t{}\n'.format(k, v))
    f.write('No stopwords {} reviews:\n'.format(sent))
    for k, v in no_stop_sorted[:20]:
        f.write('{}\t{}\n'.format(k, v))
    f.write('Lemmatized {} reviews:\n'.format(sent))
    for k, v in lemmatized_sorted[:20]:
        f.write('{}\t{}\n'.format(k, v))

def largest_counts(data):  # TODO: Finish implementing this function

    # TODO: Cut up the rows in the dataset according to how you stored things.
    # The below assumes test data is stored first and negative is stored before positive.
    # If you did the same, no change is required.
    pos_train_data = data[:12500]
    pos_test_data = data[25000:37500]
    neg_train_data = data[12500:25000]
    neg_test_data = data[37500:50000]

    # TODO: SORT the count dicts which countTokens() returns
    # by value (count) in reverse (descending) order.
    # It is your task to Google and learn how to do this, but we will help of course,
    # if you come to use with questions. This can be daunting at first, but give it time.
    # Spend some (reasonable) time across a few days if necessary, and you will do it!

    # As is, the counts returned by the counter AREN'T sorted!
    # So you won't be able to easily retrieve the most frequent words.

    # NB: str.cat() turns whole column into one text
    train_counts_pos_original = countTokens(pos_train_data["review"].str.cat())
    train_counts_pos_cleaned = countTokens(
        pos_train_data["cleaned_review"].str.cat())
    train_counts_pos_lowercased = countTokens(
        pos_train_data["lowercased"].str.cat())
    train_counts_pos_no_stop = countTokens(
        pos_train_data["no stopwords"].str.cat())
    train_counts_pos_lemmatized = countTokens(
        pos_train_data["lemmatized"].str.cat())

    train_counts_pos_original = sort_freq(train_counts_pos_original)
    train_counts_pos_cleaned = sort_freq(train_counts_pos_cleaned)
    train_counts_pos_lowercased = sort_freq(train_counts_pos_lowercased)
    train_counts_pos_no_stop = sort_freq(train_counts_pos_no_stop)
    train_counts_pos_lemmatized = sort_freq(train_counts_pos_lemmatized)

    # Once the dicts are sorted, output the first 20 rows for each.
    # This is already done below, but changes may be needed depending on what you did to sort the dicts.
    # The [:19] "slicing" syntax expects a list. If you sorting call return a list (which is likely, as being sorted
    # is conceptualy a properly of LISTS,  NOT dicts),
    # you may want to remove the additional list(dict_name.items()) conversion.
    with open('counts.txt', 'w') as f:
        f.write('Original Train POS reviews:\n')
        for k, v in train_counts_pos_original[:20]:
            f.write('{}\t{}\n'.format(k, v))
        f.write('Cleaned Train POS reviews:\n')
        for k, v in train_counts_pos_cleaned[:20]:
            f.write('{}\t{}\n'.format(k, v))
        f.write('Lowercased Train POS reviews:\n')
        for k, v in train_counts_pos_lowercased[:20]:
            f.write('{}\t{}\n'.format(k, v))
        f.write('No stopwords Train POS reviews:\n')
        for k, v in train_counts_pos_no_stop[:20]:
            f.write('{}\t{}\n'.format(k, v))
        f.write('Lemmatized Train POS reviews:\n')
        for k, v in train_counts_pos_lemmatized[:20]:
            f.write('{}\t{}\n'.format(k, v))

        condensed_sort_write(neg_train_data, 'Train NEG', f)
        condensed_sort_write(pos_test_data, 'Test POS', f)
        condensed_sort_write(neg_test_data, 'Test NEG', f)

        # I originally copy and pasted the code multiple times, but I decided to make it a function to clean it up

        # TODO: Do the same for all the remaining training dicts, per Assignment spec.

    # TODO: Copy the output of the above print statements
    #  into your document/report, or otherwise create a table/visualization for these counts.
    # Manually is fine, or you may explore bar charts in pandas! Be creative :).

    # Production of 2 .csv files for document

    column_names = ["Original Words", "Frequency", "Cleaned Words", "Frequency",
                    "No stop Words", "Frequency", "Lemmatized Words", "Frequency"]

    table_data = table_production(train_counts_pos_original, train_counts_pos_cleaned,
                                  train_counts_pos_no_stop, train_counts_pos_lemmatized)

    df = pd.DataFrame(data=table_data, columns=column_names)
    df.to_csv('data_table_pos.csv')

    train_counts_neg_original = countTokens(neg_train_data["review"].str.cat())
    train_counts_neg_cleaned = countTokens(
        neg_train_data["cleaned_review"].str.cat())
    train_counts_neg_no_stop = countTokens(
        neg_train_data["no stopwords"].str.cat())
    train_counts_neg_lemmatized = countTokens(
        neg_train_data["lemmatized"].str.cat())

    train_counts_neg_original = sort_freq(train_counts_neg_original)
    train_counts_neg_cleaned = sort_freq(train_counts_neg_cleaned)
    train_counts_neg_no_stop = sort_freq(train_counts_neg_no_stop)
    train_counts_neg_lemmatized = sort_freq(train_counts_neg_lemmatized)

    table_data = table_production(train_counts_neg_original, train_counts_neg_cleaned,
                                  train_counts_neg_no_stop, train_counts_neg_lemmatized)

    df = pd.DataFrame(data=table_data, columns=column_names)
    df.to_csv('data_table_neg.csv')

def main(argv):
    data = pd.read_csv(argv[1], index_col=[0])
    # print(data.head())  # <- Verify the format. Comment this back out once done.

    largest_counts(data)


if __name__ == "__main__":
    main(sys.argv)
