
import time
import keyboard
import os
import serial.tools.list_ports
from PIL import Image, ImageEnhance, ImageDraw
import pyautogui
import serial
import tkinter as tk
import sys

##Themes bg, fg, button, specia
Default_theme = ["#222222", "#ffffff", "#333333", "#ff0000"]
Windows_theme = ["#0078D7", "#ffffff", "#0078D7", "#0060aa"]
Red_theme = ["#770000", "#ffffff", "#990000", "#ff0000"]
Green_theme = ["#007700", "#ffffff", "#009900", "#008800"]

themes = [Default_theme, Windows_theme, Red_theme, Green_theme]
theme = 0

theme_names = ["Default", "Windows 10", "Rust", "Eco"]

ports = serial.tools.list_ports.comports()
arduino_name = "Arduino"

with open("Arduino.config", "r") as f:
    arduino_name=f.read()
    
arduino_port = None
for port in ports:
    if arduino_name in port.description:
        arduino_port = port.device
        break

def pickPort(thing, desc):
    global arduino_port
    global arduino_name
    arduino_port = thing
    arduino_name = desc
    root.destroy()

if arduino_port is None:
    root = tk.Tk()
    root.title("Can't detect Arduino")
    root.iconbitmap("Huh.ico")
    root.config(bg=themes[theme][0])
    tk.Label(root, text='''
Can't detect your Arduino Connected to this PC
      Please manually select the correct port for your Arduino if it is connected      
      ''', font=("Arial", 14), bg=themes[theme][0], fg=themes[theme][1]).pack()
    
    for port in ports:
        tk.Button(root, text=port.description, font=("Arial", 10),command=lambda p=port.device,d=port.description: pickPort(p, d), padx=50, fg=themes[theme][1], bg=themes[theme][2], width=50, bd =0, pady=5).pack(pady=1)

    tk.Label(root, bg=themes[theme][0]).pack()
    root.mainloop()

if arduino_port is None:
    sys.exit()

chunk_size = 32
baud_rate = 115200
try:
    print(arduino_port)
    ser = serial.Serial(arduino_port, baud_rate)
except serial.serialutil.SerialException:
    messagebox.showinfo("serial.serialutil.SerialException", "Can't make contact with the Arduino. Try closing the Arduino IDE or other instances of this app")
    sys.exit()
    
time.sleep(2) 
print('''
Screen mirror is running.
Close this window to stop''')
def send_loop():
    while True:
        try:
            screenshot = pyautogui.screenshot()
            image = screenshot.convert("L")
            image = image.resize((128, 64), Image.LANCZOS)
            resized_size = (128, 64)
            screen_width, screen_height = screenshot.size
            cursor_x, cursor_y = pyautogui.position()

            scale_x = resized_size[0] / screen_width
            scale_y = resized_size[1] / screen_height
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            resized_x = int(cursor_x * scale_x)
            resized_y = int(cursor_y * scale_y)
            cursor_size = 3

# Invert pixels along the horizontal and vertical lines of the cross
            for dx in range(-cursor_size, cursor_size + 1):
                x = resized_x + dx
                y = resized_y
                if 0 <= x < image.width and 0 <= y < image.height:
                    pixel = image.getpixel((x, y))
                    image.putpixel((x, y), 255 - pixel)

            for dy in range(-cursor_size, cursor_size + 1):
                x = resized_x
                y = resized_y + dy
                if 0 <= x < image.width and 0 <= y < image.height:
                    pixel = image.getpixel((x, y))
                    image.putpixel((x, y), 255 - pixel)
            image = image.convert("1")

            byte_array = list(image.tobytes())
            chunk_size = 32
            num_chunks = len(byte_array) // chunk_size + (1 if len(byte_array) % chunk_size else 0)

            for i in range(num_chunks):
                start = i * chunk_size
                end = min(start + chunk_size, len(byte_array))
                chunk = byte_array[start:end]
                ser.write(chunk)
        except Exception as e:
            print(f"Error during sending: {e}")
            break

send_loop()

