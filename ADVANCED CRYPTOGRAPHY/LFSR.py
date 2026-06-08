class LFSR:
    def __init__(self, size, taps, seed):
        if seed == 0:
            raise ValueError("Seed cannot be 0. An all-zero state causes a dead lock.")
        self.size = size
        self.taps = taps
        self.state = seed & ((1 << size) - 1)
    def step(self):
        feedback = 0
        for tap in self.taps:
            feedback ^= (self.state >> (self.size - tap)) & 1
        output_bit = self.state & 1
        self.state = (self.state >> 1) | (feedback << (self.size - 1))
        return output_bit
    def generate_bit_stream(self, length):
        return [self.step() for _ in range(length)]
    def generate_integer(self, bits):
        val = 0
        for _ in range(bits):
            val = (val << 1) | self.step()
        return val
if __name__ == "__main__":
    message = "today's training starts at 1600hrs"
    message_bits = []
    for char in message:
        char_bits = format(ord(char), '08b')
        message_bits.extend([int(b) for b in char_bits])
    bit_width = 8
    active_taps = [8, 6, 5, 4]
    initial_seed = 0b10110011
    lfsr = LFSR(size=bit_width, taps=active_taps, seed=initial_seed)
    keystream = lfsr.generate_bit_stream(len(message_bits))
    encrypted_bits = [m_bit ^ k_bit for m_bit, k_bit in zip(message_bits, keystream)]
    encrypted_chars = []
    for i in range(0, len(encrypted_bits), 8):
        byte = encrypted_bits[i:i+8]
        byte_str = "".join(map(str, byte))
        encrypted_chars.append(chr(int(byte_str, 2)))
    encrypted_message = "".join(encrypted_chars)
    lfsr_decrypt = LFSR(size=bit_width, taps=active_taps, seed=initial_seed)
    decrypt_keystream = lfsr_decrypt.generate_bit_stream(len(encrypted_bits))
    decrypted_bits = [e_bit ^ k_bit for e_bit, k_bit in zip(encrypted_bits, decrypt_keystream)]
    decrypted_chars = []
    for i in range(0, len(decrypted_bits), 8):
        byte = decrypted_bits[i:i+8]
        byte_str = "".join(map(str, byte))
        decrypted_chars.append(chr(int(byte_str, 2)))
    decrypted_message = "".join(decrypted_chars)
    print(f"Plaintext:         {message}")
    print(f"Encrypted (Raw):   {encrypted_message.encode('utf-8', errors='replace')}")
    print(f"Decrypted:         {decrypted_message}")
