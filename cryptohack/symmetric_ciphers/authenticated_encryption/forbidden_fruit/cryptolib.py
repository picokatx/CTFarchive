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

def encrypt(plaintext):
    out = json_get(f"https://aes.cryptohack.org/forbidden_fruit/encrypt/{plaintext}")
    if ("error" in out.keys()):
        return bytes.fromhex(out['ciphertext']), b"", b"", b""
    else:
        return (
            bytes.fromhex(out['ciphertext']),
            bytes.fromhex(out['nonce']),
            bytes.fromhex(out['tag']),
            bytes.fromhex(out['associated_data'])
        )
def decrypt(nonce, ciphertext, tag, associated_data):
    out = json_get(f"https://aes.cryptohack.org/paper_plane/forbidden_fruit/decrypt/{nonce}/{ciphertext}/{tag}/{associated_data}")
    
    if ("plaintext" in out.keys()):
        return out['plaintext']
    else:
        return out['error']

KEY =  b"key{the_aes_key}"
FLAG = b"crypto{aes_flag}"
PLAIN =b"Howdy! I'm Flowe"
def pool(func, iters: int, workers: int, *args):
    return p_map(func, *(range(0,iters), *args), num_cpus=workers, total=iters)