Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> 
= RESTART: C:/Users/wes/AppData/Local/Programs/Python/Python313/mini_cryptanalysis_toolkit.py
=== Automated Cryptanalysis Toolkit ===
Enter Plaintext 1/Ciphertext 1 (Hex or String): Tigers
Enter Plaintext 2 (for Difference Analysis only): Jaguars

==================================================
              ANALYSIS REPORT                  
==================================================
--- Input Differential Cryptanalysis ---
XOR Byte Differences : 0x1E 0x08 0x00 0x10 0x13 0x01 0x73
Flipped Bits Detected: 15 / 56 bits (26.79%)
--------------------------------------------------
--- Token Frequency Analysis ---
Byte [0x54]: Occurred 1 times (16.67%)
Byte [0x69]: Occurred 1 times (16.67%)
Byte [0x67]: Occurred 1 times (16.67%)
Byte [0x65]: Occurred 1 times (16.67%)
Byte [0x72]: Occurred 1 times (16.67%)
--------------------------------------------------
--- Linear Statistical Bias Analysis ---
Total Bit Density: 1s = 25 | 0s = 23
Calculated Bias  : 0.0208 (Ideal Random = 0.0000)
==================================================
