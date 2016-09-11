py_django_crack
===============

Crack the django password on the way. By default Django use pbkdf2 and sha256 method to encrypt user's password. Once get the password stored in the database table, you need to compare it with others if brute force cracking. It is recommended that you use hash table comparison. The tool 'rainbow crack' can generate rainbow hash tables while another tool 'hashcat' brute-force cracks password from a dictionary alive. Because django uses PBKDF2(Password-Based Key Derivation Function), it would take too long to generate a password. 

## jake
* The ```jake.py``` is the password encryption implementation which is derived from django

### Usage

For entertainment only :)

To decrypt the password in the Django framework, you need to get the value which is stored in the database table 'auth_user' column 'password'.

For example the encryped password is:

    pbkdf2_sha256$12000$Lz8oA7gW43mJ$N/DzMkLc/CX4oKHrU2bSPul3svNOmz8CYthM1JrR4Mo=

    {algorithm}${iteration times}${salt}${encryped password}

In this case, **pbkdf2_sha256** is the encryption algorithm, and **12000** is the iteration times, 

`Lz8oA7gW43mJ` is the salt, 

`Lz8oA7gW43mJ$N/DzMkLc/CX4oKHrU2bSPul3svNOmz8CYthM1JrR4Mo=`  is the base64 encoded password

**Note**:

> As of 2011, 10,000 iterations was the recommended default which
> took 100ms on a 2.2Ghz Core 2 Duo. This is probably the bare
> minimum for security given 1000 iterations was recommended in 2001.

This is also a standalone module derived from Django. If any other webframe work can use this module.

**When coding**:

```python
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
```

Tools
-----
* ```hashcat. This can crack password from hashes based on word dictionaries. There are tones of algorithms built-in. Good dictionary is important. ``` <a href="http://www.hashcat.net/" target="_blank">hashcat offical link</a>
* ```rainbow table generator/cracker: rainbowcrack (rcrack, rt2rtc, rtc2rt, rsort, rtgen) . ```<a href="http://project-rainbowcrack.com" target="_blank">project-rainbowcrack link</a>

Explaination
------------
* The rainbow table might be very large. Normally it would be like more than hundreds Giga Bytes. So you could download or make one by own. But sometimes it would take too long to generate the rainbow table. For instance in this case Django uses PBKDF2 and algorithm sha256 to encrypt password iteration by iteration, which means it will take very long to generate a single password or a HASH. So brute-force cracking is somehow lousy. Or you have super computer, things would be better. Sometimes you don't.
* So the summery here is:  To crack the django's password, there are two ways. 1) brute-force cracking which takes very long and hard-working on computer expense. 2) middle attack which means user's password can be captured alive. This has something to do with the art of deception. Pratical and social engineering.

#### Happy hacking
