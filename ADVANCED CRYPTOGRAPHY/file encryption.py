import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def encrypt_file(input_filepath, output_filepath, key):
    with open(input_filepath, 'rb') as f:
        file_data = f.read()

    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, file_data, None)

    with open(output_filepath, 'wb') as f:
        f.write(nonce + ciphertext)

if __name__ == "__main__":
    target_file = "sensitive_report.txt"
    protected_file = "sensitive_report.txt.enc"

    with open(target_file, "w") as f:
        f.write("CONFIDENTIAL: Project Jaguars training parameters start at 1600hrs.")

    secret_key = AESGCM.generate_key(bit_length=256)

    print("--- Local File Encryption Process ---")
    print(f"Targeting Plaintext File:   '{target_file}'")
    
    encrypt_file(target_file, protected_file, secret_key)
    
    print(f"File Successfully Encrypted: '{protected_file}'")
    print(f"Secret Key (Hex Required):  0x{secret_key.hex().upper()}")
