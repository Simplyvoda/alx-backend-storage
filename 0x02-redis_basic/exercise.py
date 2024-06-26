#!/usr/bin/env python3
"""
Interacting with Redis NoSQL data storage
"""
import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''Counts number of times a function is called
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        '''Wrapper method
        '''
        wrapper_key = method.__qualname__
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(wrapper_key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    '''decorator to store the history of inputs
    and outputs for a particular function.
    '''
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        '''Wrapper method
        '''
        input_key = method.__qualname__+":inputs"
        output_key = method.__qualname__+":outputs"
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_key, result)
        return result
    return wrapper


class Cache:
    '''Initiating the Redis class
    '''
    def __init__(self) -> None:
        '''Inititalizes a Cache instance
        '''
        self._redis = redis.Redis()
        self._redis.flushdb(True)


    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        '''Stores a value in redis data storage and returns the key
        '''
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key


    def get(
            self,
            key: str,
            fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        '''Retrieves value from Redis storage
        '''
        data = self._redis.get(key)
        return fn(data) if fn is not None else data


    def get_str(self, key: str) -> str:
        '''Converts value to string
        '''
        return self.get(key, lambda x: x.decode('utf-8'))


    def get_int(self, key: str) -> int:
        '''Converts value to integer
        '''
        return self.get(key, lambda x: int(x))
