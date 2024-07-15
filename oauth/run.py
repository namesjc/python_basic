import os
from urllib.parse import urlencode

import requests
from flask import Flask, jsonify, redirect, render_template, request, session
from oauthlib import oauth2

app = Flask(__name__)
app.secret_key = os.urandom(24)

OAUTH = {  # 配置参数，如果没有设置正确，OAuth流程就会失败
    "client_id": "blog",
    "client_secret": "LyeABvncUhtmBF5S0RxX8BfWfwbb5soo",
    "redirect_uri": "http://localhost:8080/callback/",
    "scope": "email",		# 表示OAuth请求授权的范围，Gitlab上选择了"api"
    "auth_url": "https://keycloak.adiachan.cn/auth/realms/jhipster/protocol/openid-connect/auth",
    "token_url": "https://keycloak.adiachan.cn/auth/realms/jhipster/protocol/openid-connect/token",
}
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"  # 允许使用HTTP进行OAuth


@app.route("/login/oauth/", methods=["GET"])
def oauth():
    """ 当用户点击该链接时,把用户重定向到Gitlab的OAuth2登录页面。 """
    client = oauth2.WebApplicationClient(OAUTH["client_id"])
    state = client.state_generator()    # 生成随机的state参数，用于防止CSRF攻击
    auth_url = client.prepare_request_uri(OAUTH["auth_url"],
                                          OAUTH["redirect_uri"],
                                          OAUTH["scope"],
                                          state)  # 构造完整的auth_url，接下来要让用户重定向到它
    session["state"] = state
    return redirect(auth_url)


@app.route("/callback/", methods=["GET"])
def oauth_callback():
    """ 用户在同意授权之后,会被Gitlab重定向回到这个URL。 """
    # 解析得到code
    client = oauth2.WebApplicationClient(OAUTH["client_id"])
    code = client.parse_request_uri_response(
        request.url, session["state"]).get("code")

    # 向Gitlab请求获取token
    body = client.prepare_request_body(code,
                                       redirect_uri=OAUTH["redirect_uri"],
                                       client_secret=OAUTH["client_secret"])
    r = requests.post(OAUTH["token_url"], body)
    access_token = r.json().get("access_token")
    print(access_token)

    return redirect("/")


@app.route("/logout/", methods=["GET"])
def logout():
    session.pop("username", None)
    return redirect("/")


@app.route("/", methods=["GET"])
def home():
    username = session.get("username")
    print(session)
    if username:
        context = {"title": "主页", "msg": "你已登录：{}".format(username),
                   "url": "/logout/", "url_name": "登出"}
        return jsonify(context)
    else:
        context = {"title": "主页", "msg": "你还没有登录。",
                   "url": "/login/oauth/", "url_name": "通过Gitlab登录"}
        return jsonify(context)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
