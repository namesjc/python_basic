from functools import wraps


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
