import tkinter as tk
from tkinter import messagebox
import re

class ValidationInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Input Validation Interface")
        self.root.geometry("500x550")
        self.root.configure(bg="#f4f6f9")

        header = tk.Label(root, text="Input Validation & Sanity Controls", font=("Arial", 14, "bold"), fg="#1e293b", bg="#f4f6f9")
        header.pack(pady=15)

        tk.Label(root, text="Secret Message Input (No Special Scripting Symbols):", font=("Arial", 10, "bold"), fg="#475569", bg="#f4f6f9").pack(anchor="w", padx=20)
        self.text_input = tk.Entry(root, font=("Arial", 11), width=50, bd=2, relief="groove")
        self.text_input.pack(pady=5, padx=20)

        tk.Label(root, text="Cryptographic Key (Alphabetic Strings Only):", font=("Arial", 10, "bold"), fg="#475569", bg="#f4f6f9").pack(anchor="w", padx=20)
        self.key_input = tk.Entry(root, font=("Arial", 11), width=50, bd=2, relief="groove")
        self.key_input.pack(pady=5, padx=20)

        tk.Label(root, text="Caesar Shift Integer Range (Valid: 1 to 25):", font=("Arial", 10, "bold"), fg="#475569", bg="#f4f6f9").pack(anchor="w", padx=20)
        self.shift_input = tk.Entry(root, font=("Arial", 11), width=50, bd=2, relief="groove")
        self.shift_input.pack(pady=5, padx=20)

        self.validate_btn = tk.Button(root, text="Validate Framework Inputs", font=("Arial", 11, "bold"), bg="#2563eb", fg="white", activebackground="#1d4ed8", activeforeground="white", command=self.process_validation, bd=0, padx=10, pady=8)
        self.validate_btn.pack(pady=20)

        self.log_box = tk.Text(root, height=6, width=55, font=("Courier New", 9), bg="#0f172a", fg="#38bdf8", state="disabled")
        self.log_box.pack(pady=10)

    def write_log(self, text):
        self.log_box.config(state="normal")
        self.log_box.insert(tk.END, text + "\n")
        self.log_box.see(tk.END)
        self.log_box.config(state="disabled")

    def clean_and_validate(self):
        raw_text = self.text_input.get().strip()
        raw_key = self.key_input.get().strip()
        raw_shift = self.shift_input.get().strip()

        if not raw_text or not raw_key or not raw_shift:
            messagebox.showerror("Validation Error", "All entry fields must contain operational arguments.")
            return False

        if re.search(r"[<>{}\[\]\\^\`~|]", raw_text):
            messagebox.showwarning("Security Warning", "Unsafe characters detected and flagged inside message input field.")
            return False

        if not raw_key.isalpha():
            messagebox.showerror("Type Error", "The key field rejected non-alphabetic elements. Strip numbers/symbols.")
            return False

        try:
            shift_int = int(raw_shift)
            if not (1 <= shift_int <= 25):
                raise ValueError("Out of index range bound.")
        except ValueError:
            messagebox.showerror("Range Error", "Caesar Shift must represent an operational numerical value between 1 and 25.")
            return False

        return {"message": raw_text, "key": raw_key, "shift": shift_int}

    def process_validation(self):
        validated_data = self.clean_and_validate()
        if validated_data:
            self.write_log("✅ SYSTEM SANITY CHECK PASSED")
            self.write_log(f"-> Text Matrix: '{validated_data['message']}'")
            self.write_log(f"-> Verified Key: {validated_data['key']}")
            self.write_log(f"-> Verified Shift Range: {validated_data['shift']}")
            messagebox.showinfo("Success", "All interface constraints verified successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ValidationInterface(root)
    root.mainloop()
