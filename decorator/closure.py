# Closures

# Wikipedia says, "A closure is a record storing a function together with
# an environment: a mapping associating each free variable of the function
# with the value or storage location to which the name was bound when the
# closure was created. A closure, unlike a plan function, allows the
# function to access those captured variables through the closure's
# reference to them, even when the function is inviled outside their
# scope."

# A closure is an inner function that remembers and has accesses to variables in
# the local scope in which it was created even after the outer function has finished executing

# def outer_func(msg):
#     message = msg

#     def inner_func():
#         print(message)

#     return inner_func


# hi_func = outer_func('Hi')
# hello_func = outer_func('Hello')

# hi_func()
# hello_func()

import logging
logging.basicConfig(filename='example.log', level=logging.INFO)


def logger(func):
    def log_func(*args):
        logging.info(f'Running "{func.__name__}" with arguments {args}')
        print(func(*args))
    return log_func


def add(x, y):
    return x + y


def sub(x, y):
    return x - y


add_logger = logger(add)
sub_logger = logger(sub)

add_logger(3, 4)
add_logger(4, 5)

sub_logger(10, 5)
sub_logger(20, 10)
