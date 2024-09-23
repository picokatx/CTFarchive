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
import base64
from math import log2
import random
import math
import sympy
from math import prod
from string import ascii_lowercase, ascii_uppercase, ascii_letters
from sympy.ntheory.factor_ import pollard_rho, pollard_pm1
from sympy.ntheory.residue_ntheory import _discrete_log_pollard_rho
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
    r = remote("83.136.254.243", 54909)
    r.recvuntil(b"> ")
    return r
def htb_rhome_get_params(r: remote):
    r.send(b"1\n")
    m = r.recvuntil(b"> ")
    temp = m.split(b"\n")
    p = int(temp[0][4:])
    g = int(temp[1][4:])
    A = int(temp[2][4:])
    B = int(temp[3][4:])
    return (p, g, A, B)
def htb_rhome_reset_params(r: remote):
    r.send(b"2\n")
    return r.recvuntil(b"> ")
def htb_rhome_get_flag(r: remote):
    r.send(b"3\n")
    return bytes.fromhex(r.recvuntil(b"> ").split(b"\n")[0][12:].decode())

def b64d(s):
    return base64.b64decode(s).decode()
def hxd(s):
    return bytes.fromhex(s).decode()
def ld(s):
    return long_to_bytes(s)
def ud(s):
    return "".join([chr(b) for b in s])
def b64e(s):
    return base64.b64encode(s).decode()
def hxe(s):
    return s.encode().hex()
def le(s):
    return bytes_to_long(s)
def ue(s):
    return [ord(b) for b in s]

def gcd(a, b):
    q0, q1 = a, b
    s0, s1 = 1, 0
    t0, t1 = 0, 1
    while q1!=0:
        q = q0 // q1
        q0, q1 = q1, q0 - q*q1
        s0, s1 = s1, s0 - q*s1
        t0, t1 = t1, t0 - q*t1
    return s0, t0, q0
def lcm(a,b):
    return abs(a*b)//gcd(a,b)[0]
def mod_inv(a, n):
    temp = gcd(a,n)[0]
    if (temp<0):
        temp+=n
    return temp
def crt(C, N):
    total = 0
    modulo = prod(N)
    for n_i, c_i in zip(N, C):
        p = modulo // n_i
        total += c_i * mod_inv(p, n_i) * p
    return total % modulo
ascii32bit = "abcdefghijklmnopqrstuvwxyz.,!?' "
def ascii32bit_encode(s: str):
    acc = 0
    i = 0
    for c in s:
        acc+=(ascii32bit.index(c) if c in ascii32bit else 31)<<i
        i+=5
    return acc
# edge case where last char has leading zeros, need to adjust bit shift offset accordingly
def ascii32bit_decode(s: int):
    acc = s
    ans = ""
    n = round(log2(s)) - 5
    n = n+(5-n%5) if n%5!=0 else n
    for i in range(n, -1, -5):
        temp = acc >> i
        temp2 = temp << i
        ans=ascii32bit[temp]+ans
        acc -= temp2
    return ans
def pq_from_den(d, e, n):
    k = d*e-1
    if (k%2==0):
        r = k
        t = 0
        while (r%2==0):
            r = r >> 1
            t+=1
        success = False
        y = -1
        for i in range(1,101):
            g = -1
            g = random.randrange(0,n)
            y = pow(g,r,n)
            if y==1 or y==n-1:
                continue
            for j in range(1, t):
                x = pow(y,2,n)
                if x==1:
                    success = True
                    break
                if x==n-1:
                    continue
                y = x
            x = pow(y, 2, n)
            if (x==1):
                success=True
                break
        if (success):
            p = gcd(y-1, n)[0]
            q = n//p
            return p, q
        else:
            assert False, "not found"
    else:
        assert False, "not found"
KEY =  b"key{the_aes_key}"
FLAG = b"crypto{aes_flag}"
PLAIN =b"Howdy! I'm Flowe"
IVNONCE = b"nonce{a}"
# use sympy integer_nthroot
# use sympy pollard_pm1
def pollard(n):
    a = 2
    i = 2
    while(True):
        a = (a**i) % n
        d = math.gcd((a-1), n)
        if (d > 1):
            return d
        i += 1
morse_codec = ascii_uppercase+"0123456789"
morse_table = ['.-', '-...', '-.-.', '-..', '.', '..-.', '--.', '....', '..', '.---', '-.-', '.-..', '--', '-.', '---', '.--.', '--.-', '.-.', '...', '-', '..-', '...-', '.--', '-..-', '-.--', '--..', '-----', '.----', '..---', '...--', '....-', '.....', '-....', '--...', '---..', '----.']
VALID_FLAG_CHARS = "".join([chr(c) for c in range(32,128)]).encode()
def pool(func, iters: int, workers: int, *args):
    return p_map(func, *(range(0,iters), *args), num_cpus=workers, total=iters)
def imap(func, iters: int, *args):
    return [func(*([i]+[s[i] for s in args])) for i in tqdm(range(0, iters))]