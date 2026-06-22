S_BOX = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]
P_BOX = [0, 4, 1, 5, 2, 6, 3, 7]

def substitute(byte_value):
    left_nibble = (byte_value >> 4) & 0x0F
    right_nibble = byte_value & 0x0F
    return (S_BOX[left_nibble] << 4) | S_BOX[right_nibble]

def permutate(byte_value):
    permuted_byte = 0
    for original_pos, target_pos in enumerate(P_BOX):
        bit = (byte_value >> (7 - original_pos)) & 1
        permuted_byte |= (bit << (7 - target_pos))
    return permuted_byte

def encrypt_spn(plaintext_string):
    ciphertext_hex = []
    print("\n--- Encryption Process Breakdown ---")
    for char in plaintext_string:
        original_byte = ord(char)
        sub_byte = substitute(original_byte)
        encrypted_byte = permutate(sub_byte)
        ciphertext_hex.append(f"{encrypted_byte:02X}")
        
        print(f"Char: '{char}' | Plaintext Byte: {original_byte:08b} (0x{original_byte:02X})")
        print(f"       -> After S-Box:     {sub_byte:08b} (0x{sub_byte:02X})")
        print(f"       -> After P-Box:     {encrypted_byte:08b} (0x{encrypted_byte:02X})")
        print("-" * 40)
    return " ".join(ciphertext_hex)

if __name__ == "__main__":
    print("=== Basic SPN Cipher Studio ===")
    user_input = input("Enter plaintext to encrypt: ")
    if not user_input:
        print("Plaintext cannot be empty.")
    else:
        final_ciphertext = encrypt_spn(user_input)
        print("\n=== Final Deliverable Output ===")
        print(f"Plaintext:  {user_input}")
        print(f"Ciphertext: {final_ciphertext}")
