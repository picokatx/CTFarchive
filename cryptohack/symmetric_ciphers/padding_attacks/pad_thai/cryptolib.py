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
from pwnlib.tubes.remote import remote
import json


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

def encrypt(r: remote) -> bytes:
    json_send(r, {"option": "encrypt"})
    return bytes.fromhex(json_recv(r)['ct'])
def unpad(r: remote, ct: str) -> bool:
    json_send(r, {"option": "unpad", 'ct': ct})
    return json_recv(r)['result']
def check_message(r: remote, msg: str) -> bool:
    json_send(r, {"option": "check", 'message': msg})
    out = json_recv(r)
    return out['error'] if "error" in out.keys() else out['flag']

def padding_oracle(r: remote, ciphertext: str):
    return unpad(r, ciphertext)

KEY =  b"key{the_aes_key}"
FLAG = b"crypto{aes_flag}"
PLAIN =b"Howdy! I'm Flowe"
def pool(func, iters: int, workers: int, *args):
    return p_map(func, *(range(0,iters), *args), num_cpus=workers, total=iters)
def imap(func, iters: int, *args):
    return [func(*([i]+[s[i] for s in args])) for i in tqdm(range(0, iters))]


THAI_MACOS_CODEC = {
    0x00: ["\u0000"],  # NULL
    0x01: ["\u0001"],  # START OF HEADING
    0x02: ["\u0002"],  # START OF TEXT
    0x03: ["\u0003"],  # END OF TEXT
    0x04: ["\u0004"],  # END OF TRANSMISSION
    0x05: ["\u0005"],  # ENQUIRY
    0x06: ["\u0006"],  # ACKNOWLEDGE
    0x07: ["\u0007"],  # ALERT
    0x08: ["\u0008"],  # BACKSPACE
    0x09: ["\u0009"],  # CHARACTER TABULATION
    0x0a: ["\u000a"],  # END OF LINE
    0x0b: ["\u000b"],  # LINE TABULATION
    0x0c: ["\u000c"],  # FORM FEED
    0x0d: ["\u000d"],  # CARRIAGE RETURN
    0x0e: ["\u000e"],  # LOCKING-SHIFT ONE
    0x0f: ["\u000f"],  # LOCKING-SHIFT ZERO
    0x10: ["\u0010"],  # DATA LINK ESCAPE
    0x11: ["\u0011"],  # DEVICE CONTROL ONE
    0x12: ["\u0012"],  # DEVICE CONTROL TWO
    0x13: ["\u0013"],  # DEVICE CONTROL THREE
    0x14: ["\u0014"],  # DEVICE CONTROL FOUR
    0x15: ["\u0015"],  # NEGATIVE ACKNOWLEDGE
    0x16: ["\u0016"],  # SYNCHRONOUS IDLE
    0x17: ["\u0017"],  # END OF TRANSMISSION BLOCK
    0x18: ["\u0018"],  # CANCEL
    0x19: ["\u0019"],  # END OF MEDIUM
    0x1a: ["\u001a"],  # SUBSTITUTE
    0x1b: ["\u001b"],  # ESCAPE
    0x1c: ["\u001c"],  # FILE SEPARATOR
    0x1d: ["\u001d"],  # GROUP SEPARATOR
    0x1e: ["\u001e"],  # INFORMATION SEPARATOR TWO
    0x1f: ["\u001f"],  # INFORMATION SEPARATOR ONE
    0x20: ["\u0020"],	# SPACE
    0x21: ["\u0021"],	# EXCLAMATION MARK
    0x22: ["\u0022"],	# QUOTATION MARK
    0x23: ["\u0023"],	# NUMBER SIGN
    0x24: ["\u0024"],	# DOLLAR SIGN
    0x25: ["\u0025"],	# PERCENT SIGN
    0x26: ["\u0026"],	# AMPERSAND
    0x27: ["\u0027"],	# APOSTROPHE
    0x28: ["\u0028"],	# LEFT PARENTHESIS
    0x29: ["\u0029"],	# RIGHT PARENTHESIS
    0x2A: ["\u002A"],	# ASTERISK
    0x2B: ["\u002B"],	# PLUS SIGN
    0x2C: ["\u002C"],	# COMMA
    0x2D: ["\u002D"],	# HYPHEN-MINUS
    0x2E: ["\u002E"],	# FULL STOP
    0x2F: ["\u002F"],	# SOLIDUS
    0x30: ["\u0030"],	# DIGIT ZERO
    0x31: ["\u0031"],	# DIGIT ONE
    0x32: ["\u0032"],	# DIGIT TWO
    0x33: ["\u0033"],	# DIGIT THREE
    0x34: ["\u0034"],	# DIGIT FOUR
    0x35: ["\u0035"],	# DIGIT FIVE
    0x36: ["\u0036"],	# DIGIT SIX
    0x37: ["\u0037"],	# DIGIT SEVEN
    0x38: ["\u0038"],	# DIGIT EIGHT
    0x39: ["\u0039"],	# DIGIT NINE
    0x3A: ["\u003A"],	# COLON
    0x3B: ["\u003B"],	# SEMICOLON
    0x3C: ["\u003C"],	# LESS-THAN SIGN
    0x3D: ["\u003D"],	# EQUALS SIGN
    0x3E: ["\u003E"],	# GREATER-THAN SIGN
    0x3F: ["\u003F"],	# QUESTION MARK
    0x40: ["\u0040"],	# COMMERCIAL AT
    0x41: ["\u0041"],	# LATIN CAPITAL LETTER A
    0x42: ["\u0042"],	# LATIN CAPITAL LETTER B
    0x43: ["\u0043"],	# LATIN CAPITAL LETTER C
    0x44: ["\u0044"],	# LATIN CAPITAL LETTER D
    0x45: ["\u0045"],	# LATIN CAPITAL LETTER E
    0x46: ["\u0046"],	# LATIN CAPITAL LETTER F
    0x47: ["\u0047"],	# LATIN CAPITAL LETTER G
    0x48: ["\u0048"],	# LATIN CAPITAL LETTER H
    0x49: ["\u0049"],	# LATIN CAPITAL LETTER I
    0x4A: ["\u004A"],	# LATIN CAPITAL LETTER J
    0x4B: ["\u004B"],	# LATIN CAPITAL LETTER K
    0x4C: ["\u004C"],	# LATIN CAPITAL LETTER L
    0x4D: ["\u004D"],	# LATIN CAPITAL LETTER M
    0x4E: ["\u004E"],	# LATIN CAPITAL LETTER N
    0x4F: ["\u004F"],	# LATIN CAPITAL LETTER O
    0x50: ["\u0050"],	# LATIN CAPITAL LETTER P
    0x51: ["\u0051"],	# LATIN CAPITAL LETTER Q
    0x52: ["\u0052"],	# LATIN CAPITAL LETTER R
    0x53: ["\u0053"],	# LATIN CAPITAL LETTER S
    0x54: ["\u0054"],	# LATIN CAPITAL LETTER T
    0x55: ["\u0055"],	# LATIN CAPITAL LETTER U
    0x56: ["\u0056"],	# LATIN CAPITAL LETTER V
    0x57: ["\u0057"],	# LATIN CAPITAL LETTER W
    0x58: ["\u0058"],	# LATIN CAPITAL LETTER X
    0x59: ["\u0059"],	# LATIN CAPITAL LETTER Y
    0x5A: ["\u005A"],	# LATIN CAPITAL LETTER Z
    0x5B: ["\u005B"],	# LEFT SQUARE BRACKET
    0x5C: ["\u005C"],	# REVERSE SOLIDUS
    0x5D: ["\u005D"],	# RIGHT SQUARE BRACKET
    0x5E: ["\u005E"],	# CIRCUMFLEX ACCENT
    0x5F: ["\u005F"],	# LOW LINE
    0x60: ["\u0060"],	# GRAVE ACCENT
    0x61: ["\u0061"],	# LATIN SMALL LETTER A
    0x62: ["\u0062"],	# LATIN SMALL LETTER B
    0x63: ["\u0063"],	# LATIN SMALL LETTER C
    0x64: ["\u0064"],	# LATIN SMALL LETTER D
    0x65: ["\u0065"],	# LATIN SMALL LETTER E
    0x66: ["\u0066"],	# LATIN SMALL LETTER F
    0x67: ["\u0067"],	# LATIN SMALL LETTER G
    0x68: ["\u0068"],	# LATIN SMALL LETTER H
    0x69: ["\u0069"],	# LATIN SMALL LETTER I
    0x6A: ["\u006A"],	# LATIN SMALL LETTER J
    0x6B: ["\u006B"],	# LATIN SMALL LETTER K
    0x6C: ["\u006C"],	# LATIN SMALL LETTER L
    0x6D: ["\u006D"],	# LATIN SMALL LETTER M
    0x6E: ["\u006E"],	# LATIN SMALL LETTER N
    0x6F: ["\u006F"],	# LATIN SMALL LETTER O
    0x70: ["\u0070"],	# LATIN SMALL LETTER P
    0x71: ["\u0071"],	# LATIN SMALL LETTER Q
    0x72: ["\u0072"],	# LATIN SMALL LETTER R
    0x73: ["\u0073"],	# LATIN SMALL LETTER S
    0x74: ["\u0074"],	# LATIN SMALL LETTER T
    0x75: ["\u0075"],	# LATIN SMALL LETTER U
    0x76: ["\u0076"],	# LATIN SMALL LETTER V
    0x77: ["\u0077"],	# LATIN SMALL LETTER W
    0x78: ["\u0078"],	# LATIN SMALL LETTER X
    0x79: ["\u0079"],	# LATIN SMALL LETTER Y
    0x7A: ["\u007A"],	# LATIN SMALL LETTER Z
    0x7B: ["\u007B"],	# LEFT CURLY BRACKET
    0x7C: ["\u007C"],	# VERTICAL LINE
    0x7D: ["\u007D"],	# RIGHT CURLY BRACKET
    0x7E: ["\u007E"],	# TILDE
    0x7F: ["\ufffe"],  # CRYPTOHACK
    0x80: ["\u00AB"],	# LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    0x81: ["\u00BB"],	# RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    0x82: ["\u2026"],	# HORIZONTAL ELLIPSIS
    0x83: ["\u0E48","\uF875"],	# THAI CHARACTER MAI EK, low left position
    0x84: ["\u0E49","\uF875"],	# THAI CHARACTER MAI THO, low left position
    0x85: ["\u0E4A","\uF875"],	# THAI CHARACTER MAI TRI, low left position
    0x86: ["\u0E4B","\uF875"],	# THAI CHARACTER MAI CHATTAWA, low left position
    0x87: ["\u0E4C","\uF875"],	# THAI CHARACTER THANTHAKHAT, low left position
    0x88: ["\u0E48","\uF873"],	# THAI CHARACTER MAI EK, low position
    0x89: ["\u0E49","\uF873"],	# THAI CHARACTER MAI THO, low position
    0x8A: ["\u0E4A","\uF873"],	# THAI CHARACTER MAI TRI, low position
    0x8B: ["\u0E4B","\uF873"],	# THAI CHARACTER MAI CHATTAWA, low position
    0x8C: ["\u0E4C","\uF873"],	# THAI CHARACTER THANTHAKHAT, low position
    0x8D: ["\u201C"],	# LEFT DOUBLE QUOTATION MARK
    0x8E: ["\u201D"],	# RIGHT DOUBLE QUOTATION MARK
    0x8F: ["\u0E4D","\uF874"],	# THAI CHARACTER NIKHAHIT, left position
    0x90: ["\ufffe"],  # CRYPTOHACK
    0x91: ["\u2022"],	# BULLET
    0x92: ["\u0E31","\uF874"],	# THAI CHARACTER MAI HAN-AKAT, left position
    0x93: ["\u0E47","\uF874"],	# THAI CHARACTER MAITAIKHU, left position
    0x94: ["\u0E34","\uF874"],	# THAI CHARACTER SARA I, left position
    0x95: ["\u0E35","\uF874"],	# THAI CHARACTER SARA II, left position
    0x96: ["\u0E36","\uF874"],	# THAI CHARACTER SARA UE, left position
    0x97: ["\u0E37","\uF874"],	# THAI CHARACTER SARA UEE, left position
    0x98: ["\u0E48","\uF874"],	# THAI CHARACTER MAI EK, left position
    0x99: ["\u0E49","\uF874"],	# THAI CHARACTER MAI THO, left position
    0x9A: ["\u0E4A","\uF874"],	# THAI CHARACTER MAI TRI, left position
    0x9B: ["\u0E4B","\uF874"],	# THAI CHARACTER MAI CHATTAWA, left position
    0x9C: ["\u0E4C","\uF874"],	# THAI CHARACTER THANTHAKHAT, left position
    0x9D: ["\u2018"],	# LEFT SINGLE QUOTATION MARK
    0x9E: ["\u2019"],	# RIGHT SINGLE QUOTATION MARK
    0x9F: ["\ufffe"],  # CRYPTOHACK
    0xA0: ["\u00A0"],	# NO-BREAK SPACE
    0xA1: ["\u0E01"],	# THAI CHARACTER KO KAI
    0xA2: ["\u0E02"],	# THAI CHARACTER KHO KHAI
    0xA3: ["\u0E03"],	# THAI CHARACTER KHO KHUAT
    0xA4: ["\u0E04"],	# THAI CHARACTER KHO KHWAI
    0xA5: ["\u0E05"],	# THAI CHARACTER KHO KHON
    0xA6: ["\u0E06"],	# THAI CHARACTER KHO RAKHANG
    0xA7: ["\u0E07"],	# THAI CHARACTER NGO NGU
    0xA8: ["\u0E08"],	# THAI CHARACTER CHO CHAN
    0xA9: ["\u0E09"],	# THAI CHARACTER CHO CHING
    0xAA: ["\u0E0A"],	# THAI CHARACTER CHO CHANG
    0xAB: ["\u0E0B"],	# THAI CHARACTER SO SO
    0xAC: ["\u0E0C"],	# THAI CHARACTER CHO CHOE
    0xAD: ["\u0E0D"],	# THAI CHARACTER YO YING
    0xAE: ["\u0E0E"],	# THAI CHARACTER DO CHADA
    0xAF: ["\u0E0F"],	# THAI CHARACTER TO PATAK
    0xB0: ["\u0E10"],	# THAI CHARACTER THO THAN
    0xB1: ["\u0E11"],	# THAI CHARACTER THO NANGMONTHO
    0xB2: ["\u0E12"],	# THAI CHARACTER THO PHUTHAO
    0xB3: ["\u0E13"],	# THAI CHARACTER NO NEN
    0xB4: ["\u0E14"],	# THAI CHARACTER DO DEK
    0xB5: ["\u0E15"],	# THAI CHARACTER TO TAO
    0xB6: ["\u0E16"],	# THAI CHARACTER THO THUNG
    0xB7: ["\u0E17"],	# THAI CHARACTER THO THAHAN
    0xB8: ["\u0E18"],	# THAI CHARACTER THO THONG
    0xB9: ["\u0E19"],	# THAI CHARACTER NO NU
    0xBA: ["\u0E1A"],	# THAI CHARACTER BO BAIMAI
    0xBB: ["\u0E1B"],	# THAI CHARACTER PO PLA
    0xBC: ["\u0E1C"],	# THAI CHARACTER PHO PHUNG
    0xBD: ["\u0E1D"],	# THAI CHARACTER FO FA
    0xBE: ["\u0E1E"],	# THAI CHARACTER PHO PHAN
    0xBF: ["\u0E1F"],	# THAI CHARACTER FO FAN
    0xC0: ["\u0E20"],	# THAI CHARACTER PHO SAMPHAO
    0xC1: ["\u0E21"],	# THAI CHARACTER MO MA
    0xC2: ["\u0E22"],	# THAI CHARACTER YO YAK
    0xC3: ["\u0E23"],	# THAI CHARACTER RO RUA
    0xC4: ["\u0E24"],	# THAI CHARACTER RU
    0xC5: ["\u0E25"],	# THAI CHARACTER LO LING
    0xC6: ["\u0E26"],	# THAI CHARACTER LU
    0xC7: ["\u0E27"],	# THAI CHARACTER WO WAEN
    0xC8: ["\u0E28"],	# THAI CHARACTER SO SALA
    0xC9: ["\u0E29"],	# THAI CHARACTER SO RUSI
    0xCA: ["\u0E2A"],	# THAI CHARACTER SO SUA
    0xCB: ["\u0E2B"],	# THAI CHARACTER HO HIP
    0xCC: ["\u0E2C"],	# THAI CHARACTER LO CHULA
    0xCD: ["\u0E2D"],	# THAI CHARACTER O ANG
    0xCE: ["\u0E2E"],	# THAI CHARACTER HO NOKHUK
    0xCF: ["\u0E2F"],	# THAI CHARACTER PAIYANNOI
    0xD0: ["\u0E30"],	# THAI CHARACTER SARA A
    0xD1: ["\u0E31"],	# THAI CHARACTER MAI HAN-AKAT
    0xD2: ["\u0E32"],	# THAI CHARACTER SARA AA
    0xD3: ["\u0E33"],	# THAI CHARACTER SARA AM
    0xD4: ["\u0E34"],	# THAI CHARACTER SARA I
    0xD5: ["\u0E35"],	# THAI CHARACTER SARA II
    0xD6: ["\u0E36"],	# THAI CHARACTER SARA UE
    0xD7: ["\u0E37"],	# THAI CHARACTER SARA UEE
    0xD8: ["\u0E38"],	# THAI CHARACTER SARA U
    0xD9: ["\u0E39"],	# THAI CHARACTER SARA UU
    0xDA: ["\u0E3A"],	# THAI CHARACTER PHINTHU
    0xDB: ["\u2060"],	# WORD JOINER # for Unicode 3.2 and later
    0xDC: ["\u200B"],	# ZERO WIDTH SPACE
    0xDD: ["\u2013"],	# EN DASH
    0xDE: ["\u2014"],	# EM DASH
    0xDF: ["\u0E3F"],	# THAI CURRENCY SYMBOL BAHT
    0xE0: ["\u0E40"],	# THAI CHARACTER SARA E
    0xE1: ["\u0E41"],	# THAI CHARACTER SARA AE
    0xE2: ["\u0E42"],	# THAI CHARACTER SARA O
    0xE3: ["\u0E43"],	# THAI CHARACTER SARA AI MAIMUAN
    0xE4: ["\u0E44"],	# THAI CHARACTER SARA AI MAIMALAI
    0xE5: ["\u0E45"],	# THAI CHARACTER LAKKHANGYAO
    0xE6: ["\u0E46"],	# THAI CHARACTER MAIYAMOK
    0xE7: ["\u0E47"],	# THAI CHARACTER MAITAIKHU
    0xE8: ["\u0E48"],	# THAI CHARACTER MAI EK
    0xE9: ["\u0E49"],	# THAI CHARACTER MAI THO
    0xEA: ["\u0E4A"],	# THAI CHARACTER MAI TRI
    0xEB: ["\u0E4B"],	# THAI CHARACTER MAI CHATTAWA
    0xEC: ["\u0E4C"],	# THAI CHARACTER THANTHAKHAT
    0xED: ["\u0E4D"],	# THAI CHARACTER NIKHAHIT
    0xEE: ["\u2122"],	# TRADE MARK SIGN
    0xEF: ["\u0E4F"],	# THAI CHARACTER FONGMAN
    0xF0: ["\u0E50"],	# THAI DIGIT ZERO
    0xF1: ["\u0E51"],	# THAI DIGIT ONE
    0xF2: ["\u0E52"],	# THAI DIGIT TWO
    0xF3: ["\u0E53"],	# THAI DIGIT THREE
    0xF4: ["\u0E54"],	# THAI DIGIT FOUR
    0xF5: ["\u0E55"],	# THAI DIGIT FIVE
    0xF6: ["\u0E56"],	# THAI DIGIT SIX
    0xF7: ["\u0E57"],	# THAI DIGIT SEVEN
    0xF8: ["\u0E58"],	# THAI DIGIT EIGHT
    0xF9: ["\u0E59"],	# THAI DIGIT NINE
    0xFA: ["\u00AE"],	# REGISTERED SIGN
    0xFB: ["\u00A9"],	# COPYRIGHT SIGN
    0xFC: ["\ufffe"],  # CRYPTOHACK
    0xFD: ["\ufffe"],  # CRYPTOHACK
    0xFE: ["\ufffe"],  # CRYPTOHACK
    0xFF: ["\ufffe"],  # CRYPTOHACK
}