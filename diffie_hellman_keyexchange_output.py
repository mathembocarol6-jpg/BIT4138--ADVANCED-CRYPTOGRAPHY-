Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> 
======== RESTART: D:/ADVANCED CRYPTOGRAPHY/diffie_hellman_keyexchange.py =======
Enter prime number p: 5
Enter primitive root g: 9
User A, enter your private key: lime
Traceback (most recent call last):
  File "D:/ADVANCED CRYPTOGRAPHY/diffie_hellman_keyexchange.py", line 26, in <module>
    diffie_hellman()
  File "D:/ADVANCED CRYPTOGRAPHY/diffie_hellman_keyexchange.py", line 5, in diffie_hellman
    a = int(input("User A, enter your private key: "))
ValueError: invalid literal for int() with base 10: 'lime'
>>> 
======== RESTART: D:/ADVANCED CRYPTOGRAPHY/diffie_hellman_keyexchange.py =======
Enter prime number p: 3
Enter primitive root g: 9
User A, enter your private key (a number): 5
User B, enter your private key (a number): 1

User A Public Key: 0
User B Public Key: 0

Shared Secret computed by A: 0
Shared Secret computed by B: 0

Success! Both secrets match.
