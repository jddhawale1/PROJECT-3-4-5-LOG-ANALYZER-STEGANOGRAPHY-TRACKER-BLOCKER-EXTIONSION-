from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image

# Convert message to binary
def msg_to_bin(msg):
    return ''.join(format(ord(i), '08b') for i in msg)

# ---------------- ENCODE ----------------
def encode_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png;*.bmp")]
    )
    if not file_path:
        return

    try:
        img = Image.open(file_path).convert("RGB")
    except:
        messagebox.showerror("Error", "Invalid image")
        return

    msg = text_entry.get("1.0", END).strip()

    if not msg:
        messagebox.showerror("Error", "Enter message")
        return

    msg += "###"  # delimiter
    binary_msg = msg_to_bin(msg)

    width, height = img.size
    data_index = 0

    for y in range(height):
        for x in range(width):
            pixel = list(img.getpixel((x, y)))

            for i in range(min(3, len(pixel))):
                if data_index < len(binary_msg):
                    bit = int(binary_msg[data_index])
                    pixel[i] = (pixel[i] & 254) | bit
                    data_index += 1

            img.putpixel((x, y), tuple(pixel))

            if data_index >= len(binary_msg):
                break
        if data_index >= len(binary_msg):
            break

    if data_index < len(binary_msg):
        messagebox.showerror("Error", "Message too large for image")
        return

    # 🔥 FIXED SAVE DIALOG
    save_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("BMP files", "*.bmp")]
    )

    if save_path:
        img.save(save_path)
        messagebox.showinfo("Success", "Message hidden successfully!")

# ---------------- DECODE ----------------
def decode_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.png;*.bmp")]
    )
    if not file_path:
        return

    try:
        img = Image.open(file_path).convert("RGB")
    except:
        messagebox.showerror("Error", "Invalid image")
        return

    binary_data = ""
    decoded_msg = ""

    width, height = img.size

    try:
        for y in range(height):
            for x in range(width):
                pixel = img.getpixel((x, y))

                for i in range(3):
                    binary_data += str(pixel[i] & 1)

                    if len(binary_data) >= 8:
                        byte = binary_data[:8]
                        binary_data = binary_data[8:]

                        if len(byte) < 8:
                            continue

                        try:
                            char = chr(int(byte, 2))
                        except:
                            continue

                        decoded_msg += char

                        if decoded_msg.endswith("###"):
                            result.delete("1.0", END)
                            result.insert(END, decoded_msg[:-3])
                            return

        result.delete("1.0", END)
        result.insert(END, "No hidden message found")

    except:
        messagebox.showerror("Error", "Decoding failed")

# ---------------- GUI ----------------
root = Tk()
root.title("Steganography Tool (Final Fixed)")
root.geometry("500x420")
root.configure(bg="#1e1e1e")

Label(root, text="Enter Secret Message", fg="white", bg="#1e1e1e").pack(pady=5)

text_entry = Text(root, height=5, width=50)
text_entry.pack()

Button(root, text="Hide Message", command=encode_image,
       bg="#007acc", fg="white").pack(pady=10)

Button(root, text="Extract Message", command=decode_image,
       bg="#007acc", fg="white").pack(pady=5)

Label(root, text="Extracted Message", fg="white", bg="#1e1e1e").pack(pady=5)

result = Text(root, height=5, width=50)
result.pack()

root.mainloop()