import binascii


def encode8(data):
    hexed = format(data, '08X')
    return binascii.hexlify(str(hexed))


def encode3(data):
    hexed = format(data, '03X')
    return binascii.hexlify(str(hexed))


def decode(data):
    hexed = binascii.unhexlify(data.encode('hex'))
    return int(hexed, 16)


# encoded8 = encode8(1234)
# encoded3 = encode3(1234)

# decoded = decode("4D2")
# print "Encoded: ", encoded8, encoded3
# print "Decoded: ", decoded
