from cryptography.fernet import Fernet

def encrypt_string():
    key = Fernet.generate_key()
    fernet = Fernet(key)
    
    secret_text = "musyoka#bonny"
    
    encoded_text = secret_text.encode()
    
    encrypted_text = fernet.encrypt(encoded_text)
    
    decrypted_text = fernet.decrypt(encrypted_text).decode()
    
    print(f"🔑 Generated Key: {key.decode()}")
    print(f"🔒 Encrypted:     {encrypted_text.decode()}")
    print(f"🔓 Decrypted:     {decrypted_text}")

if __name__ == "__main__":
    encrypt_string()
