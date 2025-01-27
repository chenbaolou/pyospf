#!/usr/bin/env python
# -*- coding:utf-8 -*-


import struct, socket, string, sys, datetime, ipaddr, re


def find_num_in_string(string):
    reg = re.compile('r[^0-9]*(\d*)[^0-9]*')
    return reg.findall(string)


def is_set(bit):
    if bit > 0:
        return 1
    else:
        return 0


def find_key(dic, value):
    res = []
    for v in dic.items():
        if v[1] == value:
            res.append(v[0])
    return res


def ip2int(ip):
    return ipaddr.IPv4Address(ip)._ip


def int2ip(i):
    if isinstance(i, str):
        i = int(i)
    return socket.inet_ntoa(struct.pack("!I", i))


def intpack(id):
    return struct.pack('!I', id)


def mask2plen(mask):
    rv = 32
    while mask % 2 == 0:
        rv = rv - 1
        mask = mask >> 1
    return rv


def plen2mask(plen):
    return pow(2L, 32) - pow(2L, 32-plen)


def pfx2id(pfx, plen=None):
    if plen == None:
        plen = pfx[1]
        pfx  = pfx[0]
    mask = plen2mask(plen)
    p    = 0
    for i in range(len(pfx)):
        p = p << 8
        p = p | ord(pfx[i])
    p = p << (8 * (4-len(pfx)))
    p = p & mask

    return p


def addrmask2str(addr, mask):
    plen = mask2plen(mask)
    id   = addr & mask
    return "%s/%d" % (id2str(id), plen)


def pfx2str(pfx, plen=None):
    if plen == None:
        plen = int(pfx[1])
        pfx  = pfx[0]

    mask = plen2mask(plen)
    p = 0
    for i in range(len(pfx)):
        p = p << 8
        p = p | ord(pfx[i])
    p = p << (8 * (4-len(pfx)))
    p = p & mask

    return "%s/%d" % (id2str(p), plen)


def rpfx2str(pfxtup):
    plen, pfx = pfxtup
    p = 0
    for i in range(len(pfx)):
        p = p << 8
        p = p | ord(pfx[i])
    p = p << (8 * (4-len(pfx)))

    return "%s/%d" % (id2str(p), plen)


def id2pfx(id):
    a = int( ((id & 0xff000000L) >> 24) & 0xff)
    b = int( ((id & 0x00ff0000)  >> 16) & 0xff)
    c = int( ((id & 0x0000ff00)  >>  8) & 0xff)
    d = int( ((id & 0x000000ff))        & 0xff)

    return struct.pack('4B', a, b, c, d)


def id2str(id):
    return "%d.%d.%d.%d" %\
           (int( ((id & 0xff000000L) >> 24) & 0xff),
            int( ((id & 0x00ff0000)  >> 16) & 0xff),
            int( ((id & 0x0000ff00)  >>  8) & 0xff),
            int( (id  & 0x000000ff)         & 0xff) )


def str2id(str):
    quads = string.split(str, '.')
    ret = (string.atol(quads[0]) << 24) + (string.atol(quads[1]) << 16) +\
            (string.atol(quads[2]) <<  8) + (string.atol(quads[3]) <<  0)
    return ret


def str2pfx(strng):
    pfx, plen = string.split(strng, '/')
    plen = string.atoi(plen)

    pfx = string.split(pfx, '.')
    p   = ''
    for e in pfx:
        p = struct.pack('%dsB' % len(p), p, string.atoi(e))
    pfx = p

    return (pfx, plen)


def isid2id(str):

    str = string.join(string.split(str2hex(str), '.'), '')
    str = "%s.%s.%s.%s" % (str[0:3], str[3:6], str[6:9], str[9:12])

    return str2id(str)


def str2hex(str):
    if str == None or str == "":
        return ""
    ret = map(lambda x: '%0.2x' % x, map(ord, str))
    ret = string.join(ret, '.')

    return ret


def prthex(pfx, str):
    if str == None or str == "":
        return ""

    ret = ""
    for i in range(0, len(str), 16):
        ret = ret + '\n' + pfx + '0x' + str2hex(str[i:i+16])
    return ret


def str2mac(str):
    byte = string.split(str, '.')
    if len(byte) != 6:
        return

    byte = map(lambda x: string.atoi(x, 16), byte)
    return struct.pack("BBB BBB", byte[0], byte[1], byte[2], byte[3], byte[4], byte[5])


def str2bin(str):
    if str == None or str == "":
        return ""

    ret = ""
    for i in range(len(str)):
        s = ""
        n = ord(str[i])
        for j in range(7, -1, -1):
            b = n / (2**j)
            n %= (2**j)
            s += repr(b)
        ret += ("%s." % s)
    return ret


def prtbin(pfx, str):
    if str == None or str == "":
        return ""

    ret = ""
    for i in range(0, len(str), 8):
        ret = ret + '\n' + pfx + str2bin(str[i:i+8])
    return ret


def int2bin(int):
    # XXX this breaks for negative numbers since >> is arithmetic (?)
    # -- ie. -1 >> 1 == -1...
    if int == 0: return '00000000'
    ret = "" ; bit = 0
    while int != 0:
        if bit % 8 == 0: ret = '.' + ret
        ret = `int%2` + ret
        int = int >> 1
        bit += 1

    if bit % 8 != 0: ret = (8 - bit%8)*"0" + ret
    return ret[:-1]


def int2hex(i):

    if i == 0:
        return "00"
    else:
        ret = ""

    while i != 0:
        ret = "%0.2x." % (i & 0xff) + ret
        i >>= 8

    return ret[:-1]


def strptime(lock, time):
    """
    Translate string time to datetime object.
    """
    with lock:
        try:
            r = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
        except Exception, e:
            #TODO: sometimes exception here, do not find reason
            r = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    return r


def current_time():
    return datetime.datetime.now()


def current_time_str():
    return str(datetime.datetime.now())


def hex2byte(hex_str):
    """
    Convert a string hex byte values into a byte string. The Hex Byte values may
    or may not be space separated.
    """
    bytes = []
    hex_str = ''.join(hex_str.split(" "))
    for i in range(0, len(hex_str), 2):
        bytes.append(chr(int(hex_str[i:i+2], 16)))

    return ''.join(bytes)

def orb(x):
    """Return ord(x) when not already an int."""
    if isinstance(x, int):
        return x
    return ord(x)

def fletcher16(charbuf):
    # This is based on the GPLed C implementation in Zebra <http://www.zebra.org/>  # noqa: E501
    c0 = c1 = 0
    for char in charbuf:
        c0 += orb(char)
        c1 += c0

    c0 %= 255
    c1 %= 255
    return (c0, c1)

def fletcher16_checkbytes(binbuf, offset):
    """Calculates the Fletcher-16 checkbytes returned as 2 byte binary-string.

       Including the bytes into the buffer (at the position marked by offset) the  # noqa: E501
       global Fletcher-16 checksum of the buffer will be 0. Thus it is easy to verify  # noqa: E501
       the integrity of the buffer on the receiver side.

       For details on the algorithm, see RFC 2328 chapter 12.1.7 and RFC 905 Annex B.  # noqa: E501
    """

    # This is based on the GPLed C implementation in Zebra <http://www.zebra.org/>  # noqa: E501
    if len(binbuf) < offset:
        raise Exception("Packet too short for checkbytes %d" % len(binbuf))

    binbuf = binbuf[:offset] + b"\x00\x00" + binbuf[offset + 2:]
    (c0, c1) = fletcher16(binbuf)

    x = ((len(binbuf) - offset - 1) * c0 - c1) % 255

    if (x <= 0):
        x += 255

    y = 510 - c0 - x

    if (y > 255):
        y -= 255

    chksum = (x << 8) | (y & 0xFF)
    
    return (binbuf[:offset] + struct.pack("B", x) + struct.pack("B", (y & 0xFF)) + binbuf[offset+2:], chksum)

def lsa_checksum(binbuf):
    (buf, chksum) = fletcher16_checkbytes(binbuf[2:], 14)
    return (binbuf[:2] + buf, chksum)