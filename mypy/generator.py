# squared = (x**2 for x in range(10))
# print(type(squared))
#
# for n in squared:
#     print(n)


def fibonacci(n):
    """
    Generate the first n numbers in the Fibonacci sequence
    """
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


if __name__ == "__main__":
    fib_generator = fibonacci(10)

    for num in fib_generator:
        print(num)
