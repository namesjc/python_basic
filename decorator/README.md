# Python Decorator

## 1.Alerting Function Behavior

### Example #1: Injecting New Arguments

The following decorator injects the current time as a first argument into any functions it decorates:

```python
from datetime import datetime
def add_current_time(f):
    def wrapper(*args, **kwargs):
        return f(datetime.utcnow(), *args, **kwargs)
    return wrapper
```

Example usage:

```python
@add_current_time
def test(time, a, b):
    print('I received arguments', a, b, 'at', time)

>>> test(1, 2)
>>> I received arguments 1 2 at 2019-10-10 21:38:35.582887
```

The decorated function is written to accept a first `time` argument, but this argument is automatically added by the decorator, so the function is invoked with the remaining arguments, in this case `a` and `b`

### Example #2: Alerting the Return Value of a Function

Another very common task decorators are good for is to perform a conversion on the return value of the decorated function. If you have many functions that invoke a data conversion function before returning , you can move this conversion task to decorator to make the code in your functions simpler, less repetitive and easier to read. This can be implement to Flask:

```python
@app.route('/')
def index():
    return jsonify({'hello': 'world'})
```

 If your Flask application implements an API, you likely have many routes that end by returning a JSON payload, generated with the `jsonify()` function. Wouldn't it be nice if you could just return the dictionary, instead of having to include the `jsonify()`  call at the end of every view function? A `to_json` decorator can perform the conversion to JSON for you:

```python
@app.route('/')
@to_json
def index():
    return {'hello': 'world'}
```

Here the `index()` function returns the dictionary, which for Flask is an invalid response type. But the `to_json` decorator wraps the function, and has a chance to perform the conversion and update the response before it reaches Flask. Here is the complete application, including the implementation of this decorator:

```python
from flask import Flask, jsonify

app = Flask(__name__)

def to_json(f):
    def wrapper(*args, **kwargs):
        response = f(*args, **kwargs)
        if isinstance(response, (dict, list)):
            response = jsonify(response)
        return response
    return wrapper

@app.route('/')
@to_json
def index():
    return {'hello': 'world'}
```

The `wrapper()` function simply invokes the original function, called `f` in this context, and then checks if the return value is a dictionary or list, in which it calls `jsonify()`, effectively intercepting and fixing the return value before it is returned to the framework.

### Examples #3: Validation

Another useful technique that can be implemented with decorators is to perform any kind of validation before the decorated function is allowed to run. A very common example in a web application is to authenticate the user. If the validation/authentication task ends in a failure, then the decorated function is not invoked, and instead the decorator raises an error:

```python
>>> from flask import Flask, request, abort
>>> ADMIN_TOKEN = "youwillneverknow"
>>> def only_admins(f):
...     def wrapped(*args, **kwargs):
...         tokens = request.headers.get('X-Auth-Token')
...         if tokens != ADMIN_TOKEN:
...            abort(404) # not authorized
...         return f(*args, **kwargs)
...    return wrapped
...
>>>@app.route('/admin')
...@only_admins
...def admin_route():
...    return "only admins can access this route!"
...
```

In this example the `only_admins` decorator looks for a `X-Auth-Token` header in the incoming request, and then checks that it matches a  secret administrator token, that for simplicity I have set as a  constant. If the token header isn't present, or if it is present but the token does not match, then the `abort()` function from Flask is used to generate a 401 response and halt the request. Otherwise the  request is allowed to go through by invoking the decorated function.

## 2.Decorators with Arguments

Decorators with arguments are built on top of standard decorators. A decorator with arguments is defined as a function that returns a standard decorator.

```python
def my_decorator(arg):
    def inner_decorator(f):
        def wrapped(*args, **kwargs):
            print('before function')
            response = f(*args, **kwargs)
            print('after function')
            return response
        print('decorating', f, 'with argument', arg)
        return wrapped
    return inner_decorator
```

The decorator arguments are accessible to the inner decorator through a closure, exactly like how the `wrapped()` inner function can access `f`. And since closures extend to all levels of inner functions, `arg` is also accessible from within `wrapped()` if necessary.

Example usage:

```python
@my_decorator('foo')
def my_function(a, b):
    return a + b
```

The equivalent Python expression for this new decorator is:

```python
my_function = my_decorator('foo')(my_function)
```

### Example #1: Flask's Route Decorator

Write a simple version of Flask's route decorator:

```python
route_map = {}

def route(url):
    def inner_decorator(f):
        route_map[url] = f
        return f
    return inner_decorator
```

This implementation accumulates route to function mappings in a global `route_map`, dictionary. Since this is a function registration decorator, there is no need to wrap the decorated function, so the inner decorator just updates the route dictionary and then returns the `f` decorated function unmodified.

Example usage:

```python
@route('/')
def index():
    pass

@route('/user')
def get_users():
    pass
```

if you run the above example and then print `route_map`, this is what you would get:

```python
{
	'/': <function index at 0x7a9bc16a8cb0>,
    '/users': <function get_users at 0x7a9bc16a8dd0>
}
```

To make this example a bit more realistic we can add `methods` optional argument, which also records HTTP methods in the route map:

```python
route_map = {}

def route(url, methods=['GET']):
    def inner_decorator(f):
        if url not in route_map:
            route_map[url] = {}
        for method in methods:
            route_map[url][method] = f
        return f
    return inner_decorator
```

With this improved version you can build more advanced mappings such as this:

```python
@route('/')
def index():
    pass

@route('/user', methods=['GET', 'POST'])
def get_users():
    pass

@route('/users', methods=['DELETE'])
def delete_users():
    pass
```

The `route_map` for the above example would be:

```python
{
    '/': {
        'GET': <function index at 0x7a9bc16a8680>
    },
    '/users': {
        'GET': <function get_users at 0x7a9bc16a84d0>,
        'POST': <function get_users at 0x7a9bc16a84d0>,
        'DELETE': <function delete_users at 0x7a9bc16a8a70>
    }
}
```

### Example #2: Permission Checking

A common pattern in web applications is to check whether a client request has permission to perform the action it is requesting. These checks involve obtaining the value of a header or cookie included in the request to determine the  identify of the client, and then once the client is known an application specific method is used to determine if permission can be grant or not.

For example, that we want to only allow requests made by a specific user agent to go through, while all other users agents are rejected:

```python
from flask import Flask, request, abort

app = Flask(__name__)

def only_user_agent(user_agent):
    def inner_decorator(f):
        def wrapped(*args, **kwargs):
            if user_agent not in request.user_agent.string.lower():
                abort(404)
            return f(*args, **kwargs)
        return wrapped
    return inner_decorator

@app.route('/')
@only_user_agent('curl')
def index():
    return 'Hello Curl!'
```

If you run the above application and then navigate with the browser to `http://localhost:5000` you will get a "Not Found" error. But if ou access the same URL with curl from a terminal, the request is allowed to execute:

```sh
$ curl http://localhost:5000
Hello Curl!
```

