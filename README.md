py_django_crack
===============

Crack the django password on the way. By default Django use pbkdf2 and sha256 method to encrypt user's password. Once get the password stored in the database table, you need to compare it with others if brute force cracking. It is recommended that you use hash table comparison. The tool 'rainbow crack' can generate rainbow hash tables while another tool 'hashcat' brute-force cracks password from a dictionary alive. Because django uses PBKDF2(Password-Based Key Derivation Function), it would take too long to generate a password. 

# jake
* The ```jake.py``` is the password encryption implementation which is derived from django

Tools
-----
* ```hashcat. This can crack password from hashes based on word dictionaries. There are tones of algorithms built-in. Good dictionary is important. ``` <a href="http://www.hashcat.net/" target="_blank">hashcat offical link</a>
```rainbow table generator/cracker: rainbowcrack (rcrack, rt2rtc, rtc2rt, rsort, rtgen) . ```<a href="http://project-rainbowcrack.com" target="_blank">project-rainbowcrack link</a>
* The rainbow table might be very large. Normally it would be like more than hundreds Giga Bytes. So you could download or make one by own. But sometimes it would take too long to generate the rainbow table. For instance in this case Django uses PBKDF2 and algorithm sha256 to encrypt password iteration by iteration, which means it will take very long to generate a single password or a HASH. So brute-force cracking is somehow lousy. Or you have super computer, things would be better. Sometimes you don't.
* So the summery here is:  To crack the django's password, there are two ways. 1) brute-force cracking which takes very long and hard-working on computer expense. 2) middle attack which means user's password can be captured alive. This has something to do with the art of deception. Pratical and social engineering.

# Happy hacking
