import base64
import hashlib
import hmac
import json
import os
import sys
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def pulse_effect(message, duration=0.5):
    """Clean fallback indicator for Python IDLE shell compatibility."""
    print(f">> {message}...")
    time.sleep(duration)


def check_key_strength(key, key_type):
    if len(key) < 6:
        print(f"  ⚠ [WEAK KEY WARNING]: '{key_type}' is too short. Recommend 8+ characters.")


def vigenere_cipher(text, key, mode="encrypt"):
    result = []
    key = key.lower()
    if not key:
        return text
    for i, char in enumerate(text):
        if char.isdigit():
            shift = ord(key[i % len(key)]) - ord("a")
            if mode == "decrypt":
                shift = -shift
            new_char = chr(((ord(char) - ord("0") + shift) % 10) + ord("0"))
            result.append(new_char)
        elif char.isalpha():
            shift = ord(key[i % len(key)]) - ord("a")
            if mode == "decrypt":
                shift = -shift
            base = ord("A") if char.isupper() else ord("a")
            new_char = chr(((ord(char) - base + shift) % 26) + base)
            result.append(new_char)
        else:
            result.append(char)
    return "".join(result)


def derive_aes_key(user_key_string):
    return hashlib.sha256(user_key_string.encode("utf-8")).digest()


def aes_encrypt(plaintext, key_string):
    key = derive_aes_key(key_string)
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext.encode("utf-8"), AES.block_size))
    combined = cipher.iv + ciphertext
    return base64.b64encode(combined).decode("utf-8")


def aes_decrypt(ciphertext_b64, key_string):
    try:
        key = derive_aes_key(key_string)
        combined = base64.b64decode(ciphertext_b64.encode("utf-8"))
        iv = combined[:16]
        ciphertext = combined[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return plaintext.decode("utf-8")
    except Exception:
        return None


print("=" * 55)
print("     SECURE DOCUMENT STORAGE SYSTEM (BIT4138)")
print("=" * 55 + "\n")

doc_id = input("Enter Document Name/ID: ").strip()
doc_content = input("Enter Document Text Content: ").strip()

print("\n--- CREDENTIAL INITIALIZATION ---")
vigenere_key = input("Set metadata obfuscation key (Vigenere): ").strip()
check_key_strength(vigenere_key, "Vigenere Key")

aes_key_input = input("Set master system storage key (AES Key): ").strip()
check_key_strength(aes_key_input, "AES Key")

hmac_key_input = input("Set verification signature key (HMAC Key): ").strip()
check_key_strength(hmac_key_input, "HMAC Key")

print("\n--- Securing Document Asset ---")
pulse_effect("Obfuscating metadata indexes via Vigenère implementation")
obfuscated_ref = vigenere_cipher(doc_id, vigenere_key, mode="encrypt")
print(f" [✓] [Classic Stage] Obfuscated Doc Reference: {obfuscated_ref}")

pulse_effect("Executing AES-256 Block Cipher Encryption")
protected_payload = aes_encrypt(doc_content, aes_key_input)
print(f" [✓] [Symmetric Stage] AES-256 Protected Payload: {protected_payload}")

pulse_effect("Generating high-entropy HMAC-SHA256 integrity tag")
generated_hmac = hmac.new(
    hmac_key_input.encode("utf-8"),
    protected_payload.encode("utf-8"),
    hashlib.sha256,
).hexdigest()
print(f" [✓] [Hash Stage] Generated Verification HMAC: {generated_hmac}")

manifest = {
    "target_ref": obfuscated_ref,
    "crypto_blob": protected_payload,
    "integrity_checksum": generated_hmac,
}
print("\n[MANIFEST LOG] Document Saved in Manifest JSON Format:")
print(json.dumps(manifest, indent=2))

print("\n" + "=" * 55)
print("          RECOVERY & VERIFICATION SIMULATION")
print("=" * 55 + "\n")

recovery_hmac_key = input("Provide verification checksum to unlock record: ").strip()
inject_malicious = (
    input("Inject malicious document modification? (yes/no): ")
    .strip()
    .lower()
)

simulated_payload = protected_payload
if inject_malicious == "yes":
    simulated_payload += "X"
    print("  ⚡ [TAMPERING ACTIVE]: Appended rogue data to payload.")

pulse_effect("Running cryptographic checksum validation")

calculated_hmac = hmac.new(
    recovery_hmac_key.encode("utf-8"),
    simulated_payload.encode("utf-8"),
    hashlib.sha256,
).hexdigest()

if calculated_hmac != generated_hmac:
    print("\n[CRITICAL ERROR]: Cryptographic verification failed.")
    print("Reason: Document is physically corrupted or HMAC validation key is incorrect.")
else:
    print("\n[SUCCESS]: Cryptographic integrity verified.")
    pulse_effect("Reversing cryptographic pipeline layers")

    decrypted_content = aes_decrypt(simulated_payload, aes_key_input)
    recovered_id = vigenere_cipher(obfuscated_ref, vigenere_key, mode="decrypt")

    if decrypted_content is not None:
        print("\n--- RECOVERED ASSET PLAINTEXT ---")
        print(f"🔓 Decrypted Document ID: {recovered_id}")
        print(f"🔓 Decrypted Content:     {decrypted_content}")
    else:
        print("\n[ERROR]: Integrity hash verified but AES Decryption failed. Check Master Key.")
