import time
import random
import string

import requests

SECS_IN_A_DAY = 86400


def make_get_req(url: str) -> str:
    r = requests.get(url)
    return r.text


def check_validity(api_key):
    try:
        curr_api_key = make_get_req('https://fl-shehry3894.herokuapp.com/ghtk')
        curr_api_time = decode_api_key(curr_api_key)
        api_key_time = decode_api_key(api_key)
        return curr_api_time < api_key_time
    except:
        raise Exception('Unable to check validity!')

    return False


def gen_api_key(days_from_now: int = 0):
    max_t = int(time.time() + days_from_now * SECS_IN_A_DAY)
    reversed_t = str(max_t)[::-1]
    print(max_t, reversed_t)

    api_key = []
    for digit in str(reversed_t):
        key = list(gen_rand_str(10))
        key[int(digit)] = '-'
        api_key.append(''.join(key))

    return '_'.join(api_key)


def gen_rand_str(length: int):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def decode_api_key(key_: str):
    num = ''
    for str_ in key_.split('_'):
        idx = str_.index('-')
        num += str(idx)

    return int(num[::-1])
