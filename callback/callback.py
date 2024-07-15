def greeting(name):
    print(f"Hello, {name}!")


def process_name(name: str, callback):
    # 执行其他操作...
    callback(name)  # 调用回调函数


# 使用回调函数
process_name("Alice", greeting)
