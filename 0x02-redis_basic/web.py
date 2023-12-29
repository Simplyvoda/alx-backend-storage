#!/usr/bin/env python3
"""
This module contains a function
that returns HTML content of a url
"""
import redis
import requests
from typing import Callable

redis_instance = redis.Redis()


def counter(func: Callable) -> Callable:
    """
    decorator to store how many times
    a url is accessed
    """
    def wrapper(*args):
        result = func(*args)
        key = f"count:{args[0]}"
        if redis_instance.exists(key):
            redis_instance.incr(key, 1)
        else:
            redis_instance.set(key, 0, ex=10)
            redis_instance.incr(key, 1)
        return result
    return wrapper


@counter
def get_page(url: str) -> str:
    """
    retrieves html content from
    a url
    """
    if url != "":
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text
            return html_content
    return "Failed to retrieve the page"
