import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def generate_aes_key():
    return AESGCM.generate_key(bit_length=256)

def aes_gcm_encrypt(plaintext, key):
    if isinstance(plaintext, str):
        plaintext_bytes = plaintext.encode('utf-8')
    else:
        plaintext_bytes = plaintext

    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext_bytes, None)
    return nonce + ciphertext

def aes_gcm_decrypt(combined_ciphertext, key):
    nonce = combined_ciphertext[:12]
    actual_ciphertext = combined_ciphertext[12:]
    
    aesgcm = AESGCM(key)
    plaintext_bytes = aesgcm.decrypt(nonce, actual_ciphertext, None)
    return plaintext_bytes.decode('utf-8')

if __name__ == "__main__":
    secret_message = "today's training starts at 1600hrs"
    
    secret_key = generate_aes_key()
    
    encrypted_payload = aes_gcm_encrypt(secret_message, secret_key)
    
    decrypted_message = aes_gcm_decrypt(encrypted_payload, secret_key)
    
    print("--- AES-256-GCM Encryption Script ---")
    print(f"Plaintext:  {secret_message}")
    print(f"Key (Hex):  {secret_key.hex().upper()}")
    print(f"Ciphertext: 0x{encrypted_payload.hex().upper()}")
    print(f"Decrypted:  {decrypted_message}")
