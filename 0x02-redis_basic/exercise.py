#!/usr/bin/env python3
"""
Initiating Redis
"""
import redis


class Cache:
    '''Initiating the Redis class
    '''
    def __init__(self) -> None:
        '''Inititalizes a Cache instance
        '''
        self._redis = redis.Redis()
        self._redis.flushdb(True)
