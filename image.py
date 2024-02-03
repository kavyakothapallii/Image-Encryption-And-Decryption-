import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import tkinter as tk
from tkinter import filedialog, messagebox

class ImageProcessingTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing Tool")
        self.root.geometry("400x200")
        self.root.configure(bg="#F2E7FE") 
        self.root.resizable(False, False) 
        self.key = b'Sixteen byte key'
        self.image_path = None
        self.image_label = tk.Label(root, text="No image selected", bg="#F2E7FE", font=("Arial", 10))
        self.image_label.pack(pady=10)
        self.select_button = tk.Button(root, text="Select Image", command=self.choose_image, bg="#E7E7E7", font=("Arial", 10))
        self.select_button.pack(pady=10)
        self.process_button = tk.Button(root, text="Encrypt/Decrypt Image", command=self.process_image, bg="#5E5E5E", fg="#F2E7FE", font=("Arial", 10))
        self.process_button.pack(pady=10)

    def choose_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.enc")])
        if self.image_path:
            self.image_label.config(text=f"Selected image: {os.path.basename(self.image_path)}")

    def process_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image to process first.")
            return
        with open(self.image_path, 'rb') as f:
            file_data = f.read()
        if self.image_path.endswith(".enc"):
            iv = file_data[:16]
            ciphertext = file_data[16:]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            try:
                processed_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
            except ValueError as e:
                messagebox.showerror("Error", f"Failed to decrypt image: {e}")
                return
        else:
            cipher = AES.new(self.key, AES.MODE_CBC)
            processed_data = cipher.iv + cipher.encrypt(pad(file_data, AES.block_size))
        output_extension = "enc" if not self.image_path.endswith(".enc") else "png"
        output_path = filedialog.asksaveasfilename(defaultextension=f".{output_extension}", filetypes=[("Image files", f"*.{output_extension}")])
        if output_path:
            with open(output_path, 'wb') as f:
                f.write(processed_data)
            messagebox.showinfo("Success", "Image processed and saved successfully.")
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingTool(root)
    root.mainloop()

