import logging
import flask

from flask import Flask, jsonify
from flask_pyoidc.provider_configuration import ClientMetadata
from flask_pyoidc.provider_configuration import ClientRegistrationInfo
from flask_pyoidc import OIDCAuthentication
from flask_pyoidc.provider_configuration import ProviderConfiguration
from flask_pyoidc.provider_configuration import ProviderMetadata
from flask_pyoidc.user_session import UserSession

app = Flask(__name__)
app.config.update({'OIDC_REDIRECT_URI': 'http://localhost:8080/redirect_uri',
                  'SECRET_KEY': 'dev_key',
                   'DEBUG': True
                   })

# Static Client Registration, comment out if you want to use dynamic client
# registration.
client_metadata = ClientMetadata(client_id='blog', client_secret='LyeABvncUhtmBF5S0RxX8BfWfwbb5soo',
                                 post_logout_redirect_uris=['http://localhost:8080/logout'])

provider_config = ProviderConfiguration(
    issuer='https://keycloak.adiachan.cn/auth/realms/jhipster', client_metadata=client_metadata)

auth = OIDCAuthentication({'default': provider_config})
# auth.init_app(app)

# Do you want to use client credentials flow?
# token_response = auth.clients['default'].client_credentials_grant()
# access_token = token_response['access_token']
# print(access_token)

# For browser based clients.


@auth.oidc_auth('default')
@app.route('/')
def login():
    user_session = UserSession(flask.session)
    return jsonify(access_token=user_session.access_token,
                   id_token=user_session.id_token,
                   userinfo=user_session.userinfo)


# For browser based clients.
@auth.oidc_auth('default')
@app.route('/web')
def web_resource():
    return jsonify(data='data from web resource')


# For browser-less user-agents like curl.
@auth.token_auth('default', scopes_required=['read', 'write'])
@app.route('/dev')
def dev_resource():
    logging.debug(auth.current_token_identity)
    return jsonify(data='data from dev resource')


# For both oidc_auth and token_auth.
@auth.access_control('default', scopes_required=['read', 'write'])
@app.route('/shared')
def shared_resource():
    return jsonify(data='data from shared resource')


# Optionally, have you passed post_logout_redirect_uris in client registration? If yes,
# then create their view functions also.
@auth.oidc_logout
@app.route('/logout')
def logout1():
    return jsonify(data='user is logged out')


if __name__ == '__main__':
    auth.init_app(app)
    app.run(port=8080)
