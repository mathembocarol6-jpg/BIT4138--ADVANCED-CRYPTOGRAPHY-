class LFSR:
    def __init__(self, size, taps, seed):
        if seed == 0:
            raise ValueError("Seed cannot be 0.")
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

if __name__ == "__main__":
    bit_width = 8
    active_taps = [8, 6, 5, 4]
    initial_seed = 0b10110011
    
    lfsr = LFSR(size=bit_width, taps=active_taps, seed=initial_seed)
    
    stream_length = 32
    raw_bits = lfsr.generate_bit_stream(stream_length)
    
    bit_string = ", ".join(map(str, raw_bits))
    
    print("--- LFSR Pseudorandom Sequence Output ---")
    print(f"Configuration: {bit_width}-bit width, Taps at {active_taps}")
    print(f"Initial Seed:  {bin(initial_seed)} (Decimal: {initial_seed})")
    print(f"\nGenerated Bitstream (First {stream_length} Cycles):")
    print(f"[{bit_string}]")
    
    print("\nFormatted as 8-bit Bytes:")
    for i in range(0, len(raw_bits), 8):
        byte_bits = raw_bits[i:i+8]
        byte_str = "".join(map(str, byte_bits))
        decimal_val = int(byte_str, 2)
        hex_val = hex(decimal_val).upper().replace("0X", "0x")
        print(f"Byte {i//8 + 1}: {byte_str} -> Decimal: {decimal_val:<3} | Hex: {hex_val}")
        
