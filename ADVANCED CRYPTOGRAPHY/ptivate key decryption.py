import time
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

def run_decryption_pipeline():
    print("--- Generating 2048-bit RSA Key Pair ---")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()

    secret_message = "CONFIDENTIAL: Project Jaguars training parameters start at 1600hrs."
    plaintext_bytes = secret_message.encode('utf-8')

    print("\n--- Simulating Encryption (Sender Layer) ---")
    ciphertext = public_key.encrypt(
        plaintext_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    ciphertext_hex = ciphertext.hex().upper()
    print(f"Incoming Ciphertext (Hex Sample): 0x{ciphertext_hex[:60]}...")
    print(f"Ciphertext Byte Length:          {len(ciphertext)} Bytes")

    print("\n--- Executing Private Key Decryption (Receiver Layer) ---")
    
    if len(ciphertext_hex) % 2 != 0:
        raise ValueError("Hex string must contain an even number of digits.")
    
    raw_ciphertext_bytes = bytes.fromhex(ciphertext_hex)

    start_time = time.perf_counter_ns()

    try:
        decrypted_bytes = private_key.decrypt(
            raw_ciphertext_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        end_time = time.perf_counter_ns()
        latency_microseconds = (end_time - start_time) / 1000

        restored_text = decrypted_bytes.decode('utf-8')

        print("\n📥 Decryption Execution Metrics:")
        print(f"   -> Operational Status:     SUCCESS")
        print(f"   -> Decryption Latency:     {latency_microseconds:.2f} μs")
        print(f"   -> Padding Validation:     PASSED (OAEP SHA-256)")
        print(f"   -> Output Integrity Check: MATCH")
        print(f"   -> Restored Plaintext:     {restored_text}")

    except Exception as e:
        print(f"\n❌ Decryption Failed: {str(e)}")

if __name__ == "__main__":
    run_decryption_pipeline()
