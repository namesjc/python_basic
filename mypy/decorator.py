# 定义一个简单的装饰器
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("Something is happening before the function is called.")
        result = func(*args, **kwargs)
        print("Something is happening after the function is called.")
        return result

    return wrapper


@my_decorator
def say_hello(name):
    print(f"Hello, {name}!")


# 调用装饰过的函数
say_hello("Bob")
