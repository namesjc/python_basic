# Decorators
# A decorator is a function that takes another function as an argument and returns another function
# Decorating a function allows us easily add functionality to our existing functions by adding that function inside of a wrapper
from functools import wraps

# def decorator_func(msg):
#     def wrapper_func():
#         print(msg)
#     return wrapper_func


def decorator_func(original_func):
    def wrapper_func(*args, **kwargs):
        print(f'wrapper executed this before "{original_func.__name__}"')
        return original_func(*args, **kwargs)
    return wrapper_func


# class decorator_class(object):

#     def __init__(self, original_func):
#         self.original_func = original_func

#     def __call__(self, *args, **kwargs):
#         print(
#             f'call method executed this before "{self.original_func.__name__}"')
#         return self.original_func(*args, **kwargs)


# def display():
#     print('display function ran')


# decorated_display = decorator_func(display)

# decorated_display()


def my_logger(orig_func):
    import logging
    logging.basicConfig(
        filename=f'{orig_func.__name__}.log', level=logging.INFO)

    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        print(list(args))
        logging.info(f'Ran with args {args}, and kwargs {kwargs}')
        return orig_func(*args, **kwargs)

    return wrapper


def my_timer(orig_func):
    import time

    @wraps(orig_func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = orig_func(*args, **kwargs)
        t2 = time.time() - t1
        print(f'{orig_func.__name__} ran in {t2} sec')
        return result

    return wrapper


@my_logger
# this line is equivalent to 'display = decorator_func(display)'
def display():
    return 'display function ran'


display()

import time


@my_logger
# we can re-use this decorate anytime you want to add that loggin functionality to any new function
def display_info(name, age):
    time.sleep(1)
    print(f'display_info ran with arguments({name}, {age})')


display_info('Test', 30)
