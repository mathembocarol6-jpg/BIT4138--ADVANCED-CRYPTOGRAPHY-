import tkinter as tk
from tkinter import messagebox, ttk
S_BOX = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
]
INV_S_BOX = [0] * 256
for index, value in enumerate(S_BOX):
    INV_S_BOX[value] = index
P_BOX = [0, 4, 1, 5, 2, 6, 3, 7]
INV_P_BOX = [0, 2, 4, 6, 1, 3, 5, 7]
def generate_subkeys(master_key, total_rounds):
    subkeys = []
    for round_index in range(total_rounds + 1):
        rotated_key = ((master_key >> round_index) | (master_key << (8 - round_index))) & 0xFF
        subkeys.append(rotated_key)
    return subkeys
def apply_permutation(byte_value, box_map):
    permuted = 0
    for original_pos, target_pos in enumerate(box_map):
        bit = (byte_value >> (7 - original_pos)) & 1
        permuted |= (bit << (7 - target_pos))
    return permuted
def encrypt_block(byte_value, subkeys, total_rounds):
    state = byte_value
    for r in range(total_rounds):
        state ^= subkeys[r]
        state = S_BOX[state]
        if r < total_rounds - 1:
            state = apply_permutation(state, P_BOX)
    state ^= subkeys[total_rounds]
    return state
def decrypt_block(byte_value, subkeys, total_rounds):
    state = byte_value
    state ^= subkeys[total_rounds]
    for r in range(total_rounds - 1, -1, -1):
        if r < total_rounds - 1:
            state = apply_permutation(state, INV_P_BOX)
        state = INV_S_BOX[state]
        state ^= subkeys[r]
    return state
class MiniAesSimulatorApp:
    def __init__(self, master_window):
        self.window = master_window
        self.window.title("Mini-AES Cryptography Studio")
        self.window.geometry("620x540")
        self.window.configure(bg="#F4F6F9")
        style = ttk.Style()
        style.theme_use("clam")
        header_frame = tk.Frame(self.window, bg="#1E293B", height=60)
        header_frame.pack(fill="x", side="top")
        header_label = tk.Label(header_frame, text="MINI-AES SPN ENCRYPTION LAB", fg="#FFFFFF", bg="#1E293B", font=("Helvetica", 14, "bold"))
        header_label.pack(pady=15)
        main_content_layout = tk.Frame(self.window, bg="#F4F6F9")
        main_content_layout.pack(pady=15, padx=20, fill="both", expand=True)
        config_frame = tk.LabelFrame(main_content_layout, text=" Cipher Configurations ", font=("Helvetica", 10, "bold"), bg="#FFFFFF", fg="#334155", bd=1, relief="solid")
        config_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5, padx=5)
        tk.Label(config_frame, text="Master Key (Hex 00-FF):", bg="#FFFFFF", font=("Helvetica", 10)).grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.key_entry_box = tk.Entry(config_frame, width=12, font=("Courier", 10, "bold"), bd=1, relief="solid")
        self.key_entry_box.insert(0, "A5")
        self.key_entry_box.grid(row=0, column=1, padx=10, pady=8, sticky="w")
        tk.Label(config_frame, text="Cipher Execution Rounds:", bg="#FFFFFF", font=("Helvetica", 10)).grid(row=0, column=2, padx=15, pady=8, sticky="w")
        self.rounds_combobox = ttk.Combobox(config_frame, values=["2", "4", "8", "16"], width=5, state="readonly")
        self.rounds_combobox.set("4")
        self.rounds_combobox.grid(row=0, column=3, padx=10, pady=8, sticky="w")
        tk.Label(main_content_layout, text="Input Data Field:", bg="#F4F6F9", font=("Helvetica", 10, "bold"), fg="#334155").grid(row=1, column=0, sticky="w", pady=(10,2), padx=5)
        self.input_text_area = tk.Text(main_content_layout, height=5, width=70, bd=1, relief="solid", font=("Courier", 10))
        self.input_text_area.insert("1.0", "Musyoka Boniface")
        self.input_text_area.grid(row=2, column=0, columnspan=2, pady=5, padx=5)
        buttons_group_frame = tk.Frame(main_content_layout, bg="#F4F6F9")
        buttons_group_frame.grid(row=3, column=0, columnspan=2, pady=10)
        self.encrypt_action_btn = tk.Button(buttons_group_frame, text="EXECUTE ENCRYPTION", bg="#0EA5E9", fg="#FFFFFF", font=("Helvetica", 10, "bold"), activebackground="#0284C7", activeforeground="#FFFFFF", bd=0, padx=15, pady=8, command=self.trigger_encryption)
        self.encrypt_action_btn.pack(side="left", padx=15)
        self.decrypt_action_btn = tk.Button(buttons_group_frame, text="EXECUTE DECRYPTION", bg="#10B981", fg="#FFFFFF", font=("Helvetica", 10, "bold"), activebackground="#059669", activeforeground="#FFFFFF", bd=0, padx=15, pady=8, command=self.trigger_decryption)
        self.decrypt_action_btn.pack(side="left", padx=15)
        tk.Label(main_content_layout, text="Output Processing Results Screen:", bg="#F4F6F9", font=("Helvetica", 10, "bold"), fg="#334155").grid(row=4, column=0, sticky="w", pady=(10,2), padx=5)
        self.output_text_area = tk.Text(main_content_layout, height=7, width=70, bd=1, relief="solid", bg="#0F172A", fg="#38BDF8", font=("Courier", 10), state="disabled")
        self.output_text_area.grid(row=5, column=0, columnspan=2, pady=5, padx=5)
    def parse_system_configurations(self):
        raw_key = self.key_entry_box.get().strip()
        try:
            master_key_integer = int(raw_key, 16)
            if not (0 <= master_key_integer <= 255):
                raise ValueError()
        except ValueError:
            messagebox.showerror("Configuration Error", "Master key token validation error. Please supply an 8-bit hex key between 00 and FF.")
            return None, None
        return master_key_integer, int(self.rounds_combobox.get())
    def update_results_screen(self, display_content):
        self.output_text_area.config(state="normal")
        self.output_text_area.delete("1.0", tk.END)
        self.output_text_area.insert("1.0", display_content)
        self.output_text_area.config(state="disabled")
    def trigger_encryption(self):
        master_key, total_rounds = self.parse_system_configurations()
        if master_key is None: return
        plaintext_payload = self.input_text_area.get("1.0", tk.END).strip()
        if not plaintext_payload:
            messagebox.showwarning("Execution Warning", "Input text area cannot be empty.")
            return
        subkeys_schedule = generate_subkeys(master_key, total_rounds)
        encrypted_hex_tokens = []
        for character in plaintext_payload:
            cipher_byte = encrypt_block(ord(character), subkeys_schedule, total_rounds)
            encrypted_hex_tokens.append(f"{cipher_byte:02X}")
        final_output_string = " ".join(encrypted_hex_tokens)
        display_log = f"=== ENCRYPTION DELIVERABLE LOG ===\n" \
                      f"Plaintext String : {plaintext_payload}\n" \
                      f"Master Hex Key   : 0x{master_key:02X}\n" \
                      f"Rounds Count     : {total_rounds}\n" \
                      f"Ciphertext (Hex) : {final_output_string}"
        self.update_results_screen(display_log)
    def trigger_decryption(self):
        master_key, total_rounds = self.parse_system_configurations()
        if master_key is None: return
        hex_ciphertext_payload = self.input_text_area.get("1.0", tk.END).strip()
        if not hex_ciphertext_payload:
            messagebox.showwarning("Execution Warning", "Input data missing hex strings.")
            return
        subkeys_schedule = generate_subkeys(master_key, total_rounds)
        decrypted_characters_array = []
        try:
            hex_data_tokens = hex_ciphertext_payload.split()
            for hex_token in hex_data_tokens:
                cipher_byte = int(hex_token, 16)
                plain_byte = decrypt_block(cipher_byte, subkeys_schedule, total_rounds)
                decrypted_characters_array.append(chr(plain_byte))
            reconstructed_plaintext = "".join(decrypted_characters_array)
            display_log = f"=== DECRYPTION DELIVERABLE LOG ===\n" \
                          f"Ciphertext Input   : {hex_ciphertext_payload}\n" \
                          f"Master Hex Key     : 0x{master_key:02X}\n" \
                          f"Rounds Count       : {total_rounds}\n" \
                          f"Decrypted (String) : {reconstructed_plaintext}"
            self.update_results_screen(display_log)
        except Exception:
            messagebox.showerror("Execution Fault", "Decryption pipeline failure. Confirm ciphertext formatting strings are space-separated hex bytes (e.g., 4A 7F 6B).")
if __name__ == "__main__":
    root_window = tk.Tk()
    app_engine = MiniAesSimulatorApp(root_window)
    root_window.mainloop()
