import os
from Crypto.Util.Padding import pad, unpad
from datetime import datetime, timedelta
from Crypto.Cipher import AES
from Crypto.Cipher import ARC4
from os import urandom
import requests
from Crypto.Util.number import long_to_bytes, bytes_to_long
import json
from tqdm import tqdm
from p_tqdm import p_map
from pwnlib.tubes.remote import remote
from multiprocessing import Pool

def json_get(url) -> dict:
    return json.loads(requests.get(url).content.decode())
def xor(a, b):
    return long_to_bytes(bytes_to_long(a) ^ bytes_to_long(b))
def repeat_xor(a, b):
    return bytes(x ^ y for x,y in zip(a, b * (1 + len(a) // len(b))))

def json_recv(r: remote) -> dict:
    line = r.readline()
    return json.loads(line.decode())

def json_send(r: remote, hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

def is_utf8(s: str):
    try:
        s.decode('utf-8')
        return True
    except UnicodeError:
        return False

def rc4_fms_possible_key_bit(key, c):
    s = [i for i in range(256)]
    j = 0
    for i in range(len(key)):
        j = (j + s[i] + key[i]) % 256
        s[i], s[j] = s[j], s[i]
    return (c[0] - j - s[len(key)]) % 256
def hello_world():
    r = remote("socket.cryptohack.org", 13421)
    # r = remote("localhost", 13421)
    r.recvline()
    return r

KEY =  b"key{the_aes_key}"
FLAG = b"crypto{aes_flag}"
PLAIN =b"Howdy! I'm Flowe"
IVNONCE = b"nonce{a}"

def pool(func, iters: int, workers: int, *args):
    return p_map(func, *(range(0,iters), *args), num_cpus=workers, total=iters)
def imap(func, iters: int, *args):
    return [func(*([i]+[s[i] for s in args])) for i in tqdm(range(0, iters))]