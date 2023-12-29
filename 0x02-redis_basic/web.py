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
    def wrapper(url: str) -> str:
        """
        wrapper function to store key
        and value in redis
        """
        count_key = f"count:{url}"
        result_key = f"result:{url}"

        if not redis_instance.exists(count_key):
            redis_instance.set(count_key, 0)

        redis_instance.incr(count_key)
        result = redis_instance.get(result_key)
        if result:
            return result.decode('utf-8')

        result = func(url)
        redis_instance.setex(result_key, 10, result)
        return result
    return wrapper


@counter
def get_page(url: str) -> str:
    """
    retrieves html content from
    a url
    """
    return requests.get(url).text
