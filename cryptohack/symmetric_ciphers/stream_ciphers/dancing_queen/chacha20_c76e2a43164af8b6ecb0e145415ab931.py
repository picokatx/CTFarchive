#!/usr/bin/env python3

from os import urandom


FLAG = b'crypto{?????????????????????????????}'


# safe
def bytes_to_words(b):
    return [int.from_bytes(b[i:i+4], 'little') for i in range(0, len(b), 4)]

# safe
def rotate(x, n):
    return ((x << n) & 0xffffffff) | ((x >> (32 - n)) & 0xffffffff)

# safe
def word(x):
    return x % (2 ** 32)

# safe
def words_to_bytes(w):
    return b''.join([i.to_bytes(4, 'little') for i in w])

# safe
def xor(a, b):
    return b''.join([bytes([x ^ y]) for x, y in zip(a, b)])


class ChaCha20:
    # safe
    def __init__(self):
        self._state = []

    # safe
    def _inner_block(self, state):
        self._quarter_round(state, 0, 4, 8, 12)
        self._quarter_round(state, 1, 5, 9, 13)
        self._quarter_round(state, 2, 6, 10, 14)
        self._quarter_round(state, 3, 7, 11, 15)
        self._quarter_round(state, 0, 5, 10, 15)
        self._quarter_round(state, 1, 6, 11, 12)
        self._quarter_round(state, 2, 7, 8, 13)
        self._quarter_round(state, 3, 4, 9, 14)

    # safe
    def _quarter_round(self, x, a, b, c, d):
        x[a] = word(x[a] + x[b]); x[d] ^= x[a]; x[d] = rotate(x[d], 16)
        x[c] = word(x[c] + x[d]); x[b] ^= x[c]; x[b] = rotate(x[b], 12)
        x[a] = word(x[a] + x[b]); x[d] ^= x[a]; x[d] = rotate(x[d], 8)
        x[c] = word(x[c] + x[d]); x[b] ^= x[c]; x[b] = rotate(x[b], 7)
    
    # safe (used incorrectly down the line)
    def _setup_state(self, key, iv):
        # more or less 1 for 1 with lines 46-50
        # jsut need to check if bytes word conversions are secure
        self._state = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]
        self._state.extend(bytes_to_words(key))
        self._state.append(self._counter)
        self._state.extend(bytes_to_words(iv))

    # ignore: same as ciphertext
    def decrypt(self, c, key, iv):
        return self.encrypt(c, key, iv)

    # vuln almost certainly here, already see some differences
    def encrypt(self, m, key, iv):
        c = b''
        self._counter = 1

        for i in range(0, len(m), 64):
            self._setup_state(key, iv)
            print(self._state)
            for j in range(10):
                self._inner_block(self._state)
            # ctx[12] = (ctx[12] + 1) & 0xffffffff
            # if ctx[12] == 0:
            # ctx[13] = (ctx[13] + 1) & 0xffffffff

            # !x[i] + ctx[i] does not add residual!!!! not sure if this means anything
            # _state[12] resets to self._counter+1 which is definitely sus
            # ok in general we run._setup_state every time which is bad
            # we have key, iv1 state of 2 blocks, with counter = 1 and 2 respectively
            # we have key, iv2 state of flag block, with counter = 1
            c += xor(m[i:i+64], words_to_bytes(self._state))

            self._counter += 1
            print(self._state)
        
        return c
    
# ignore: no special info, we get iv and ciphertext + 1 non flag plaintext
if __name__ == '__main__':
    msg = b'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula.'
    key = urandom(32)
    iv1 = urandom(12)
    iv2 = urandom(12)

    c = ChaCha20()
    msg_enc = c.encrypt(msg, key, iv1)
    flag_enc = c.encrypt(FLAG, key, iv2)

    print(f"iv1 = '{iv1.hex()}'")
    print(f"iv2 = '{iv2.hex()}'")
    print(f"msg_enc = '{msg_enc.hex()}'")
    print(f"flag_enc = '{flag_enc.hex()}'")
