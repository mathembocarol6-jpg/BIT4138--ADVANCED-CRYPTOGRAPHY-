import os
import time
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class SecureTransmissionNode:
    def __init__(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()

    def get_serialized_public_key(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

def sender_transmit_payload(plaintext_message, receiver_public_key_bytes):
    receiver_pub_key = serialization.load_pem_public_key(receiver_public_key_bytes)
    
    session_key = AESGCM.generate_key(bit_length=256)
    
    encrypted_session_key = receiver_pub_key.encrypt(
        session_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    aesgcm = AESGCM(session_key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext_message.encode('utf-8'), None)
    
    return {
        "encrypted_key": encrypted_session_key,
        "nonce": nonce,
        "ciphertext": ciphertext
    }

def receiver_ingest_payload(encrypted_packet, receiver_node):
    session_key = receiver_node.private_key.decrypt(
        encrypted_packet["encrypted_key"],
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    aesgcm = AESGCM(session_key)
    decrypted_bytes = aesgcm.decrypt(
        encrypted_packet["nonce"],
        encrypted_packet["ciphertext"],
        None
    )
    
    return decrypted_bytes.decode('utf-8')

if __name__ == "__main__":
    print("--- Initializing Secure Transmission Network ---")
    bob_node = SecureTransmissionNode()
    bob_public_directory = bob_node.get_serialized_public_key()
    
    secret_data = "CONFIDENTIAL: Project Jaguars training parameters start at 1600hrs."
    print(f"\n1. Alice prepares plaintext transmission:\n   -> '{secret_data}'")
    
    start_enc = time.perf_counter_ns()
    transmission_packet = sender_transmit_payload(secret_data, bob_public_directory)
    end_enc = time.perf_counter_ns()
    
    print("\n2. Alice compiles secure digital network packet:")
    print(f"   -> Encrypted Session Key (Hex): 0x{transmission_packet['encrypted_key'].hex().upper()[:40]}...")
    print(f"   -> Nonce / IV Vector (Hex):    0x{transmission_packet['nonce'].hex().upper()}")
    print(f"   -> Symmetric Ciphertext (Hex): 0x{transmission_packet['ciphertext'].hex().upper()[:40]}...")
    print(f"   -> Processing Overhead:         {(end_enc - start_enc)/1000:.2f} μs")
    
    print("\n3. Network packet transmitted over public infrastructure...")
    
    start_dec = time.perf_counter_ns()
    recovered_plaintext = receiver_ingest_payload(transmission_packet, bob_node)
    end_dec = time.perf_counter_ns()
    
    print("\n4. Bob decrypts and authenticates inbound packet:")
    print(f"   -> Decryption Integrity Check:  PASSED (AES-GCM Auth Tag Match)")
    print(f"   -> Processing Overhead:         {(end_dec - start_dec)/1000:.2f} μs")
    print(f"   -> Decoded Message:             '{recovered_plaintext}'")
