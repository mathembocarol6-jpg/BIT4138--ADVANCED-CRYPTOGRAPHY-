import tkinter as tk
from tkinter import messagebox
import re
import os
import math
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class LFSR:
    def __init__(self, size, taps, seed):
        if seed == 0:
            raise ValueError("Seed cannot be 0.")
        self.size = size
        self.taps = taps
        self.state = seed & ((1 << size) - 1)

    def step(self):
        feedback = 0
        for tap in self.taps:
            feedback ^= (self.state >> (self.size - tap)) & 1
        output_bit = self.state & 1
        self.state = (self.state >> 1) | (feedback << (self.size - 1))
        return output_bit

    def generate_bit_stream(self, length):
        return [self.step() for _ in range(length)]

def caesar_cipher(text, shift, mode='encrypt'):
    result = ""
    if mode == 'decrypt':
        shift = -shift
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            new_char = chr((ord(char) - start + shift) % 26 + start)
            result += new_char
        else:
            result += char
    return result

def vigenere_cipher(text, key, mode='encrypt'):
    result = []
    key = key.upper()
    key_index = 0
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            key_char = key[key_index % len(key)]
            shift = ord(key_char) - ord('A')
            if mode == 'decrypt':
                shift = -shift
            new_char = chr((ord(char) - start + shift) % 26 + start)
            result.append(new_char)
            key_index += 1
        else:
            result.append(char)
    return "".join(result)

def rc4_ksa(key):
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def rc4_prga(S, text_length):
    i = 0
    j = 0
    keystream = []
    for _ in range(text_length):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % 256
        keystream.append(S[t])
    return keystream

def rc4_crypt(text, key_string):
    key = [ord(c) for c in key_string]
    if isinstance(text, str):
        text_bytes = [ord(c) for c in text]
    else:
        text_bytes = text
    S = rc4_ksa(key)
    keystream = rc4_prga(S, len(text_bytes))
    return [b ^ k for b, k in zip(text_bytes, keystream)]

def run_statistical_tests(bit_stream):
    n = len(bit_stream)
    if n == 0:
        return 0.0, 0.0
    
    s_n = sum(1 if bit == 1 else -1 for bit in bit_stream)
    s_obs = abs(s_n) / math.sqrt(n)
    p_freq = math.erfc(s_obs / math.sqrt(2))
    
    p_val = sum(bit_stream) / n
    v_n = 1
    for i in range(n - 1):
        if bit_stream[i] != bit_stream[i + 1]:
            v_n += 1
    num = abs(v_n - (2 * n * p_val * (1 - p_val)))
    den = 2 * math.sqrt(2 * n) * p_val * (1 - p_val)
    p_runs = math.erfc(num / den) if den != 0 else 0.0
    
    return p_freq, p_runs

class CryptoSuiteInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Integrated Cryptographic Suite")
        self.root.geometry("520 dropped_nodes")
        self.root.geometry("520x580")
        self.root.configure(bg="#f4f6f9")

        header = tk.Label(root, text="Multi-Layer Encryption Framework", font=("Arial", 14, "bold"), fg="#1e293b", bg="#f4f6f9")
        header.pack(pady=15)

        tk.Label(root, text="Secret Message Input:", font=("Arial", 10, "bold"), fg="#475569", bg="#f4f6f9").pack(anchor="w", padx=20)
        self.text_input = tk.Entry(root, font=("Arial", 11), width=52, bd=2, relief="groove")
        self.text_input.pack(pady=5, padx=20)

        tk.Label(root, text="Cryptographic Alphanumeric Key:", font=("Arial", 10, "bold"), fg="#475569", bg="#f4f6f9").pack(anchor="w", padx=20)
        self.key_input = tk.Entry(root, font=("Arial", 11), width=52, bd=2, relief="groove")
        self.key_input.pack(pady=5, padx=20)

        tk.Label(root, text="Caesar Shift Range Integer (1 to 25
