import requests
from requests_kerberos import HTTPKerberosAuth, OPTIONAL
from requests_ntlm import HttpNtlmAuth
import ssl

# download from windows os
context = ssl.create_default_context()
der_certs = context.get_ca_certs(binary_form=True)
pem_certs = [ssl.DER_cert_to_PEM_cert(der) for der in der_certs]
with open("wincacerts.pem", 'w') as outfile:
    for pem in pem_certs:
        outfile.write(pem + '\n')

# basic auth
# Base64 encode cred
cred = "Basic " + " "
# Set header parameters
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": cred
}

url = ""

endpoint = ""

response = requests.request("GET", url + endpoint, headers=headers)

# kerberos auth
kerberos_auth = HTTPKerberosAuth(mutual_authentication=OPTIONAL)
url = "https://sharepoint.com/event management.xlsx"

r = requests.get(url, auth=kerberos_auth, verify="wincacerts.pem")

# ntlm auth
r = requests.get(url, auth=HttpNtlmAuth('username', 'password'), verify="wincacerts.pem")


# download sharepoint file
open('event management.xlsx', 'wb').write(r.content)
