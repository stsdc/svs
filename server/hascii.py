import binascii
from log import logger

def encode8(data):
    hexed = format(data, '08X')
    return binascii.hexlify(str(hexed))


def encode3(data):
    hexed = format(data, '03X')
    return binascii.hexlify(str(hexed))


def decode(data):
    hexed = binascii.unhexlify(data.encode('hex'))
    try:
        return int(hexed, 16)
    except ValueError as e:
        logger.error("HAscii: %s", e)


# encoded8 = encode8(100)
# encoded3 = encode3(1234)

# decoded = decode("4D2")
# print "Encoded: ", encoded8, encoded3
# print "Decoded: ", decoded
