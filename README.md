py_django_crack
===============

Crack the django password on the way. By default Django use pbkdf2 and sha256 method to encrypt user's password. Once get the password stored in the database table, you need to compare it with others if brute force cracking. It is recommended that you use hash table comparison. The tool 'rainbow crack' can generate rainbow hash tables while another tool 'hashcat' brute-force cracks password from a dictionary alive. Because django uses PBKDF2(Password-Based Key Derivation Function), it would take too long to generate a password. 
