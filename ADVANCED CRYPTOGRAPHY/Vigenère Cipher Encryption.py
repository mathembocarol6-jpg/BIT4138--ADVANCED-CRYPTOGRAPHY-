def vigenere_cipher(text, key, mode='encrypt'):
    result = []
    key = key.upper()
    key_index = 0
    
    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            key_char = key[key_index % len(key)]
            shift = ord(key_char) - ord('A')
            
            if mode == 'decrypt':
                shift = -shift
                
            new_char = chr((ord(char) - start + shift) % 26 + start)
            result.append(new_char)
            key_index += 1
        else:
            result.append(char)
            
    return "".join(result)

if __name__ == "__main__":
    message = "today's passkey is MKU Jaguars"
    secret_key = "LEMON"
    
    encrypted = vigenere_cipher(message, secret_key, mode='encrypt')
    print(f"Plaintext:  {message}")
    print(f"Encrypted:  {encrypted}")
    
    decrypted = vigenere_cipher(encrypted, secret_key, mode='decrypt')
    print(f"Decrypted:  {decrypted}")
