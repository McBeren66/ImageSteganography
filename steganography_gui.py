import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image


def message_to_bits(message):
    """
    Convert a text message into a string of bits. The first 32 bits store the length of the message in characters.  
    Each character is represented by eight bits.  
    """
    length = len(message)
    length_bits = format(length, '032b')
    message_bits = ''.join([format(ord(c), '08b') for c in message])
    return length_bits + message_bits


def bits_to_message(bits):
    """
    Convert a string of bits back into the original text message.  
    The first 32 bits indicate how many characters the message contains.  
    """
    length = int(bits[:32], 2)
    message_bits = bits[32:32 + length * 8]
    chars = [chr(int(message_bits[i:i+8], 2)) for i in range(0, len(message_bits), 8)]
    return ''.join(chars)


def hide_message_in_image(image_path, message, output_path):
    """
    Embed a secret message into an image using the least significant bit technique.  
    Each pixel has three colour channels, and we modify the least significant bit of each channel to store message bits.  
    The function writes the modified image to the specified output path.  
    """
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    width, height = img.size
    pixels = img.load()

    bitstring = message_to_bits(message)
    total_bits = len(bitstring)

    if total_bits > width * height * 3:
        raise ValueError("The message is too long for the selected image.")

    bit_index = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            new_colors = []
            for colour in (r, g, b):
                if bit_index < total_bits:
                    bit = int(bitstring[bit_index])
                    new_colour = (colour & ~1) | bit
                    bit_index += 1
                else:
                    new_colour = colour
                new_colors.append(new_colour)
            pixels[x, y] = tuple(new_colors)
            if bit_index >= total_bits:
                break
        if bit_index >= total_bits:
            break
    img.save(output_path)


def extract_message_from_image(image_path):
    """
    Retrieve a hidden message from an image by reading the least significant bits of its pixels.  
    The function reads the first 32 bits to determine the message length and then reads the corresponding number of bits to reconstruct the message.  
    """
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    width, height = img.size
    pixels = img.load()
    bits = ''
    message_length = None
    for y in range(height):
        for x in range(width):
            for colour in pixels[x, y]:
                bits += str(colour & 1)
                if message_length is None and len(bits) == 32:
                    message_length = int(bits, 2)
                if message_length is not None:
                    total_needed = 32 + message_length * 8
                    if len(bits) >= total_needed:
                        relevant_bits = bits[:total_needed]
                        return bits_to_message(relevant_bits)
    return ""


class SteganographyApp(tk.Tk):
    """
    The main application class that sets up the graphical interface with two tabs: one for hiding messages and one for extracting messages.  
    """
    def __init__(self):
        super().__init__()
        self.title("Image Steganography")
        self.geometry("600x400")
        notebook = ttk.Notebook(self)
        self.hide_tab = ttk.Frame(notebook)
        self.extract_tab = ttk.Frame(notebook)
        notebook.add(self.hide_tab, text="Hide")
        notebook.add(self.extract_tab, text="Extract")
        notebook.pack(expand=1, fill="both")
        self._create_hide_tab()
        self._create_extract_tab()
        self.hide_image_path = None
        self.extract_image_path = None

    def _create_hide_tab(self):
        load_button = ttk.Button(self.hide_tab, text="Load Image", command=self.load_hide_image)
        load_button.pack(pady=10)
        self.message_text = tk.Text(self.hide_tab, height=10)
        self.message_text.pack(padx=10, pady=10, fill="both", expand=True)
        save_button = ttk.Button(self.hide_tab, text="Save", command=self.save_hidden_image)
        save_button.pack(pady=10)

    def _create_extract_tab(self):
        load_button = ttk.Button(self.extract_tab, text="Load Image", command=self.load_extract_image)
        load_button.pack(pady=10)
        self.extract_result = tk.StringVar()
        result_label = ttk.Label(self.extract_tab, textvariable=self.extract_result, wraplength=500)
        result_label.pack(padx=10, pady=10, fill="both", expand=True)
        decrypt_button = ttk.Button(self.extract_tab, text="Decrypt", command=self.decrypt_message)
        decrypt_button.pack(pady=10)

    def load_hide_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
        if path:
            self.hide_image_path = path

    def save_hidden_image(self):
        if not self.hide_image_path:
            messagebox.showerror("Error", "Please load an image first.")
            return
        message = self.message_text.get("1.0", tk.END).rstrip("\n")
        if not message:
            messagebox.showerror("Error", "Please enter a message to hide.")
            return
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        if output_path:
            try:
                hide_message_in_image(self.hide_image_path, message, output_path)
                messagebox.showinfo("Success", "Message hidden and image saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def load_extract_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
        if path:
            self.extract_image_path = path

    def decrypt_message(self):
        if not self.extract_image_path:
            messagebox.showerror("Error", "Please load an image first.")
            return
        message = extract_message_from_image(self.extract_image_path)
        if message:
            self.extract_result.set(message)
        else:
            self.extract_result.set("No hidden message found.")


if __name__ == "__main__":
    app = SteganographyApp()
    app.mainloop()
