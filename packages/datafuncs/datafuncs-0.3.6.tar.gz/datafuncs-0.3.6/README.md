# Datafuncs
Functions for Data Processing

## Functions

.mean(data) - Returns the mean of a list

.setOutlier(data, low, high) - Removes the outliers from a list

.imputate(data, low, high) - Replaces outliers in a list with the mean of the filtered list.

.median(data) - Returns the median of a list

.mode(data) - Returns the mode of a list

.freq(data, value) - Returns the Amount of times that a value occurs in the list data

.Range(data) - Returns the range of the list

.replace(data, old, new) - Replaces every old value in the list with the new value
 
.gen(length, low, high, type) - Generates a list of random values of the type specified that is length long - Ignore the low and high values if you are not generating a list of integers

.stdDev(data) - Returns the standard deviation of the list to two decimal places

.variance(data) - Returns the variance of the list to two decimal places

.iqr(data) - Returns the Interquartile Range of the list data to two decimal places

.zScore(data, value) - Returns the z score of a value using the list data as a dataset

.percentile(zScore) - Returns the percentile of a value using the z score

.outlier(data, zScoreCutoff) -  Automatically removes outliers outside a set z score

.merge(list1, list2) - Merges two lists into tupled lists

.covariance(list1, list2) - Returns the covariance of the two given lists to two decimal places

.correlate(list1, list2) - Returns the correlation coefficient of the two given lists to two decimal places
    
.slope(list1, list2) - Calculates the of a linear regression line using the two given lists

.regression(list1, list2, value) - Calculates the regression line for a given value between two lists

.all(list1, list2, list3, etc...) - Returns everything the script knows about a list and compares multiple lists

.Help() - Prints a list of the above functions and their explanations

### Created by Fraser Woodward & Liam Leonard 
