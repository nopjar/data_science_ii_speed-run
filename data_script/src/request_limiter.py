import requests
from time import time, sleep

REQUEST_LIMIT = 90
TIME_THRESHOLD = 30
TIMEOUT = 10
REQUESTS = []

def clear_requests():
    current_time = time()
    expired = [timestamp for timestamp in REQUESTS if current_time - timestamp > TIME_THRESHOLD]
    for key in expired:
        del REQUESTS[key]


def get(url):
    clear_requests()
    if len(REQUESTS) > REQUEST_LIMIT:
        print('Ran into rate limit. Waiting before doing more requests...')
        while len(REQUESTS) > REQUEST_LIMIT:
            sleep(TIMEOUT)
            clear_requests()
    REQUESTS.append(time())
    return requests.get(url)
