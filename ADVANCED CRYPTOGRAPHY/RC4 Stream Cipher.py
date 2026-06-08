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
    
    out_bytes = [b ^ k for b, k in zip(text_bytes, keystream)]
    return out_bytes

if __name__ == "__main__":
    secret_message = "today's training starts at 1600hrs"
    encryption_key = "Jaguars"
    
    encrypted_bytes = rc4_crypt(secret_message, encryption_key)
    encrypted_hex = "".join(f"{b:02x}" for b in encrypted_bytes)
    
    decrypted_bytes = rc4_crypt(encrypted_bytes, encryption_key)
    decrypted_message = "".join(chr(b) for b in decrypted_bytes)
    
    print("--- RC4 Stream Cipher Simulation ---")
    print(f"Plaintext:  {secret_message}")
    print(f"Key:        {encryption_key}")
    print(f"Ciphertext: 0x{encrypted_hex.upper()}")
    print(f"Decrypted:  {decrypted_message}")
