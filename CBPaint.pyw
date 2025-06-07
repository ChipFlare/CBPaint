import tkinter as tk
from tkinter import filedialog, messagebox
import sys
try:
    import keyboard
    from tkinter import StringVar
    from PIL import Image, ImageTk, ImageEnhance
    import time
    import os
    import serial
    import numpy as np
    import serial.tools.list_ports
    import subprocess
    import pyautogui as pag
    import copy
    import winsound
    
except ModuleNotFoundError:
    messagebox.showinfo("ModuleNotFoundError", "Please install all the necessary modules first")
    subprocess.Popen(['notepad.exe', r'Libraries.txt'])
    sys.exit()

ports = serial.tools.list_ports.comports()
arduino_port = None

##Themes bg, fg, button, specia
Default_theme = ["#222222", "#ffffff", "#333333", "#ff0000"]
Light_mode = ["#ffffff", "#000000", "#eeeeee", "#ff0000"]
Windows_theme = ["#0078D7", "#ffffff", "#0078D7", "#0060aa"]
Red_theme = ["#770000", "#ffffff", "#990000", "#ff0000"]
Green_theme = ["#007700", "#ffffff", "#009900", "#008800"]

themes = [Default_theme,Light_mode, Windows_theme, Red_theme, Green_theme]
theme = 0

theme_names = ["Default", "Light mode" , "Windows 10", "Rust", "Eco"]

with open("theme.config", "r") as f:
    data=f.read()
    theme = int(data)

arduino_name = "Arduino"

with open("Arduino.config", "r") as f:
    arduino_name=f.read()

print(arduino_name)

auto_picked = 0

for port in ports:
    if arduino_name in port.description:
        arduino_port = port.device
        auto_picked = 1
        break


def helpme():
    os.startfile("help.docx")
    sys.exit()

def kill():
    sys.exit()


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

    tk.Button(root, text="Use without device", font=("Arial", 10), command=lambda p=None,d=port.description: pickPort(p, d), padx=50, fg=themes[theme][1], bg=themes[theme][2], width=50, bd =0, pady=5).pack(pady=1)
    tk.Button(root, text=" ? ", font=("Arial", 20), command=helpme, fg=themes[theme][1], bg=themes[theme][2], bd =0, pady=5).place(relx=1,rely=1, anchor="se")
    tk.Label(root, bg=themes[theme][0]).pack()
    root.protocol("WM_DELETE_WINDOW", kill)
    root.mainloop()


def save_arduino_name():
    arduino_name1=arduino_name[:-6]
    if arduino_port is not None:
        with open("Arduino.config", 'w') as file:
            file.write(arduino_name1)

wait = tk.Tk()
wait.title("Wait")
wait.iconbitmap("Huh.ico")
tk.Label(wait, text="Wait while the Aruduino is restarting...", font=("Arial", 12), bg=themes[theme][0], fg=themes[theme][1]).pack(pady=5, padx=40)
wait.config(bg=themes[theme][0])
wait.update() 
        
chunk_size = 32
baud_rate = 115200
try:
    print(arduino_port)
    ser = serial.Serial(arduino_port, baud_rate)
    if auto_picked == 0 and arduino_port is not None:
        save_arduino_name()
except serial.serialutil.SerialException:
    messagebox.showinfo("serial.serialutil.SerialException", "Can't make contact with the Arduino. Try closing the Arduino IDE or other instances of this app")
    sys.exit()

if arduino_port is not None:
    time.sleep(2)

wait.destroy()

WIDTH = 128
HEIGHT = 64
PIXEL_SIZE = 10
cursor = [0,0]

point1 = [0,0]
point2 = [0,0]
work_area = [0,0,128,64]
curpoint = 1
curpoint_s = 1

pixel_array = [[1 for _ in range(WIDTH)] for _ in range(HEIGHT)]
undo_stack = []
saved = True
save_path = None


def Saveport(com,desc):
    desc1 = desc[:-6]
    with open("Arduino.config", 'w') as file:
        file.write(desc1)
    result = messagebox.askyesno("Relaunch needed", "App needs to be relaunched for the effects to take place. Do you want to close now? if not, the port will be applied the next time you open the app")
    if result:
        subprocess.Popen([sys.executable] + sys.argv)
        sys.exit()

def change_port():
    ports = serial.tools.list_ports.comports()
    global arduino_name
    with open("Arduino.config", "r") as f:
        arduino_name=f.read()
    root = tk.Tk()
    root.title("Select Arduino")
    root.iconbitmap("Huh.ico")
    root.config(bg=themes[theme][0])
    tk.Label(root, text="Your current Arduino is '"+arduino_name+"'. Select the new one", font=("Arial", 14), bg=themes[theme][0], fg=themes[theme][1]).pack()
    
    for port in ports:
        tk.Button(root, text=port.description, font=("Arial", 10),command=lambda p=port.device,d=port.description: Saveport(p, d), padx=50, fg=themes[theme][1], bg=themes[theme][2], width=50, bd =0, pady=5).pack(pady=1)
    tk.Label(root, bg=themes[theme][0]).pack()
    root.mainloop()


def theme_write(themei):
    with open("theme.config", 'w') as file:
        file.write(str(themei))
    result = messagebox.askyesno("Relaunch needed", "App needs to be relaunched for the effects to take place. Do you want to close now? if not, the theme will be applied the next time you open the app")
    if result:
        subprocess.Popen([sys.executable] + sys.argv)
        sys.exit()

def set_theme():
    root = tk.Tk()
    root.title("Themes")
    root.iconbitmap("Huh.ico")
    root.config(bg=themes[theme][0])
    tk.Label(root, text="      Pick a theme      ", font=("Arial", 20), bg=themes[theme][0], fg=themes[theme][1]).pack(pady=5, padx=40)
    for i in range(len(theme_names)):
        tk.Button(root, text=theme_names[i], font=("Arial", 10),command=lambda p=i: theme_write(p), padx=50, fg=themes[i][1], bg=themes[i][2], width=50, bd =0, pady=5).pack(pady=1)

def wait_tho():
    if not saved:
        result = messagebox.askyesnocancel("Save?", "Save before closing?")
        if result is None:
            pass
        elif result:
            save_command()
        else:
            sys.exit()
    else:
        sys.exit()

def save_command(event=""):
    global save_path
    global saved
    saved = True
    final_save = ""
    print(pixel_array)
    for x in range(64):
        for y in range(128):
            final_save = final_save + str(pixel_array[x][y])
        final_save=final_save+"\n"
    if save_path == None:
        file_path = filedialog.asksaveasfilename(
        title="Save Crapbox File",
        defaultextension=".cbf",
        filetypes=[("CrapFile", "*.cbf")]
        )
        save_path = file_path
    else:
        file_path = save_path
    try:
        with open(file_path, 'w') as file:
            file.write(str(final_save))
            saved = True
            root.title(os.path.basename(save_path))
    except:
        messagebox.showinfo("No File Path", "Please choose a file path to save")

def save_as_command(event=""):
    global save_path
    save_path = None
    save_command()


def send():
    pixel_array1 = np.array(pixel_array, dtype=np.uint8)
    pixel_array1 = 255 - pixel_array1 * 255
    image = Image.fromarray(pixel_array1)
    if (arduino_port!=None):
        image = image.convert("1")
        byte_array = list(image.tobytes())
        num_chunks = len(byte_array) // chunk_size + (1 if len(byte_array) % chunk_size else 0)
        for i in range(num_chunks):
            start = i * chunk_size
            end = min(start + chunk_size, len(byte_array))
            chunk = byte_array[start:end]
            ser.write(chunk)

send()     
def open_command(event=""):
    global save_path

    make_new = True
    if not saved:
        result = messagebox.askyesnocancel("Save?", "Save before opening new file?")
        if result is None:
            make_new  = False
        elif result:
            save_command()

    if make_new:
        file_path = filedialog.askopenfilename(
        title="Save Crapbox File",
        defaultextension=".cbf",
        filetypes=[("CrapFile", "*.cbf")]
        )

        with open(file_path, 'r') as file:
            lines = file.readlines()

        try:
            for x in range(64):
                curline = list(lines[x])
                for y in range(128):
                    set_pixel_color(y, x, 1-int(curline[y]))
            save_path = file_path
        except IndexError:
            messagebox.showinfo("Something went wrong", "The file is either corrupt or unsupported")
        send()
        
        
    canvas.itemconfig(line, state='hidden')
    root.after(10, loop)

def mousepos(event):
    if curpoint == 2:
        if curtool.get() == "Rectangle tool" or curtool.get() == "Picture tool":
            canvas.coords(square, point1[0]*10+7, point1[1]*10+7, round((event.x-5)/10)*10+7, round((event.y-5)/10)*10+7)
        if curtool.get() == "Line tool":
            canvas.coords(line, point1[0]*10+7, point1[1]*10+7, round((event.x-5)/10)*10+7, round((event.y-5)/10)*10+7)
    if curpoint_s == 2:            
        if curtool.get() == "Selection tool":
            canvas.coords(selection, work_area[0]*10+2, work_area[1]*10+2, round((event.x-5)/10)*10+2, round((event.y-5)/10)*10+2)

def toggle_pixel(x, y):
    if x >= work_area[0] and x < work_area[2] and y >= work_area[1] and y < work_area[3]:
        pixel_array[y][x] = 1 - pixel_array[y][x]  
        color = "black" if pixel_array[y][x] else "white"
        canvas.itemconfig(grid[y][x], fill=color)

def set_pixel(x, y):
    if x >= work_area[0] and x < work_area[2] and y >= work_area[1] and y < work_area[3]:
        pixel_array[y][x] = 1 if keyboard.is_pressed('shift') else 0
        color = "black" if keyboard.is_pressed('shift') else "white"
        canvas.itemconfig(grid[y][x], fill=color)

def set_pixel_color(x, y, color):
    if x >= work_area[0] and x < work_area[2] and y >= work_area[1] and y < work_area[3]:
        pixel_array[y][x] = 1-color
        color = "black" if (color == 0) else "white"
        canvas.itemconfig(grid[y][x], fill=color)

def clear_display(event=""):
    global saved
    global save_path
    global work_area
    work_area[0] = 0
    work_area[1] = 0
    work_area[2] = 128
    work_area[3] = 64
    canvas.itemconfig(selection, state='hidden')
    make_new = True
    if not saved:
        result = messagebox.askyesnocancel("Save?", "Save before opening new file?")
        if result is None:
            make_new  = False
        elif result:
            save_command()

    if make_new:
        for x in range(128):
            for y in range(64):
                if pixel_array[y][x] ==0:
                    set_pixel_color(x, y, 0)
        saved = True
        save_path = None
        send()

def just_clear(event=""):
    global undo_array
    undo_array = copy.deepcopy(pixel_array)
    global saved
    global work_area
    canvas.itemconfig(selection, state='hidden')
    work_area[0] = 0
    work_area[1] = 0
    work_area[2] = 128
    work_area[3] = 64
    for x in range(128):
        for y in range(64):
            if pixel_array[y][x] ==0:
                set_pixel_color(x, y, 0)
    saved = False
    send()

def invert(event=""):
    global pixel_array
    global saved
    for x in range(128):
        for y in range(64):
            if pixel_array[y][x] ==0:
                set_pixel_color(x, y, 0)
            else:
                set_pixel_color(x, y, 1)
    saved = False
    send()
    
def drawrect():
    x1, y1 = min(point1[0], point2[0]), min(point1[1], point2[1])
    x2, y2 = max(point1[0], point2[0]), max(point1[1], point2[1])
    for i in range(x1, x2+1):
        set_pixel(i, y1)
        set_pixel(i, y2)
    for i in range(y1, y2+1):
        set_pixel(x1, i)
        set_pixel(x2, i)

def drawpic():
    x1, y1 = min(point1[0], point2[0]), min(point1[1], point2[1])
    x2, y2 = max(point1[0], point2[0]), max(point1[1], point2[1])
    height = y2-y1
    width = x2-x1

    if x1 == x2 and y1==y2:
        x1,y1=work_area[0], work_area[1]
        width, height=work_area[2]-work_area[0],work_area[3]-work_area[1]
    
    file_path = filedialog.askopenfilename(
        title="Select an Image File",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")]
    )
    try:
        image = Image.open(file_path)
        items += 1
    except:
        pass
    new_size = (width, height)
    image = image.convert("L")
    image = image.resize(new_size, Image.LANCZOS)
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    
    image = image.convert("1")

    for x in range (width):
        for y in range(height):
            pixel_array[y+y1][x+x1] = image.getpixel((x, y))
            pixel_array[y+y1][x+x1] = int(1 - pixel_array[y+y1][x+x1]/255)

    update()

def drawline():
    x1, y1 = point1
    x2, y2 = point2
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1 
    sy = 1 if y1 < y2 else -1
    err = dx - dy  
    while True:
        set_pixel(x1, y1)
        if x1 == x2 and y1 == y2:
            break 
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy

def flood_fill(x, y, target_value, fill_value):
    if pixel_array[y][x] != target_value:
        return
    stack = [(x, y)]

    while stack:
        cx, cy = stack.pop()
        if cx >= work_area[0] and cx < work_area[2] and cy >= work_area[1] and cy < work_area[3]:
            if pixel_array[cy][cx] == target_value:
                pixel_array[cy][cx] = fill_value
                if cx + 1 < 128:  
                    stack.append((cx + 1, cy))
                if cx - 1 >= 0:  
                    stack.append((cx - 1, cy))
                if cy + 1 < 64: 
                    stack.append((cx, cy + 1))
                if cy - 1 >= 0:  
                    stack.append((cx, cy - 1))

mouse_down = False
mbufaw = False
def loop():
    global mbufaw
    x = (canvas.winfo_pointerx()-canvas.winfo_rootx()-5)// PIXEL_SIZE
    y = (canvas.winfo_pointery()-canvas.winfo_rooty()-5)// PIXEL_SIZE
    cursor[0] = x
    cursor[1] = y

    color = "black" if keyboard.is_pressed('shift') else "white"
    label2.config(bg=color)
    
    if mouse_down:
        if curtool.get() == "Pen tool":
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                if not mbufaw:
                    point1[0] = x
                    point1[1] = y    
                point2[0] = x
                point2[1] = y
                drawline()
                mbufaw=True
                point1[0] = x
                point1[1] = y
    else:
        mbufaw=False
    root.after(10, loop)

def on_canvas_click(event):
    global saved 
    global undo_array
    undo_stack.append(copy.deepcopy(pixel_array))
    global mouse_down
    mouse_down = True
    global curpoint
    global curpoint_s
    saved = False
    if save_path is None:
        root.title("*Not saved")
    else:
        root.title("*"+os.path.basename(save_path))
    x = (event.x-5)// PIXEL_SIZE
    y = (event.y-5)// PIXEL_SIZE
    cursor[0] = x
    cursor[1] = y
    
    if curtool.get() == "Rectangle tool":
        canvas.tag_raise(square)
        if keyboard.is_pressed("shift"):
            canvas.itemconfig(square, outline='black', width = 9)
        else:
            canvas.itemconfig(square, outline='white', width = 9)
        point1[0] = x
        point1[1] = y
        set_pixel(x,y)
        curpoint = 2
        label.config(text = "Release to finish rectangle")
        canvas.itemconfig(square, state='normal')
        canvas.coords(square, point1[0]*10+7, point1[1]*10+7, event.x, event.y)
        
    if curtool.get() == "Line tool":
        canvas.tag_raise(line)
        if keyboard.is_pressed("shift"):
            canvas.itemconfig(line, fill='black')
        else:
            canvas.itemconfig(line, fill='white')
        point1[0] = x
        point1[1] = y
        set_pixel(x,y)
        canvas.itemconfig(line, state='normal')
        canvas.coords(line, point1[0]*10+7, point1[1]*10+7, event.x, event.y)
        curpoint = 2
        label.config(text = "Release to finish line")

    if curtool.get() == "Paint Bucket tool":
        if keyboard.is_pressed("shift"):
            flood_fill(x, y, 0, 1)
        else:
            flood_fill(x, y, 1, 0)
        update()

    if curtool.get() == "Picture tool":
        canvas.tag_raise(square)
        if keyboard.is_pressed("shift"):
            canvas.itemconfig(square, outline='black', width = 2)
        else:
            canvas.itemconfig(square, outline='white', width = 2)
        point1[0] = x
        point1[1] = y
        curpoint = 2
        canvas.itemconfig(square, state='normal')
        canvas.coords(square, point1[0]*10+7, point1[1]*10+7, event.x, event.y)
        label.config(text = "Release to set picture position")

    if curtool.get() == "Selection tool":
        canvas.tag_raise(selection)
        work_area[0]=x
        work_area[1]=y
        curpoint_s = 2
        canvas.itemconfig(selection, state='normal')
        canvas.coords(selection, work_area[0]*10+2, work_area[1]*10+2, event.x, event.y)
        
def update():
    for y in range (HEIGHT):
        for x in range(WIDTH):
            color = "black" if pixel_array[y][x] else "white"
            if canvas.itemcget(grid[y][x], "fill") != color:
                canvas.itemconfig(grid[y][x], fill=color)

def undo(event=""):
    global pixel_array
    if undo_stack:
        pixel_array = undo_stack.pop()
        update()
        send()
    else:
        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)


def mouse_up(event):
    global mouse_down
    global curpoint_s
    mouse_down = False

    x = (event.x-5)// PIXEL_SIZE
    y = (event.y-5)// PIXEL_SIZE
    cursor[0] = x
    cursor[1] = y
    
    if curtool.get() == "Rectangle tool":
            point2[0] = x
            point2[1] = y
            set_pixel(x,y)
            canvas.itemconfig(square, state='hidden')
            label.config(text = " ")
            drawrect()

    if curtool.get() == "Line tool":
            point2[0] = x
            point2[1] = y
            set_pixel(x,y)
            drawline()
            curpoint = 1
            canvas.itemconfig(line, state='hidden')
            label.config(text = " ")

    if curtool.get() == "Picture tool":
            point2[0] = x
            point2[1] = y
            curpoint = 1
            canvas.itemconfig(square, state='hidden')
            label.config(text = " ")
            drawpic()

    if curtool.get() == "Selection tool":
        work_area[2]=x
        work_area[3]=y
        curpoint_s = 1
        x1, y1 = min(work_area[0], work_area[2]), min(work_area[1], work_area[3])
        x2, y2 = max(work_area[0], work_area[2]), max(work_area[1], work_area[3])
        work_area[0] = x1
        work_area[1] = y1
        work_area[2] = x2
        work_area[3] = y2
        canvas.itemconfig(selection, state='normal')
        if work_area[0] == work_area[2] or work_area[1] == work_area[3]:
            canvas.itemconfig(selection, state='hidden')
            work_area[0] = 0
            work_area[1] = 0
            work_area[2] = 128
            work_area[3] = 64
        else:
            canvas.coords(selection, work_area[0]*10+2, work_area[1]*10+2, work_area[2]*10+2, work_area[3]*10+2)

    send()

def toolchange(value):
    for i in range(6):
        buttons[i].config(bg=themes[theme][2], fg=themes[theme][1])
    if value == "Rectangle tool":
        label.config(text = "Rectangle tool | Drag to create rectangles | hold Shift to make black rectangles")
        buttons[1].config(bg=themes[theme][1], fg=themes[theme][2])
    if value == "Pen tool":
        label.config(text = "Pen tool | Drag to draw in white | Shift+Drag to draw in black")
        buttons[0].config(bg=themes[theme][1], fg=themes[theme][2])
    if value == "Line tool":
        label.config(text = "Line tool | Drag to draw lines | Hold Shift to draw black lines")
        buttons[2].config(bg=themes[theme][1], fg=themes[theme][2])
    if value == "Paint Bucket tool":
        label.config(text = "Pant bucket tool | Click where you want to fill | Hold Shift to fill black")
        buttons[3].config(bg=themes[theme][1], fg=themes[theme][2])
    if value == "Picture tool":
        label.config(text = "Click to insert picture to selection | Drag to set picture position")
        buttons[4].config(bg=themes[theme][1], fg=themes[theme][2])
    if value == "Selection tool":
        label.config(text = "Drag to select | Click to select all")
        buttons[5].config(bg=themes[theme][1], fg=themes[theme][2])
    

def newtool(i):
    toolchange(i)
    curtool.set(i)

def about():
    root = tk.Tk()
    root.title("About")
    root.iconbitmap("Huh.ico")
    root.config(bg=themes[theme][0])
    tk.Label(root, text="Crapbox paint v1.0", font=("Impact", 20), bg=themes[theme][0], fg=themes[theme][1]).pack(pady=5, padx=40)
    tk.Label(root, text='''

Crapbox paint by ChipFlare Studios
Minusha Dulwan

''', font=("Arial", 10), bg=themes[theme][0], fg="#999999").pack(pady=5)
    tk.Label(root, text="Copyright ChipFlare Studios 2025", font=("Arial", 7), bg=themes[theme][0], fg=themes[theme][1]).pack()
    root.mainloop()
    
def launch_mirror():
    ser.close()
    root.destroy()
    subprocess.run(['python.exe', r'Screen_mirror.py'])
    sys.exit()

def do_nothing():
    pass

root = tk.Tk()
root.title("Crapbox Paint")
root.iconbitmap("icon.ico")
root.geometry("1400x675")
root.config(bg=themes[theme][0])
tools = ["Pen tool", "Rectangle tool", "Line tool", "Paint Bucket tool", "Picture tool", "Selection tool"]
buttons = []

#all the menubar stuff

menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="New                               Ctrl+N", command=clear_display)
file_menu.add_command(label="Open                             Ctrl+O", command=open_command)
file_menu.add_command(label="Save                               Ctrl+S", command=save_command)
file_menu.add_command(label="Save as                Ctrl+Shift+S", command=save_as_command)
file_menu.add_separator()
file_menu.add_command(label="Change Port", command=change_port)
file_menu.add_command(label="Themes", command=set_theme)

if arduino_port == None:
    file_menu.add_command(label="Mirror Screen (No Arduino)", command=launch_mirror, state='disabled')
else:
    file_menu.add_command(label="Mirror Screen", command=launch_mirror)
    
file_menu.add_separator()
file_menu.add_command(label="Quit                               Alt+F4", command=wait_tho)

tools_menu =  tk.Menu(menubar, tearoff=1)
for i in range(6):
    tools_menu.add_command(label=tools[i], command=lambda me=i: newtool(tools[me]))
tools_menu.add_separator()
tools_menu.add_command(label="Clear                        C", command=just_clear)
tools_menu.add_command(label="Invert                        I", command=invert)

help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="Help Document", command=helpme)
help_menu.add_separator()
help_menu.add_command(label="About CBPaint", command=about)

edit_menu = tk.Menu(menubar, tearoff=0)
edit_menu.add_command(label="Undo                      Ctrl+Z", command=undo)
edit_menu.add_separator()
edit_menu.add_command(label="Clear                               C", command=just_clear)
edit_menu.add_command(label="Invert                               I", command=invert)

menubar.add_cascade(label="File", menu=file_menu)
menubar.add_cascade(label="Edit", menu=edit_menu)
menubar.add_cascade(label="Tools", menu=tools_menu)
menubar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menubar)
#They end here

canvas = tk.Canvas(root, width=WIDTH * PIXEL_SIZE, height=HEIGHT * PIXEL_SIZE, bg="white")
canvas.place(x=0,y=0)

square = canvas.create_rectangle(50, 50, 150, 150, outline="#ffffff", width = 9)
line = canvas.create_line(50, 50, 150, 150, fill="#ffffff", width = 9)
selection = canvas.create_rectangle(50, 50, 150, 150, outline="#ff5500", width = 2)

curtool = StringVar()
curtool.set("Pen tool")

for i in range(6):
    btn = tk.Button(text=tools[i], command=lambda me=i: newtool(tools[me]), width=15,bg=themes[theme][2], fg=themes[theme][1], borderwidth =0)
    btn.place(relx=1, y=i*25+5, anchor="ne")
    buttons.append(btn)
tk.Button(root, text="Clear", command=just_clear, bg=themes[theme][3], fg=themes[theme][1], width = 15, borderwidth =0).place(relx=1,y=175, anchor="ne")
buttons[0].config(bg=themes[theme][1], fg=themes[theme][2])

if arduino_port == None:
    tk.Button(root, text="Mirror screen", command=launch_mirror, bg=themes[theme][2], fg=themes[theme][1], width = 15, borderwidth =0, state='disabled').place(relx=1,y=200, anchor="ne")
else:
    tk.Button(root, text="Mirror screen", command=launch_mirror, bg=themes[theme][3], fg=themes[theme][1], width = 15, borderwidth =0).place(relx=1,y=200, anchor="ne")

label = tk.Label(root, text="Pen tool | Drag to draw in white | Shift+Drag to draw in black", font=("Arial", 14), bg=themes[theme][0], fg=themes[theme][1])
label.place(relx=0.5, rely=1, anchor = "s")
label2 = tk.Label(root, text="", font=("Arial", 14), bg=themes[theme][0], fg=themes[theme][1], width=7, height=2)
label2.place(relx=0.99, y=640, anchor = "se")


grid = [[None for _ in range(WIDTH)] for _ in range(HEIGHT)]
for y in range(HEIGHT):
    for x in range(WIDTH):
        rect = canvas.create_rectangle(
            x * PIXEL_SIZE + 2,
            y * PIXEL_SIZE + 2,
            (x + 1) * PIXEL_SIZE + 2,
            (y + 1) * PIXEL_SIZE + 2,
            fill="white",
            outline="#333333",
        )
        grid[y][x] = rect

canvas.bind("<ButtonPress-1>", on_canvas_click)
canvas.bind("<ButtonRelease-1>", mouse_up)
canvas.bind("<Motion>", mousepos)
root.bind_all("<Control-z>", undo)
root.bind_all("<Control-s>", save_command)
root.bind_all("<Control-o>", open_command)
root.bind_all("<Control-n>", clear_display)
root.bind_all("<Control-Shift-s>", save_as_command)
root.bind_all("<i>", invert)
root.bind_all("<c>", just_clear)
root.protocol("WM_DELETE_WINDOW", wait_tho)
root.wm_resizable(width=False, height=False)
loop()
update()
send()

root.mainloop()
