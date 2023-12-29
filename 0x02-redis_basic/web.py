#!/usr/bin/env python3
"""
This module contains a function
that returns HTML content of a url
"""
import redis
import requests
from typing import Callable
from functools import wraps


redis_instance = redis.Redis()


def counter(func: Callable) -> Callable:
    """
    decorator to store how many times
    a url is accessed
    """
    @wraps(func)
    def wrapper(*args):
        """
        wrapper function to store key
        and value in redis
        """
        redis_instance.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = func(*args)
        redis_instance.set(f'count:{args[0]}', 0)
        redis_instance.setex(f'result:{args[0]}', 10, result)
        return result
    return wrapper


@counter
def get_page(url: str) -> str:
    """
    retrieves html content from
    a url
    """
    if url != "":
        return response = requests.get(url).text
