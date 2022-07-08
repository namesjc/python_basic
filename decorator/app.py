from flask import Flask, request, abort

app = Flask(__name__)


def only_user_agent(user_agent):
    def inner_decorator(f):
        def wrapped(*args, **kwargs):
            print(request.user_agent.string)
            if user_agent not in request.user_agent.string.lower():
                abort(404)
            return f(*args, **kwargs)
        return wrapped
    return inner_decorator


@app.route('/')
@only_user_agent('curl')
def index():
    return 'Hello Curl!'


if __name__ == '__main__':
    app.run(debug=True)
