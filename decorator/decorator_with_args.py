from functools import wraps


# example 1
def repeat(times):
    ''' call a function a number of times '''
    def decorate(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # print(list(args)[-1])
            for _ in range(times):
                result = fn(*args, **kwargs)
            return result
        return wrapper
    return decorate


@repeat(10)
def say(message):
    ''' print the message
    Arguments
        message: the message to show
    '''
    print(message)


say('Hi')


# example 2
def forty_two():
    return 42


def my_decorator(f):
    def inner(*args, **kwargs):
        print('before function')
        response = f(*args, **kwargs)
        print('after function')
        return response
    print('decorating', f)
    return inner


@my_decorator
def my_func(a, b):
    print('in function')
    return a + b


print(my_func(1, 2))
