Python 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, 13:03:48) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> 
= RESTART: C:/Users/wes/AppData/Local/Programs/Python/Python313/Modified_SPN_Design.py
=== Multi-Round SPN Studio: Avalanche Evaluation ===
Enter a single plaintext character (e.g., M): Y
Enter custom 8-bit master key in Hex (e.g., A5): A4
Enter total cryptographic rounds (e.g., 4): 2

[Initial State Setup]
Plaintext 1: 'Y' -> 01011001
Plaintext 2: 'X' -> 01011000 (Flipped 1 bit)
Master Key:   0xA4 -> 10100100

=== Multi-Round Structural Bit Tracking ===
Round 0 (Input) | P1: 01011001 | P2: 01011000 | Flipped Bits: 1
Round 01 (State) | P1: 00001110 | P2: 11000100 | Flipped Bits: 4 (50.0%)
Round 02 (State) | P1: 00010001 | P2: 10101101 | Flipped Bits: 5 (62.5%)

=== Avalanche Phenomenon Analysis ===
Status: Complete. A 1-bit input variance produced a 5-bit change (62.5% structure distortion).
