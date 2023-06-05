import numpy as np
def get_outliar():
    # Define the list of numbers
    numbers = [1, 2, 3, 5, 7, 9, 11,50,45,30 ,13, 16, 18, 25, 30]

    # Define the number of IQRs from the median to keep
    num_iqrs = 1.5

    # Calculate the median and interquartile range (IQR) values
    median = np.median(numbers)
    quartiles = np.percentile(numbers, [40, 60])
    iqr = quartiles[1] - quartiles[0]

    # Define the outlier limits as the median plus or minus the IQR multiplied by the number of IQRs to keep
    lower_limit = median - num_iqrs * iqr
    upper_limit = median + num_iqrs * iqr

    # Select only the numbers that are beyond the IQR limits
    outliers = [num for num in numbers if num < lower_limit or num > upper_limit]

    # Print the outlier numbers
    print(outliers)

import numpy as np
from scipy.stats import zscore

def get_useful_strings(string_list, min_word_count_threshold, zscore_threshold):
    word_counts = np.array([len(string.split()) for string in string_list])
    zscores = zscore(word_counts)

    filtered_strings = [string for string, zscore_val in zip(string_list, zscores) if len(string.split()) >= min_word_count_threshold and zscore_val >= zscore_threshold]

    return filtered_strings

text_chunks  =  ["sjsjs","sd","About NCA","Sports and Exercise Medicine","Facilities","Age Verification","Programmes","abca","an","de","a"]
top_3_longest = sorted(text_chunks, key=len, reverse=True)[:3]


min_word_count_threshold = 3
zscore_threshold = 1.0

useful_strings = get_useful_strings(text_chunks, min_word_count_threshold, zscore_threshold)
print(useful_strings)