#!/usr/bin/env python

# Functions for calculating k-Nearest Neighbors

from numpy import *
import operator
from os import listdir

def createDataSet():
    group = array([[1.0,1.1], [1.0,1.0], [0,0], [0,0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels

def classify0(inX, dataSet, labels, k):
    # dataSet is an array of rows
    # dataSetSize is the number of rows (i.e. no. of data points)
    dataSetSize       = dataSet.shape[0]
    # insert inX in similar array
    # subtract dataSet entry by entry
    diffMat           = tile(inX, (dataSetSize,1)) - dataSet
    # square each entry
    sqDiffMat         = diffMat**2
    # sum along rows, put in array
    sqDistances       = sqDiffMat.sum(axis=1)
    # take square root of each entry
    distances         = sqDistances**0.5
    # argsort() returns an array of integers
    # that gives the order of the elements least to greatest
    sortedDistIndices = distances.argsort()

    classCount = {}
    for i in range(k):
        # pick out first k elements
        # find out what their labels are
        voteILabel             = labels[sortedDistIndices[i]]
        # make hash with (key,val) = (label,label_count)
        # and add 1 to the count for that label
        classCount[voteILabel] = classCount.get(voteILabel,0) + 1

    # iteritems() returns a sequence of all (key,val) pairs in a dictionary
    # itemgetter(n) returns the (n-1)th element of a tuple
    # sorted(..., key=something,...) tells sorted() to use "something" as
    # the property on which to base the sorting
    # (here itemgetter(1)==label_count)
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)

    # sortedClassCount will be a list of classCount entries
    # so sortedClassCount[0] will be the classCount
    # (label,label_count) pair of the closest label
    # so sortedClassCount[0][0] is the label from that closest element
    return sortedClassCount[0][0]


def file2matrix(filename):
    # open file and read through it
    # to count the number of lines
    fr = open(filename)
    numberOfLines = len(fr.readlines())
    # create a matrix with the same number of rows
    # and 3 columns
    returnMat = zeros( (numberOfLines,3) )
    classLabelVector = []
    # read through the file again,
    # and process line by line
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()
        listFromLine = line.split('\t')
        # for each line
        # take first 3 columns from file
        # and put as row in returnMat
        # (the file line number is the row number)
        returnMat[index,:] = listFromLine[0:3]
        # put the last (4th) column of the file
        # in a separate array of class labels
        # NB: we're converting the label to an int
        # ... this is different from the output
        # in the text
        classLabelVector.append( int( listFromLine[-1] ) )
        index += 1
    return returnMat, classLabelVector


def autoNorm(dataSet):
    # get min/max values in dataSet
    # (pass argument "0" to get min/max in each column, not row)
    # calculate data range for each column
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges  = maxVals - minVals
    # create new matrix to hold normalized data
    normDataSet = zeros( shape(dataSet) )
    # get number of rows
    m = dataSet.shape[0]
    # create matrix with minVals vector
    # listed in m rows, repeated only once per row
    # (so matrix has shape (m, length(minVals))
    # ... same as dataSet)
    # subtract from original dataSet
    # then divide column by appropriate range
    normDataSet = dataSet - tile(minVals, (m,1))
    normDataSet = normDataSet / tile(ranges, (m,1))
    return normDataSet, ranges, minVals


def datingClassTest():
    # pick a fraction of the data to use for testing
    # get data & labels
    # normalize the data
    hoRatio = 0.5
    testData = '/Users/bobtodd/Computation/mining/machine_learning_harrington/Ch1-7 Source/Ch2/datingTestSet2.txt'
    datingDataMat, datingLabels = file2matrix(testData)
    normMat, ranges, minVals = autoNorm(datingDataMat)
    # number of vectors in test = (total length of data) * (fraction desired for test)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        # for ith datum to be tested...
        # classify that datum against all the data *not* being tested
        classifierResult = classify0(normMat[i,:], normMat[numTestVecs:m,:], datingLabels[numTestVecs:m], 3)
        print "The classifier came back with: %d.  The real answer is %d." % (classifierResult, datingLabels[i])
        # count the errors
        if (classifierResult != datingLabels[i]): errorCount += 1.0
    print "The total error rate is: %f" % ( errorCount/float(numTestVecs) )


def classifyPerson():
    # create list of possible classifications
    # and get input from user
    resultList  = ['not at all', 'in small doses', 'in large doses']
    percentTats = float(raw_input("percentage of time spent playing video games? "))
    ffMiles     = float(raw_input("frequent flier miles earned per year?         "))
    iceCream    = float(raw_input("liters of ice cream consumed per year?        "))
    # get data file and convert to normalized data matrix
    # get labels, min values, data range
    dataFile    = '/Users/bobtodd/Computation/mining/machine_learning_harrington/Ch1-7 Source/Ch2/datingTestSet2.txt'
    datingDataMat, datingLabels = file2matrix(dataFile)
    normMat, ranges, minVals = autoNorm(datingDataMat)
    # put user input into array, feed to classifier
    inArr = array([ffMiles, percentTats, iceCream])
    classifierResult = classify0( (inArr - minVals)/ranges, normMat, datingLabels, 3)
    # output result to screen
    print "You will probabily like this person:", resultList[classifierResult - 1]


def img2vector(filename):
    returnVect = zeros( (1,1024) )
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0, 32*i + j] = int( lineStr[j] )
    return returnVect


def handwritingClassTest():
    # set up a list of the classification label for each digit
    hwLabels = []
    # set up directories
    trainDir = '/Users/bobtodd/Computation/mining/machine_learning_harrington/Ch1-7 Source/Ch2/trainingDigits'
    testDir  = '/Users/bobtodd/Computation/mining/machine_learning_harrington/Ch1-7 Source/Ch2/testDigits'
    # get directory contents and number of files
    trainingFileList = listdir(trainDir)
    m = len(trainingFileList)
    # set up matrix with 1 row for each file
    # each row is the length of the file (number of "pixels")
    trainingMat = zeros( (m,1024) )
    for i in range(m):
        # loop through training files
        # get file name for each file
        fileNameStr      = trainingFileList[i]
        fileStr          = fileNameStr.split('.')[0]
        # the leading digit in the file name
        # is the digit it's "supposed" to be
        classNumStr      = int( fileStr.split('_')[0] )
        # ... so add a corresponding classification entry to the labels list
        hwLabels.append(classNumStr)
        # and append the file contents as a row to the training matrix
        trainingMat[i,:] = img2vector(trainDir + "/%s" % fileNameStr)
    testFileList = listdir(testDir)
    errorCount   = 0.0
    mTest        = len(testFileList)
    for i in range(mTest):
        # loop through the test files
        fileNameStr = testFileList[i]
        fileStr     = fileNameStr.split('.')[0]
        # the leading digit tells us what the image is "supposed" to be
        classNumStr = int( fileStr.split('_')[0] )
        # load image as vector
        vectorUnderTest = img2vector(testDir + '/%s' % fileNameStr)
        # classify against the training data
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        # compare classifierResult to what the image is "supposed" to be
        print "The classifier came back with: %d.  The real answer is: %d" % (classifierResult, classNumStr)
        # if misidentified, note the error
        if (classifierResult != classNumStr): errorCount += 1.0
    print "\nThe total number of errors is: %d" % errorCount
    print "\nThe total error rate is:       %f" % (errorCount/float(mTest))
