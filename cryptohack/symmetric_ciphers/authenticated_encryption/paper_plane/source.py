from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os


KEY = "?"
FLAG = "?"


class AesIge:
    def __init__(self, key):
        self.cipher = AES.new(key, AES.MODE_ECB)

    def encrypt(self, data, m0=os.urandom(16), c0=os.urandom(16)):
        data = pad(data, 16, 'pkcs7')

        last_block_plaintext = m0
        last_block_ciphertext = c0
        result = b''
        for i in range(0, len(data), 16):
            block = data[i: i + 16]
            x = AesIge._xor_blocks(block, last_block_ciphertext)
            x = self.cipher.encrypt(x)
            x = AesIge._xor_blocks(x, last_block_plaintext)
            result += x

            last_block_plaintext = block
            last_block_ciphertext = x

        return result, m0, c0

    def decrypt(self, data, m0, c0):
        last_block_plaintext = m0
        last_block_ciphertext = c0
        result = b''

        for i in range(0, len(data), 16):
            block = data[i: i + 16]
            # m0 and c0 can be negated
            # pkcs7 padding oracle
            # can get stream data of flag enc
            # unk: flag
            # ciph = enc(pad(flag) ^ c0) ^ m0
            # flag = upad(dec(ciph ^ m0) ^ c0)
            # issue is the typical padding oracle now requires us to change the ciphertext to check for padding errors with this config
            
            # flag = upad(dec(ciph) ^ c) # find c that works with no m
            # start with 0x00*15 + 0xi

            # plain = upad(dec(ciph ^ m) ^ c)
            # plain = upad(dec(ciph ^ c0) ^ 0000)
            x = AesIge._xor_blocks(block, last_block_plaintext)
            x = self.cipher.decrypt(x)
            x = AesIge._xor_blocks(x, last_block_ciphertext)
            result += x

            last_block_ciphertext = block
            last_block_plaintext = x

        if AesIge._is_pkcs7_padded(result):
            return unpad(result, 16, 'pkcs7')
        else:
            return None

    @staticmethod
    def _is_pkcs7_padded(message):
        padding = message[-message[-1]:]
        return all(padding[i] == len(padding) for i in range(0, len(padding)))

    @staticmethod
    def _xor_blocks(a, b):
        return bytes([x ^ y for x, y in zip(a, b)])



@chal.route('/paper_plane/encrypt_flag/')
def encrypt_flag():
    ciphertext, m0, c0 = AesIge(KEY).encrypt(FLAG.encode())
    return {"ciphertext": ciphertext.hex(), "m0": m0.hex(), "c0": c0.hex()}


@chal.route('/paper_plane/send_msg/<ciphertext>/<m0>/<c0>/')
def send_msg(ciphertext, m0, c0):
    ciphertext = bytes.fromhex(ciphertext)
    m0 = bytes.fromhex(m0)
    c0 = bytes.fromhex(c0)
    if len(ciphertext) % 16 != 0:
        return {"error": "Data length must be a multiple of the blocksize!"}
    if len(c0) != 16 or len(m0) != 16:
        return {"error": "m0 and c0 must be 16 bytes long!"}

    plaintext = AesIge(KEY).decrypt(ciphertext, m0, c0)
    if plaintext is not None:
        return {"msg": "Message received"}
    else:
        return {"error": "Can't decrypt the message."}
