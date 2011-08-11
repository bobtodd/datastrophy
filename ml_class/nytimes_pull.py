#!/usr/bin/env python
# encoding: utf-8

"""
nytimes_pull.py

Created by Hilary Mason on 2011-02-17.
Copyright (c) 2011 Hilary Mason. All rights reserved.
"""

import sys, os
import urllib, urllib2
import json

def main(api_key, category, label):
    # This creates a file called "label"
    # with corresponding output from the NYT category

    content = []
    for i in range(0,5):
        print "http://api.nytimes.com/svc/search/v1/article?query=classifiers_facet:%s&api-key=%s&offset=%s" % (category, api_key, i)
        h = urllib.urlopen( "http://api.nytimes.com/svc/search/v1/article?query=classifiers_facet:%s&api-key=%s&offset=%s" % (category, api_key, i) )
        data = json.loads(h.read())
        for result in data['results']:
            content.append(result['body'])

    f = open(label, 'w')
    for line in content:
        try:
            f.write("%s\n" % line)
        except UnicodeEncodeError:
            pass

    f.close()

if __name__ == '__main__':
    main("54c0253b5c1f9b7701e73f142e17df52:11:60326808", "[Top/Features/Arts]", "arts")
    main("54c0253b5c1f9b7701e73f142e17df52:11:60326808", "[Top/News/Sports]", "sports")
