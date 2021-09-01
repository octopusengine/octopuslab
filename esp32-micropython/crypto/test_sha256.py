# test_sha256
# from uhashlib import sha256

import uhashlib as hashlib
from ubinascii import hexlify

print("test_sha256")


# Python:
# decoded = array.array('b', hash).tostring().decode('utf-8')
"""
def convert(byte_array):
    result = []
    for i in range(len(byte_array)):
            x = byte_array[i]
            if x < 0:
                b16 = x & 0xFFFF # 16 bit
                b16 = b16 << 8
                b16 = b16 | byte_array[i+1]
                result.append(unichr(m16))
            else:
                result.append(chr(x))
    return "".join(result)
"""

# Python:
# sha256(string.encode('utf-8')).hexdigest()
"""
hash = sha256("agama").digest() # .hexdigest() / .decode('utf-8')
print("hash ", hash)
decoded = convert(hash)
print("decoded ", decoded)
"""

h = hashlib.sha256()
h.update(b"abcd" * 1000)
print(h.digest())

print(hashlib.sha256(b"\xff" * 64).digest())
print()


print("--------- agama3 -----------")
h = hashlib.sha256()
hash = h.update(b"agama3")

hdig = h.digest()
print(hdig)

hhex = hexlify(hdig).decode()

print("sha256: ", hhex)
