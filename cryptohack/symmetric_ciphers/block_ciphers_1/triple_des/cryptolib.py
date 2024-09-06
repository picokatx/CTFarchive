# TODO: may as well make this an entire library now that I need an ext file
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
from multiprocessing import Pool

def json_get(url) -> dict:
    return json.loads(requests.get(url).content.decode())
def xor(a, b):
    return long_to_bytes(bytes_to_long(a) ^ bytes_to_long(b))
def repeat_xor(a, b):
    return bytes(x ^ y for x,y in zip(a, b * (1 + len(a) // len(b))))
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

def encrypt(key, ciphertext):
    return bytes.fromhex(json_get(f"https://aes.cryptohack.org/triple_des/encrypt/{key.hex()}/{ciphertext.hex()}")['ciphertext'])
def send_msg(ciphertext, m0, c0):
    return json_get(f"https://aes.cryptohack.org/paper_plane/send_msg/{ciphertext}/{m0}/{c0}")
def padding_oracle(ciphertext, m0, c0):
    return list(send_msg(ciphertext, m0, c0).values())[0]=="Message received"

KEY =  b"key{the_aes_key}"
FLAG = b"crypto{aes_flag}"
PLAIN =b"Howdy! I'm Flowe"
def pool(func, iters: int, workers: int):
    return p_map(func, range(0,iters), num_cpus=workers)