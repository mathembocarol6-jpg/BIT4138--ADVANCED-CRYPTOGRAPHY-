Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> 
= RESTART: C:/Users/wes/AppData/Local/Programs/Python/Python313/differential_cryptanalysis_simulator.py
=== SPN Multi-Plaintext Comparative Studio ===
Enter Plaintext 1 (e.g., Musyoka Boniface): mku
Enter Plaintext 2 (e.g., Musyoka Coniface): kilo
Enter Master Key in Hex (e.g., A5): A7
Enter Encryption Rounds (e.g., 4): 8

==================================================
               DATA COMPARISON LOG             
==================================================
Plaintext 1  : mku
Plaintext 2  : kilo
Ciphertext 1 : EA E8 ED
Ciphertext 2 : E8 4F 70 E3
--------------------------------------------------
Total Bits Analyzed    : 32
Flipped Bits Detected  : 16
Structural Distortion  : 50.00%
--------------------------------------------------

[Security Observation]
Observation: Strict Avalanche Criterion (SAC) satisfied. Output bit flips hover near 50%, indicating strong non-linear randomness.
