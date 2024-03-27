#!/usr/bin/env python3
"""
Initiating Redis
"""
import redis
import uuid


class Cache:
    '''Initiating the Redis class
    '''
    def __init__(self) -> None:
        '''Inititalizes a Cache instance
        '''
        self._redis = redis.Redis()
        self._redis.flushdb(True)


    def store(data: Union[str, bytes, int, float]) -> str:
        '''Stores a value in redis data storage and returns the key
        '''
        random_key = str(uuid.uuid4())
        _redis.set(random_key, data)
        return random_key
