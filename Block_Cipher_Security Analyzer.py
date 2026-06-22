import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import collections
import math

S_BOX_8BIT = [
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
P_BOX = [0, 4, 1, 5, 2, 6, 3, 7]

def encrypt_block(byte_value, master_key, rounds):
    state = byte_value
    for r in range(rounds):
        shift = r % 8
        round_key = ((master_key >> shift) | (master_key << (8 - shift))) & 0xFF
        state ^= round_key
        state = S_BOX_8BIT[state]
        permuted = 0
        for orig, target in enumerate(P_BOX):
            bit = (state >> (7 - orig)) & 1
            permuted |= (bit << (7 - target))
        state = permuted
    shift = rounds % 8
    final_key = ((master_key >> shift) | (master_key << (8 - shift))) & 0xFF
    state ^= final_key
    return state

def encrypt_string(text, master_key, rounds):
    return [encrypt_block(ord(c), master_key, rounds) for c in text]

class CryptanalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Block Cipher Security Analyzer")
        self.root.geometry("850x650")
        self.root.configure(bg="#F1F5F9")
        self.saved_report = ""

        header = tk.Frame(root, bg="#0F172A", height=60)
        header.pack(fill="x", side="top")
        tk.Label(header, text="BLOCK CIPHER SECURITY LABS", fg="#38BDF8", bg="#0F172A", font=("Helvetica", 14, "bold")).pack(pady=15)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=10)

        self.tab_dashboard = tk.Frame(self.notebook, bg="#FFFFFF")
        self.tab_charts = tk.Frame(self.notebook, bg="#FFFFFF")
        self.notebook.add(self.tab_dashboard, text="Analysis Dashboard")
        self.notebook.add(self.tab_charts, text="Visual Charts")

        self.setup_dashboard_ui()
        self.setup_charts_ui()

    def setup_dashboard_ui(self):
        left_panel = tk.Frame(self.tab_dashboard, bg="#FFFFFF", width=300)
        left_panel.pack(side="left", fill="y", padx=15, pady=15)

        tk.Label(left_panel, text="Cipher Configurations", font=("Helvetica", 11, "bold"), fg="#1E293B", bg="#FFFFFF").pack(anchor="w", pady=(0,10))
        
        tk.Label(left_panel, text="Master Key (Hex 00-FF):", bg="#FFFFFF").pack(anchor="w")
        self.key_entry = tk.Entry(left_panel, font=("Courier", 10), bd=1, relief="solid")
        self.key_entry.insert(0, "A5")
        self.key_entry.pack(fill="x", pady=(2,10))

        tk.Label(left_panel, text="Rounds Count:", bg="#FFFFFF").pack(anchor="w")
        self.rounds_box = ttk.Combobox(left_panel, values=["1", "2", "4", "8", "16"], state="readonly")
        self.rounds_box.set("4")
        self.rounds_box.pack(fill="x", pady=(2,15))

        tk.Label(left_panel, text="Plaintext Vector 1:", font=("Helvetica", 10, "bold"), bg="#FFFFFF").pack(anchor="w")
        self.pt1_entry = tk.Entry(left_panel, font=("Helvetica", 10), bd=1, relief="solid")
        self.pt1_entry.insert(0, "Musyoka Boniface")
        self.pt1_entry.pack(fill="x", pady=(2,10))

        tk.Label(left_panel, text="Plaintext Vector 2 (Avalanche Testing):", font=("Helvetica", 10, "bold"), bg="#FFFFFF").pack(anchor="w")
        self.pt2_entry = tk.Entry(left_panel, font=("Helvetica", 10), bd=1, relief="solid")
        self.pt2_entry.insert(0, "Musyoka Coniface")
        self.pt2_entry.pack(fill="x", pady=(2,15))

        tk.Button(left_panel, text="RUN SECURITY ANALYSIS", bg="#0284C7", fg="#FFFFFF", font=("Helvetica", 10, "bold"), bd=0, pady=8, command=self.execute_analysis).pack(fill="x", pady=5)
        tk.Button(left_panel, text="EXPORT RESULTS REPORT", bg="#10B981", fg="#FFFFFF", font=("Helvetica", 10, "bold"), bd=0, pady=8, command=self.export_report).pack(fill="x", pady=5)

        right_panel = tk.Frame(self.tab_dashboard, bg="#FFFFFF")
        right_panel.pack(side="right", fill="both", expand=True, padx=15, pady=15)

        tk.Label(right_panel, text="Statistical Analysis Output Reports", font=("Helvetica", 11, "bold"), fg="#1E293B", bg="#FFFFFF").pack(anchor="w", pady=(0,5))
        self.report_box = tk.Text(right_panel, bg="#0F172A", fg="#38BDF8", font=("Courier", 10), bd=1, relief="solid")
        self.report_box.pack(fill="both", expand=True)

    def setup_charts_ui(self):
        self.chart_canvas = tk.Canvas(self.tab_charts, bg="#F8FAFC", bd=0, highlightthickness=0)
        self.chart_canvas.pack(fill="both", expand=True, padx=20, pady=20)

    def execute_analysis(self):
        try:
            key_val = int(self.key_entry.get().strip(), 16) & 0xFF
        except ValueError:
            messagebox.showerror("Configuration Error", "Invalid master key. Supply an 8-bit hex sequence (00-FF).")
            return
        
        rounds = int(self.rounds_box.get())
        pt1 = self.pt1_entry.get()
        pt2 = self.pt2_entry.get()

        if not pt1 or not pt2:
            messagebox.showwarning("Input Error", "Both plaintexts are required for comparative testing.")
            return

        c1 = encrypt_string(pt1, key_val, rounds)
        c2 = encrypt_string(pt2, key_val, rounds)

        max_len = max(len(c1), len(c2))
        c1_padded = c1 + [0] * (max_len - len(c1))
        c2_padded = c2 + [0] * (max_len - len(c2))

        xor_diffs = []
        flipped_bits = 0
        total_bits = max_len * 8

        for x, y in zip(c1_padded, c2_padded):
            diff = x ^ y
            xor_diffs.append(f"{diff:02X}")
            flipped_bits += bin(diff).count('1')

        avalanche_pct = (flipped_bits / total_bits) * 100 if total_bits > 0 else 0

        c1_hex_list = [f"{b:02X}" for b in c1]
        counts = collections.Counter(c1_hex_list)
        total_bytes = len(c1)
        freq_report = ""
        for token, count in counts.most_common(5):
            freq_report += f"     Byte [0x{token}]: Occurred {count} times ({(count/total_bytes)*100:.1f}%)\n"

        ones_count = sum(bin(b).count('1') for b in c1)
        zeros_count = (len(c1) * 8) - ones_count
        measured_bias = abs((ones_count / (len(c1) * 8)) - 0.5) if len(c1) > 0 else 0

        c1_string = " ".join(c1_hex_list)
        c2_string = " ".join(f"{b:02X}" for b in c2)

        self.saved_report = f"==================================================================\n" \
                            f"               SPN CIPHER LAB SECURITY REPORT                     \n" \
                            f"==================================================================\n" \
                            f"Cipher Configuration Parameters:\n" \
                            f"  - Encryption Rounds: {rounds}\n" \
                            f"  - Master Secret Key: 0x{key_val:02X}\n\n" \
                            f"Difference Analysis Output Vector Logs:\n" \
                            f"  - Ciphertext 1 Hex : {c1_string}\n" \
                            f"  - Ciphertext 2 Hex : {c2_string}\n" \
                            f"  - Byte XOR Profiles: {' '.join(xor_diffs)}\n\n" \
                            f"Avalanche Performance Evaluation:\n" \
                            f"  - Inspected Bit Register Width : {total_bits} Bits\n" \
                            f"  - Confirmed Bit Flip Count    : {flipped_bits} Bits\n" \
                            f"  - Strict Avalanche Percentage : {avalanche_pct:.2f}% (Target: 50.00%)\n\n" \
                            f"Frequency Distribution Spectrum (Top 5 Bytes):\n" \
                            f"{freq_report}\n" \
                            f"Linear Bit-Density Statistical Profile:\n" \
                            f"  - Bit Density Counter Metrics : 1s = {ones_count} | 0s = {zeros_count}\n" \
                            f"  - Measured Statistical Bias   : {measured_bias:.4f} (Ideal: 0.0000)\n" \
                            f"=================================================================="

        self.report_box.delete("1.0", tk.END)
        self.report_box.insert("1.0", self.saved_report)

        self.draw_custom_charts(ones_count, zeros_count, avalanche_pct)

    def draw_custom_charts(self, ones, zeros, avalanche_val):
        self.chart_canvas.delete("all")
        
        self.chart_canvas.create_text(180, 40, text="Ciphertext Bit Density Split", font=("Helvetica", 12, "bold"), fill="#1E293B")
        total = ones + zeros
        if total > 0:
            one_pct = ones / total
            zero_pct = zeros / total
            
            self.chart_canvas.create_rectangle(60, 100, 140, 280, fill="#E2E8F0", outline="")
            self.chart_canvas.create_rectangle(60, 280 - (180 * one_pct), 140, 280, fill="#0EA5E9", outline="")
            self.chart_canvas.create_text(100, 295, text=f"Ones ({(one_pct*100):.1f}%)", font=("Helvetica", 9))

            self.chart_canvas.create_rectangle(180, 100, 260, 280, fill="#E2E8F0", outline="")
            self.chart_canvas.create_rectangle(180, 280 - (180 * zero_pct), 260, 280, fill="#64748B", outline="")
            self.chart_canvas.create_text(220, 295, text=f"Zeros ({(zero_pct*100):.1f}%)", font=("Helvetica", 9))

        self.chart_canvas.create_text(520, 40, text="Avalanche Effect Meter Gauge", font=("Helvetica", 12, "bold"), fill="#1E293B")
        
        self.chart_canvas.create_arc(400, 100, 640, 340, start=0, extent=180, fill="#E2E8F0", outline="")
        self.chart_canvas.create_arc(400, 100, 640, 340, start=180 - 55, extent=10, fill="#10B981", outline="")
        
        angle_rad = math.radians(180 - (avalanche_val if avalanche_val <= 180 else 180))
        needle_length = 100
        center_x, center_y = 520, 220
        end_x = center_x + needle_length * math.cos(angle_rad)
        end_y = center_y - needle_length * math.sin(angle_rad)
        
        self.chart_canvas.create_line(center_x, center_y, end_x, end_y, fill="#EF4444", width=3, arrow="last")
        self.chart_canvas.create_oval(center_x-6, center_y-6, center_x+6, center_y+6, fill="#0F172A")
        self.chart_canvas.create_text(520, 245, text=f"Current: {avalanche_val:.2f}%", font=("Helvetica", 11, "bold"), fill="#EF4444")
        self.chart_canvas.create_text(520, 265, text="Optimal Performance Target: 50.0%", font=("Helvetica", 8, "italic"), fill="#64748B")

    def export_report(self):
        if not self.saved_report:
            messagebox.showwarning("Export Void", "Please execute a security analysis verification pass before trying to export records.")
            return
        
        target_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if target_path:
            try:
                with open(target_path, "w") as out_file:
                    out_file.write(self.saved_report)
                messagebox.showinfo("Export Complete", f"Cryptanalysis documentation successfully saved to:\n{target_path}")
            except Exception as e:
                messagebox.showerror("Export Exception", f"An error occurred while writing output logs to disk:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptanalyzerApp(root)
    root.mainloop()
