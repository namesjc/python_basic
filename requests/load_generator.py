import time
import random
import threading
import requests

endpoints = ("index", "search?q=test", "explore", "user/marco", "user/adiachan")
HOST = "https://xxx/"
# Base64 encode credentials
cred =  "Basic " + ""
# Set header parameters
headers = {
   "Accept": "application/json",
   "Content-Type": "application/json",
   "Authorization" : cred
}


def run():
    while True:
        try:
            target = random.choice(endpoints)
            response = requests.request("GET", HOST + target, headers=headers)
            print(response.status_code)
        except requests.RequestException:
            print("cannot connect", HOST)
            time.sleep(1)


if __name__ == "__main__":
    for _ in range(5):
        thread = threading.Thread(target=run)
        thread.daemon = True
        thread.start()

    while True:
        time.sleep(1)
