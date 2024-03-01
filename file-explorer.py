import tkinter as tk
from tkinter import filedialog, Entry, Menu, Toplevel
import tkinter.font as TkFont
import os
from os import path

config_dir = path.expandvars(r'%LOCALAPPDATA%')

data = ''
config = []
folder_selected = ''

def read_config():
    config = open(config_dir+'config.cfg','r')
    path = config.readline().strip()    
    config.close()
    if path == '':
        return False
    else:
        return path

def about():
    settingsWindow = Toplevel(root)
    settingsWindow.title('About')
    settingsWindow.geometry('400x400')
    root.eval(f'tk::PlaceWindow {str(settingsWindow)} center')

def save_config():
    global folder_selected
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        file = open(config_dir+'config.cfg','w')
        file.write(folder_selected + '\n')
        file.close()

def browse_folder():
    path = filedialog.askdirectory()
    if path:
        folder_contents.delete(0, tk.END)
        for root, dirs, files in os.walk(path,onerror=None):           
            for name in files:
                folder_contents.insert(tk.END, os.path.join(root, name))
        global data
        data = folder_contents.get(0,tk.END)

def save_data():
    files = [('Text Document', '*.txt'),('All Files', '*.*')]
    path = read_config()    
    if path:
        file_path = filedialog.asksaveasfile(initialdir=path,filetypes=files,defaultextension=files)
    else:
        print("no config")
        file_path = filedialog.asksaveasfile(filetypes=files,defaultextension=files)
    if file_path:    
        file_path.write("\n".join(folder_contents.get(0, tk.END)))
        file_path.write('\n')
        file_path.close()

def open_data():
    path = read_config()
    if path:
        file_path = filedialog.askopenfilename(initialdir=path)
    else:
        file_path = filedialog.askopenfilename()
    if file_path:
        folder_contents.delete(0, tk.END)        
        with open(file_path, 'r') as file:
            lines = file.read().split("\n")
            for line in lines:
                folder_contents.insert(tk.END, line)
        global data
        data = folder_contents.get(0,tk.END)

def search_string(event):
    typed = search.get()
    if typed == '':
        filtered_data = data
    else:
        filtered_data = []
        for item in data:
            if typed.lower() in item.lower():
                filtered_data.append(item)
    update(filtered_data)

def update(data):
    folder_contents.delete(0, tk.END)
    for item in data:
        folder_contents.insert(tk.END, item)

root = tk.Tk()
root.geometry("700x500")
root.title("File Explorer")
root.iconbitmap("icon.ico")

bf = TkFont.Font(family='Helvetica', size=12, weight='bold')
lf = TkFont.Font(family='Helvetica', size=13, weight='normal')
df = TkFont.Font(family='Helvetica', size=11, weight='normal')

menubar = Menu(root)
filemenu = Menu(menubar,tearoff=0,font=df)
filemenu.add_command(label="Settings",command=save_config)
filemenu.add_command(label="About",command=about)

filemenu.add_separator()

filemenu.add_command(label="Exit",command=root.quit)
menubar.add_cascade(label="File",menu=filemenu)

buttons = tk.Frame(root)
srch = tk.Frame(root)
content = tk.Frame(root)

browse_button = tk.Button(buttons, text="Browse Folder", command=browse_folder, padx=20,pady=5,font=bf)
browse_button.pack(side=tk.LEFT, pady=5)

save_button = tk.Button(buttons, text="Save", command=save_data, padx=20,pady=5,font=bf)
save_button.pack(side=tk.LEFT, pady=5)

open_button = tk.Button(buttons, text="Open", command=open_data, padx=20,pady=5,font=bf)
open_button.pack(side=tk.RIGHT, pady=5)

search = Entry(srch,width=60,font=lf)
search.pack(side=tk.LEFT,pady=10)
search.bind('<KeyRelease>',search_string)

folder_contents = tk.Listbox(content, selectmode=tk.SINGLE,width=200,font=lf)
folder_contents.pack(fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(folder_contents, orient=tk.VERTICAL)
scrollbar.config(command=folder_contents.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
folder_contents.config(yscrollcommand=scrollbar.set)

buttons.pack(padx=10,pady=0,fill=tk.BOTH)
content.pack(padx=10,pady=0,fill=tk.BOTH, expand=True)
srch.pack(padx=10,pady=0,fill=tk.BOTH)

root.config(menu=menubar)

root.mainloop()
