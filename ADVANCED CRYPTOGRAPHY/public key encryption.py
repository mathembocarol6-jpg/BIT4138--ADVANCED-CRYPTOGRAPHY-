from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

def simulate_public_key_pipeline(message_string):
    bob_private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    bob_public_key = bob_private_key.public_key()

    plaintext_bytes = message_string.encode('utf-8')
    ciphertext = bob_public_key.encrypt(
        plaintext_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    decrypted_bytes = bob_private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext, decrypted_bytes.decode('utf-8')

if __name__ == "__main__":
    secret_text = "CONFIDENTIAL: Project Jaguars training parameters start at 1600hrs."
    
    enc_payload, dec_message = simulate_public_key_pipeline(secret_text)
    
    print("--- Public Key Asymmetric Cryptography Simulation ---")
    print(f"Plaintext Input:  {secret_text}")
    print(f"Ciphertext (Hex): 0x{enc_payload.hex().upper()[:60]}...")
    print(f"Decrypted Result: {dec_message}")
