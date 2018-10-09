import os
os.path.basename(os.path.dirname(os.path.realpath(__file__)))

import hashlib
import hmac
# for python3.x
from promise import Promise

import six
import operator
import struct
import binascii
import base64
import functools


'''
Copyright to Alexander Liu
For entertainment only :)

To decrypt the password in the Django framework, you need to get
the value which is stored in the database table 'auth_user' column 'password'.

For example the encryped password is:

    pbkdf2_sha256$12000$Lz8oA7gW43mJ$N/DzMkLc/CX4oKHrU2bSPul3svNOmz8CYthM1JrR4Mo=
    {algorithm}${iteration times}${salt}${encryped password}

In this case, pbkdf2_sha256 is the encryption algorithm, and 12000 is the iteration times, 
'Lz8oA7gW43mJ' (without quoto) is the salt, 
'Lz8oA7gW43mJ$N/DzMkLc/CX4oKHrU2bSPul3svNOmz8CYthM1JrR4Mo=' (without quoto) is the base64 encoded password

Note:
    As of 2011, 10,000 iterations was the recommended default which
    took 100ms on a 2.2Ghz Core 2 Duo. This is probably the bare
    minimum for security given 1000 iterations was recommended in 2001.

This is also a standalone module derived from Django. If any other webframe work can use this module.

Usage:
>>> from jake import give_back_hashed
>>> from jake import get_base64_hashed
>>> a = give_base64_hashed('the_password', 'the_salt', 'iteration_times', 'the_hashlib_digest_object(the algorithm)')
>>> # this is the password which encrypted in the database table 'auth_user' column 'password'
>>> print a
N/DzMkLc/CX4oKHrU2bSPul3svNOmz8CYthM1JrR4Mo=
>>> # or you can do this
>>> import hashlib
>>> b = give_base64_hashed('the_password', 'the_salt', 'iteration_times', hashlib.sha256)
>>> print b
N/DzMkLc/CX4oKHrU2bSPul3svNOmz8CYthM1JrR4Mo=
>>> # To get the real sha256 hashed value
>>> c = give_back_hashed(b)
>>> print c
'7\xf0\xf32B\xdc\xfc%\xf8\xa0\xa1\xebSf\xd2>\xe9w\xb2\xf3N\x9b?\x02b\xd8L\xd4\x9a\xd1\xe0\xca'
>>> # you need other tools such as 'hashcat' or 'crack' to generate HASHes from 
>>> # a dictionay to compare them with this.

'''

def _bin_to_long(x):
    """
    Convert a binary string into a long integer

    This is a clever optimization for fast xor vector math
    """
    return int(binascii.hexlify(x), 16)


def _long_to_bin(x, hex_format_string):
    """
    Convert a long integer into a binary string.
    hex_format_string is like "%020x" for padding 10 characters.
    """
    return binascii.unhexlify((hex_format_string % x).encode('ascii'))


def force_bytes(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Similar to smart_bytes, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    '''
    if isinstance(s, six.memoryview):
        s = bytes(s)
    '''
    if isinstance(s, bytes):
        if encoding == 'utf-8':
            return s
        else:
            return s.decode('utf-8', errors).encode(encoding, errors)
    if strings_only and (s is None or isinstance(s, int)):
        return s
    if isinstance(s, Promise):
        return six.text_type(s).encode(encoding, errors)
    if not isinstance(s, six.string_types):
        try:
            if six.PY3:
                return six.text_type(s).encode(encoding)
            else:
                return bytes(s)
        except UnicodeEncodeError:
            if isinstance(s, Exception):
                # An Exception subclass containing non-ASCII data that doesn't
                # know how to print itself properly. We shouldn't raise a
                # further exception.
                return b' '.join([force_bytes(arg, encoding, strings_only,
                        errors) for arg in s])
            return six.text_type(s).encode(encoding, errors)
    else:
        return s.encode(encoding, errors)


def pbkdf2(password, salt, iterations, dklen=0, digest=None):
    """
    Implements PBKDF2 as defined in RFC 2898, section 5.2

    HMAC+SHA256 is used as the default pseudo random function.

    As of 2011, 10,000 iterations was the recommended default which
    took 100ms on a 2.2Ghz Core 2 Duo. This is probably the bare
    minimum for security given 1000 iterations was recommended in
    2001. This code is very well optimized for CPython and is only
    four times slower than openssl's implementation. Look in
    django.contrib.auth.hashers for the present default.
    """
    assert iterations > 0
    if not digest:
        digest = hashlib.sha256
    password = force_bytes(password)
    salt = force_bytes(salt)
    hlen = digest().digest_size
    if not dklen:
        dklen = hlen
    if dklen > (2 ** 32 - 1) * hlen:
        raise OverflowError('dklen too big')
    l = -(-dklen // hlen)
    r = dklen - (l - 1) * hlen

    hex_format_string = "%%0%ix" % (hlen * 2)

    inner, outer = digest(), digest()
    if len(password) > inner.block_size:
        password = digest(password).digest()
    password += b'\x00' * (inner.block_size - len(password))
    inner.update(password.translate(hmac.trans_36))
    outer.update(password.translate(hmac.trans_5C))

    def F(i):
        def U():
            u = salt + struct.pack(b'>I', i)
            for j in range(int(iterations)):
                dig1, dig2 = inner.copy(), outer.copy()
                dig1.update(u)
                dig2.update(dig1.digest())
                u = dig2.digest()
                yield _bin_to_long(u)
        return _long_to_bin(functools.reduce(operator.xor, U()), hex_format_string)

    T = [F(x) for x in range(1, l + 1)]
    return b''.join(T[:-1]) + T[-1][:r]




def get_base64_hashed(password, salt, iterations, dklen=0, digest=None):
    gotten = pbkdf2(password, salt, iterations, dklen=0, digest=None)
    gotten = base64.b64encode(gotten).decode('ascii').strip()
    return gotten


def give_back_hashed(base64string):
    '''
    '''
    return base64.b64decode(base64string)
