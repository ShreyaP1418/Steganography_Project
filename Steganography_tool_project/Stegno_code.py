import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

# -------- Helper Functions --------
def encode_msg(img_path, message, password, out_name):
    img = Image.open(img_path)
    # Add a special END marker to detect end of message
    secret = password + "::" + message + "%%END%%"
    binary = ''.join(format(ord(c), '08b') for c in secret)

    pixels = list(img.getdata())
    new_pixels = []
    bin_index = 0

    for pixel in pixels:
        r, g, b = pixel[:3]
        if bin_index < len(binary):
            r = (r & ~1) | int(binary[bin_index]); bin_index += 1
        if bin_index < len(binary):
            g = (g & ~1) | int(binary[bin_index]); bin_index += 1
        if bin_index < len(binary):
            b = (b & ~1) | int(binary[bin_index]); bin_index += 1
        new_pixels.append((r, g, b))

    img.putdata(new_pixels)
    img.save(out_name)
    return True

def decode_msg(img_path, password):
    img = Image.open(img_path)
    pixels = list(img.getdata())

    binary = ""
    for r, g, b in pixels:
        binary += str(r & 1)
        binary += str(g & 1)
        binary += str(b & 1)

    # Convert binary back to characters
    data = ""
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) < 8:
            break
        data += chr(int(byte, 2))
        if "%%END%%" in data:
            break

    # Split password and message
    try:
        passw, rest = data.split("::", 1)
        if passw == password:
            return rest.replace("%%END%%", "")
        else:
            return "❌ Wrong password!"
    except:
        return "❌ No hidden message found!"

# -------- GUI --------
root = tk.Tk()
root.title("Steganography Tool")
root.geometry("400x400")

# ----- Encode -----
def open_encode():
    def select_img():
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg")])
        entry_img.delete(0, tk.END)
        entry_img.insert(0, path)

    def encode_action():
        img = entry_img.get()
        msg = entry_msg.get()
        pwd = entry_pwd.get()
        out = entry_out.get()
        if not all([img, msg, pwd, out]):
            messagebox.showerror("Error", "All fields are required!")
            return
        encode_msg(img, msg, pwd, out)
        messagebox.showinfo("Success", f"Message hidden in {out}")

    win = tk.Toplevel(root)
    win.title("Encode")
    tk.Label(win, text="Image Path").pack()
    entry_img = tk.Entry(win, width=40); entry_img.pack()
    tk.Button(win, text="Browse", command=select_img).pack()
    tk.Label(win, text="Secret Message").pack()
    entry_msg = tk.Entry(win, width=40); entry_msg.pack()
    tk.Label(win, text="Password").pack()
    entry_pwd = tk.Entry(win, show="*", width=40); entry_pwd.pack()
    tk.Label(win, text="Output Image Name(with .png extension)").pack()
    entry_out = tk.Entry(win, width=40); entry_out.pack()
    tk.Button(win, text="Encode", command=encode_action).pack(pady=5)

# ----- Decode -----
def open_decode():
    def select_img():
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg")])
        entry_img.delete(0, tk.END)
        entry_img.insert(0, path)

    def decode_action():
        img = entry_img.get()
        pwd = entry_pwd.get()
        if not all([img, pwd]):
            messagebox.showerror("Error", "All fields are required!")
            return
        msg = decode_msg(img, pwd)
        messagebox.showinfo("Hidden Message", msg)

    win = tk.Toplevel(root)
    win.title("Decode")
    tk.Label(win, text="Image Path").pack()
    entry_img = tk.Entry(win, width=40); entry_img.pack()
    tk.Button(win, text="Browse", command=select_img).pack()
    tk.Label(win, text="Password").pack()
    entry_pwd = tk.Entry(win, show="*", width=40); entry_pwd.pack()
    tk.Button(win, text="Decode", command=decode_action).pack(pady=5)

# ----- Main Buttons -----
tk.Button(root, text="Encode", width=20, command=open_encode).pack(pady=20)
tk.Button(root, text="Decode", width=20, command=open_decode).pack(pady=20)

root.mainloop()