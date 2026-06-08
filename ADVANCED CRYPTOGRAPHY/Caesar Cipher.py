def caesar_cipher(text, shift, mode='encrypt'):
    result = ""
    if mode == 'decrypt':
        shift = -shift

    for char in text:
        if char.isalpha():
            start = ord('A') if char.isupper() else ord('a')
            new_char = chr((ord(char) - start + shift) % 26 + start)
            result += new_char
        else:
            result += char
            
    return result

if __name__ == "__main__":
    secret_message = "execution today at noon, meet 10 minutes to time opposite Nairobi City Hall gate"
    shift_value = 4
    
    encrypted = caesar_cipher(secret_message, shift_value, mode='encrypt')
    print(f"Plaintext:  {secret_message}")
    print(f"Encrypted:  {encrypted}")
    
    decrypted = caesar_cipher(encrypted, shift_value, mode='decrypt')
    print(f"Decrypted:  {decrypted}")
