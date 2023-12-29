#!/usr/bin/env python3
"""
This module contains a function
created to play with redis db
"""
import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    decorator that returns number of times a method
    is called
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        if not self._redis.exists(key):
            self._redis.set(key, 0)
        result = method(self, *args, **kwargs)
        self._redis.incr(key, 1)
        return result
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    decorator that returns a log containing input and output
    of method called
    """
    @wraps(method)
    def wrapper(self, *args):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        result = method(self, *args)
        self._redis.rpush(output_key, result)
        return result
    return wrapper


def replay(method: Callable):
    """
    returns a summarised log of
    method called
    """
    if method is None or not hasattr(method, '__self__'):
        return
    redis_store = getattr(method.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    method_name = method.__qualname__
    call_count = redis_store.get(method_name)
    input_key = f"{method_name}:inputs"
    output_key = f"{method_name}:outputs"

    print(f"{method_name} was called {call_count.decode('utf-8')} times:")

    input_list = redis_store.lrange(input_key, 0, -1)
    output_list = redis_store.lrange(output_key, 0, -1)

    full_list = zip(input_list, output_list)

    for in_value, out_value in full_list:
        print(f"{method_name}(*{in_value.decode('utf-8')}) -> "
              f"{out_value.decode('utf-8')}")


class Cache:
    """
    This class contains methods
    that interact with redis
    """
    def __init__(self):
        """
        initialises the class object
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        stores a random key in redis with data
        entered as an argument
        """
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str, fn: Callable = None):
        """
        Performs a function on data
        or returns data as is if fn not
        available
        """
        if not self._redis.exists(key):
            return None

        data = self._redis.get(key)
        if fn:
            return fn(data)
        else:
            return data

    def get_str(self, key: str):
        """
        formats the data to return
        a string
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str):
        """
        formats data to return
        int
        """
        return self.get(key, fn=int)
