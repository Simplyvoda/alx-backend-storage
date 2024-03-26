#!/usr/bin/env python3
'''
Task 8
'''


def list_all(mongo_collection):
    '''
    List all documents in the given MongoDB collection.

    Args:
    mongo_collection: pymongo collection object.

    Returns:
    A list of documents in the collection.
    '''
    documents = list(mongo_collection.find())
    return documents
