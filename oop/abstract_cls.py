import requests
from time import time
from abc import ABC, abstractmethod


class MacmaToken(ABC):
    def __init__(self):
        self.deadline = 0
        self._token = None

    @abstractmethod
    def refresh_token(self):
        raise NotImplementedError(
            "Called refresh_token of abstract MacmaToken")

    def get(self):
        if self.deadline - time() < 60 or not self._token:
            self.refresh_token()
        return self._token

    def get_if_present(self):
        return self._token if self.deadline - time() < 60 else None

# Just the given token, cannot be refreshed


class BareMacmaToken(MacmaToken):
    def refresh_token(self):
        pass

    def __init__(self, token, deadline=0xEFFFFFFF):
        super()
        self._token = token
        self.deadline = deadline


class MacmaClientToken(MacmaToken):
    def __init__(self, base_url, tenant_id, client_id, client_secret, scope, verify_ssl=True, token=None):
        super()
        self.base_url = base_url
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.verify_ssl = verify_ssl
        self._token = token
        self.deadline = 120

    def refresh_token(self):
        body = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': self.scope
        }
        resp = requests.request('POST',
                f"{self.base_url}/access-management/v1/tenants/{ self.tenant_id }/openid-connect/token",
                data=body, verify=self.verify_ssl, headers=USER_AGENT_HEADERS).json()
        self._token = resp['access_token']
        self.deadline = int(resp['expires_in']) + time() - 1
        return self._token

    def get(self):
        if not self._token or self.deadline - time() < 50:
            self.refresh_token()
        return self._token


BareMacmaToken("test")
