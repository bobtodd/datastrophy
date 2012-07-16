#!/usr/bin/env python

from numpy import *
import operator

def createDataSet():
    group = array([[1.0,1.1], [1.0,1.0], [0,0], [0,0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels

def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    # NumPy "tile" creates an array with elements <first_arg>
    # and with shape <second_arg>.  Here we're taking a vector
    # inX, and putting in in an array with "dataSetSize" rows
    # and 1 column.  The result with look like a matrix with
    # dataSetSize rows and len(inX) columns.
    diffMat = tile(inX, (dataSetSize,1)) - dataSet
    # element-wise squaring, not matrix square:
    sqDiffMat = diffMat**2
    # sum along row, resulting in column vector of squared distances:
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    # get list giving the indices of "distances" in increasing order of distance
    sortedDistIndices = distances.argsort()

    classCount = {}
    for i in range(k):
        # get the label of the ith nearest neighbor
        voteIlabel = labels[sortedDistIndices[i]]
        # keep track of how many times you encountered that label
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1

    # sort the labels in order for frequency of occurrence, high to low
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

