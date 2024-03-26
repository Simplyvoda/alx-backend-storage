#!/usr/bin/env python3
'''Task 11 module
'''


def schools_by_topic(mongo_collection, topic):
    '''
    Returns a list of schools from the MongoDB
    collection that have a specific topic.
    '''
    return list(mongo_collection.find({'topics': topic}))
