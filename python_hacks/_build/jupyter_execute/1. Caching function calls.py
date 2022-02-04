#!/usr/bin/env python
# coding: utf-8

# # Caching function calls

# There are a few different alternatives and settings when it comes to using caching features from the 'functools' library. I tend to default to 'lru_cache' in most cases, where LRU stands for least recently used (i.e. remove the oldest unused values first).

# In[1]:


from functools import lru_cache


# For a much more detailed explanation of the different types of caching and a deep dive into 'lru_cache' in particular and how it works I'd highly recommend checking out: https://realpython.com/lru-cache-python/

# ## Recursion

# Using caching can drastically reduce compution times for highly recursive code. A simple toy example commonly used for demonstration is calculating Fibonacci numbers. The time taken to run this function recursively from scratch each time blows up exponentially (if you want to experiment and see for yourself run this in Colab and experiment).

# In[2]:


def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

@lru_cache(maxsize=2)
def fib_cached(n: int) -> int:
    if n < 2:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)


# Lets test out the difference...

# In[3]:


from timeit import timeit

n = 36

for fn in ["fib", "fib_cached"]:
    time_taken_secs = timeit(
        f"{fn}({n})",
        setup="from __main__ import fib, fib_cached",
        number=1,
    )
    print(f"Time taken to run {fn}: {time_taken_secs:.6f} seconds")


# In[4]:


fib_cached(36)


# # Singleton Factory

# While come people consider using Singletons an anti-pattern, I've found they can be useful at times. For example when using a class for all of your configuration.

# In[5]:


from os import getenv
from pydantic import BaseSettings


class DevSettings(BaseSettings):
    VAR: str = 'x'

class TestSettings(
    DevSettings, # This way we only overwrite settings we want to change
):
    VAR: str = 'y'

class ProdSettings(DevSettings):
    VAR: str = 'z'

@lru_cache(maxsize=1)
def get_settings() -> DevSettings | TestSettings | ProdSettings:
    match getenv("DEPLOYED_ENVIRONMENT"):
        case "TEST":
            return TestSettings()
        case "PROD":
            return ProdSettings()
        case _:
            return DevSettings()


# In[6]:


settings = get_settings()

print(settings.VAR)


# If we keep using our 'get_settings' function in our other scripts it will keep returning the result without re-calculating it each time. We can also test this by checking the identity of the object:

# In[7]:


a = DevSettings()
b = DevSettings()

id(a) == id(b)


# In[8]:


c = get_settings()
d = get_settings()

id(c) == id(d)


#  
