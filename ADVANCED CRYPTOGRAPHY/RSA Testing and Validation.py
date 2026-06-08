import time
import math
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

def run_rsa_validation_suite():
    print("--- Phase 1: Key Pair Generation & Structural Audit ---")
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    
    priv_numbers = private_key.private_numbers()
    p, q, d, n = priv_numbers.p, priv_numbers.q, priv_numbers.d, priv_numbers.public_numbers.n
    e = priv_numbers.public_numbers.e
    
    phi = (p - 1) * (q - 1)
    lambda_n = math.lcm(p - 1, q - 1)
    
    inverse_check_phi = (e * d) % phi
    inverse_check_lambda = (e * d) % lambda_n
    
    structural_pass = (inverse_check_phi == 1) or (inverse_check_lambda == 1)
    
    print(f"   -> Modulus (n) Bit Length: {n.bit_length()} bits")
    print(f"   -> Multiplicative Inverse Verification: {'PASSED' if structural_pass else 'FAILED'}")

    print("\n--- Phase 2: Probabilistic Padding Randomness Test ---")
    msg = "CONFIDENTIAL: Secure Parameters Actioned."
    plaintext = msg.encode('utf-8')
    
    pad_engine = padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
    
    cipher1 = public_key.encrypt(plaintext, pad_engine)
    cipher2 = public_key.encrypt(plaintext, pad_engine)
    
    print(f"   -> Ciphertext 1 Sample: 0x{cipher1.hex().upper()[:30]}...")
    print(f"   -> Ciphertext 2 Sample: 0x{cipher2.hex().upper()[:30]}...")
    print(f"   -> Entropy Check (Outputs Distinct): {'PASSED' if cipher1 != cipher2 else 'FAILED'}")

    print("\n--- Phase 3: Mathematical Reciprocity Test ---")
    start_time = time.perf_counter_ns()
    decrypted = private_key.decrypt(cipher1, pad_engine)
    end_time = time.perf_counter_ns()
    
    restored_text = decrypted.decode('utf-8')
    print(f"   -> Decrypted Output: '{restored_text}'")
    print(f"   -> Functional Round-Trip: {'PASSED' if restored_text == msg else 'FAILED'}")
    print(f"   -> Compute Overhead: {(end_time - start_time)/1000:.2f} μs")

    print("\n--- Phase 4: Malicious Payload Injection & Tamper Test ---")
    tampered_cipher = bytearray(cipher1)
    tampered_cipher[10] ^= 0xFF
    tampered_cipher = bytes(tampered_cipher)
    
    try:
        private_key.decrypt(tampered_cipher, pad_engine)
        print("   -> Tamper Test: FAILED (System accepted corrupted payload)")
    except Exception:
        print("   -> Tamper Test: PASSED (System successfully caught and rejected modified bits)")

if __name__ == "__main__":
    print("=============================================")
    print("   RSA INFRASTRUCTURE TESTING AND VALIDATION ")
    print("=============================================\n")
    run_rsa_validation_suite()
    
