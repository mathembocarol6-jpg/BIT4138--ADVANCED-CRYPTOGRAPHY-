from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def decrypt_file(input_filepath, output_filepath, key):
    with open(input_filepath, 'rb') as f:
        combined_data = f.read()

    nonce = combined_data[:12]
    actual_ciphertext = combined_data[12:]

    aesgcm = AESGCM(key)
    decrypted_data = aesgcm.decrypt(nonce, actual_ciphertext, None)

    with open(output_filepath, 'wb') as f:
        f.write(decrypted_data)

if __name__ == "__main__":
    protected_file = "sensitive_report.txt.enc"
    recovered_file = "restored_report.txt"
    
    key_hex_input = input("Enter the 64-character Secret Key (Hex): ").strip()
    
    if key_hex_input.lower().startswith("0x"):
        key_hex_input = key_hex_input[2:]
        
    if len(key_hex_input) != 64:
        print(f"\n❌ Input Length Error: Expected 64 characters, got {len(key_hex_input)}.")
        print("Please ensure the full key was copied completely from the encryption script output.")
    else:
        try:
            secret_key = bytes.fromhex(key_hex_input)
            print("\n--- Local File Decryption Process ---")
            print(f"Targeting Encrypted File:  '{protected_file}'")
            
            decrypt_file(protected_file, recovered_file, secret_key)
            
            print(f"File Successfully Decrypted: '{recovered_file}'")
            
            with open(recovered_file, "r") as f:
                print(f"Contents of Restored File:   '{f.read()}'")
        except ValueError as e:
            print(f"\n❌ Parsing Error: {e}. Check for non-hex characters.")
