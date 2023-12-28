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
    @wraps(method)
    def wrapper(self, *args):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        result = method(self, *args)
        self._redis.rpush(output_key, result)
        return result
    return wrapper


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str, fn: Callable = None):
        if not self._redis.exists(key):
            return None

        data = self._redis.get(key)
        if fn:
            return fn(data)
        else:
            return data

    def get_str(self, key: str):
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str):
        return self.get(key, fn=int)
