# TODO: may as well make this an entire library now that I need an ext file
import os
from Crypto.Util.Padding import pad, unpad
from datetime import datetime, timedelta
from Crypto.Cipher import AES
from os import urandom
import requests
from Crypto.Util.number import long_to_bytes, bytes_to_long
import json
from tqdm import tqdm
def json_get(url):
    return json.loads(requests.get(url).content.decode())
def xor(a, b):
    return long_to_bytes(bytes_to_long(a) ^ bytes_to_long(b))
def repeat_xor(a, b):
    return bytes(x ^ y for x,y in zip(a, b * (1 + len(a) // len(b))))
def encrypt():
    return bytes.fromhex(json_get(f"https://aes.cryptohack.org/stream_consciousness/encrypt/")['ciphertext'])
from p_tqdm import p_map
from multiprocessing import Pool
def temp(a):
    return encrypt()
def run():
    return p_map(temp, range(0,100), num_cpus=16)