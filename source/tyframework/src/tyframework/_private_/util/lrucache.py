# -*- coding=utf-8 -*-

# import collections
import functools
from heapq import nsmallest
from operator import itemgetter


# from itertools import ifilterfalse

class Counter(dict):
    'Mapping where default values are zero'

    def __missing__(self, key):
        return 0


# def lru_cache(maxsize=100, cache_key_args_index=1):
#     
#     '''Least-recently-used cache decorator.
# 
#     Arguments to the cached function must be hashable.
#     Cache performance statistics stored in f.hits and f.misses.
#     Clear the cache with f.clear().
#     http://en.wikipedia.org/wiki/Cache_algorithms#Least_Recently_Used
# 
#     '''
#     maxqueue = maxsize * 10
#     def decorating_function(user_function,
#             len=len, iter=iter, tuple=tuple, sorted=sorted, KeyError=KeyError):
#         cache = {}  # mapping of args to results
#         queue = collections.deque()  # order that keys have been used
#         refcount = Counter()  # times each key is in the queue
#         sentinel = object()  # marker for looping around the queue
# 
#         # lookup optimizations (ugly but fast)
#         queue_append, queue_popleft = queue.append, queue.popleft
#         queue_appendleft, queue_pop = queue.appendleft, queue.pop
# 
#         @functools.wraps(user_function)
#         def wrapper(*args, **kwds):
#             # cache key records both positional and keyword args
#             key = args[cache_key_args_index]
# 
#             # record recent use of this key
#             queue_append(key)
#             refcount[key] += 1
# 
#             # get cache entry or compute if not found
#             try:
#                 result = cache[key]
#                 wrapper.hits += 1
#             except KeyError:
#                 result = user_function(*args, **kwds)
#                 cache[key] = result
#                 wrapper.misses += 1
# 
#                 # purge least recently used cache entry
#                 if len(cache) > maxsize:
#                     key = queue_popleft()
#                     refcount[key] -= 1
#                     while refcount[key]:
#                         key = queue_popleft()
#                         refcount[key] -= 1
#                     del cache[key], refcount[key]
# 
#             # periodically compact the queue by eliminating duplicate keys
#             # while preserving order of most recent access
#             if len(queue) > maxqueue:
#                 refcount.clear()
#                 queue_appendleft(sentinel)
#                 for key in ifilterfalse(refcount.__contains__,
#                                         iter(queue_pop, sentinel)):
#                     queue_appendleft(key)
#                     refcount[key] = 1
# 
# 
#             return result
# 
#         def clearKey(*args):
#             for key in args :
#                 if key in cache:
#                     del cache[key]
# 
#         def clear():
#             cache.clear()
#             queue.clear()
#             refcount.clear()
#             wrapper.hits = wrapper.misses = 0
# 
#         wrapper.hits = wrapper.misses = 0
#         wrapper.clear = clear
#         wrapper.clearKey = clearKey
#         wrapper.cache = cache
#         wrapper.refcount = refcount
#         wrapper.queue = queue
# 
#         return wrapper
#     return decorating_function

def lfu_cache(maxsize=100, cache_key_args_index=1):
    '''Least-frequenty-used cache decorator.
 
    Arguments to the cached function must be hashable.
    Cache performance statistics stored in f.hits and f.misses.
    Clear the cache with f.clear().
    http://en.wikipedia.org/wiki/Least_Frequently_Used
 
    '''

    def decorating_function(user_function):
        cache = {}  # mapping of args to results
        use_count = Counter()  # times each key has been accessed

        @functools.wraps(user_function)
        def wrapper(*args, **kwds):
            key = args[cache_key_args_index]

            use_count[key] += 1

            # get cache entry or compute if not found
            try:
                result = cache[key]
                wrapper.hits += 1
            except KeyError:
                result = user_function(*args, **kwds)
                cache[key] = result
                wrapper.misses += 1

                # purge least frequently used cache entry
                if len(cache) > maxsize:
                    for key, _ in nsmallest(maxsize // 10,
                                            use_count.iteritems(),
                                            key=itemgetter(1)):
                        del cache[key], use_count[key]

            return result

        def clear_keys(args):
            for key in args:
                if key in cache:
                    del cache[key]

        def clear():
            cache.clear()
            use_count.clear()
            wrapper.hits = 0
            wrapper.misses = 0

        wrapper.hits = 0
        wrapper.misses = 0
        wrapper.use_count = use_count
        wrapper.cache = cache
        wrapper.clear = clear
        wrapper.clear_keys = clear_keys
        return wrapper

    return decorating_function
