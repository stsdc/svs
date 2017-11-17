import binascii
from log import logger

# This are maximum values for 3 & 8 character HAscii ranges
MAX3 = 4095  # => 0xFFF
MAX4 = 65535  # => 0xFFFF
MAX8 = 4294967295  # => 0xFFFFFFFF


def encode8(data):
    if data >= 0:
        hexed = format(data, '08X')
    else:
        hexed = format(MAX8 - abs(data), '08X')
    return [ord(x) for x in hexed]


def encode3(data):
    if data >= 0:
        hexed = format(data, '03X')
    else:
        hexed = format(MAX3 - abs(data), '03X')
    return [ord(x) for x in hexed]


def decode(data):
    hexed = binascii.unhexlify(data.encode('hex'))
    try:
        return int(hexed, 16)
    except ValueError as e:
        logger.error("HAscii: Decode: %s", e)

# encoded8 = encode8(100)
# encoded3 = encode3(1234)
#
# decoded = decode("4D2")
# print "Encoded: ", encoded8, encoded3
# print "Decoded: ", decoded
