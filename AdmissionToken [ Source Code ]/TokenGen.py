from queue import Queue
from tkinter import *
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import pickle
import datetime
import pyttsx3
import csv
import os
import sms
from sms_module import *
import ctypes


engine = pyttsx3.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)
engine.setProperty('language', 'en-in')
engine.setProperty('gender', 'female')
engine.setProperty('volume', 1)
engine.setProperty('age', 'adult')
engine.setProperty('rate', 178)

def speak(Text):
    #print("    ")
    engine.say(text=Text)
    engine.runAndWait()
    #print("     ")


count = 0
item = ""
is_queue_running = False
first = True
row = 1
root = tk.Tk()
root.geometry("1650x850")
root.title("      \u2022ADMISSION MANAGEMENT SYSTEM\u2022  Token Generator")

# Set the icon for the window (replace 'icon.ico' with your icon's file path)
root.iconbitmap('icon.ico')

#root.resizable(False, False)

frame1 = Frame(root, highlightbackground="black", highlightthickness=3,width=1580, height=790, bd= 0)
frame1.place(x=33, y=26)

# Create a nested frame inside frame1
nested_frame = tk.Frame(frame1, bg='#BBC0D3')
nested_frame.place(x=10, y=10, width=670, height=762)


# Create a nested frame inside frame2
nested_frame2 = tk.Frame(frame1, bg='#353536')
nested_frame2.place(x=690, y=10, width=870, height=762)

class QueueManager:
    global count
    def __init__(self):
        self.token_number = 0
        self.queue = []
        self.waiting = []
        self.tokens = " "
        self.total_count = 0
        

    def get_next_token(self):
        self.token_number += 1
        self.total_count += 1
        self.queue.append(self.token_number)
        global count
        count += 1

    def dequeue_token(self):
        if len(self.queue) > 0:
            global count
            count -= 1
            return self.queue.pop(0)
        else:
            return None
        

queue_manager = QueueManager()

def save_state():
    with open("state.pickle", "wb") as f:
        saved_state = {
            "count": count,
            "row": row,
            "tokens": queue_manager.tokens,
            "token_number": queue_manager.token_number,
            "queue": queue_manager.queue,
            "waiting": queue_manager.waiting,
            
        }
        pickle.dump(saved_state, f)
    # print(row)

# Load saved state if available
try:
    with open("state.pickle", "rb") as f:
        saved_state = pickle.load(f)
        count = saved_state["count"]
        row = saved_state.get("row", 1)
        queue_manager.tokens = saved_state.get("tokens", 0)
        queue_manager.token_number = saved_state.get("token_number", 0)
        queue_manager.queue = saved_state.get("queue", 0)
        queue_manager.waiting = saved_state.get("waiting", 0)
        
except FileNotFoundError:
    # No saved state found
    pass


def close_window():
    save_state()
    root.destroy()

# Save state when window is closed
root.protocol("WM_DELETE_WINDOW", close_window)

##################################  Newly Added Code  #########################################
def open_window():
    window = tk.Toplevel(root)
    window.title("Student Detail for Token Generation")
    window.geometry("450x250")
    window.attributes('-topmost', True)
    frame2 = Frame(window, highlightbackground="black", highlightthickness=3,width=400, height=200, bd= 0)
    frame2.place(x=25, y=15)
    nested_frame1 = tk.Frame(frame2, bg='#BBC0D3')
    nested_frame1.place(x=10, y=10, width=370, height=175)


    tk.Label(window, text="Name:", bg="#BBC0D3").place(x=75, y=50)
    entry_name = tk.Entry(window)
    entry_name.place(x=150, y=50)
    
    tk.Label(window, text="Phone No.:", bg="#BBC0D3").place(x=75, y=90)
    entry_phone = tk.Entry(window)
    entry_phone.place(x=150, y=90)
    
    btn_generate = tk.Button(window, text="Generate", command=lambda: generate_data(entry_name, entry_phone))
    btn_generate.place(x=180, y=150)

def generate_data(entry_name, entry_phone):
    name = entry_name.get()
    phone = entry_phone.get()
    phone = '+91'+ phone
    #print(phone)
    
    if name and phone:
        generate_token()
        data = [str(queue_manager.token_number), name, phone]
        file_exists = os.path.exists("token_data.csv")
        with open("token_data.csv", "a", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            if not file_exists:
                csv_writer.writerow(["Token", "Name", "Phone"])  # Write header if the file is newly created
            csv_writer.writerow(data)
        
        #SMS send module function call 
        #sms.send_sms(message=f"Your Token No. is {data[0]}. Please wait until we remind you! ", recipient=phone)
            
        entry_name.delete(0, tk.END)
        entry_phone.delete(0, tk.END)
        tk.messagebox.showinfo(f"Token No. {data[0]} Generated Successfully!", "Data saved Succesfully")
    else:
        tk.messagebox.showerror("Error", "Please enter Name and Phone No.")

############################################################################################################

token_count = tk.Label(root,text = " ", font=("Arial", 17), bg="#353536",fg="white", width=40,height=1)
token_count.place(x=100,y=100)
token_count.config(text=f"REMAINING NUMBER OF TOKENS: {count}")

def generate_token():
    queue_manager.get_next_token()
    token_count.config(text=f"REMAINING NUMBER OF TOKENS: {count}")
    #print(count)
    tokens = " "
    for i in queue_manager.queue:
        if tokens == " ":
            tokens = tokens + str(i)
        else:
            tokens = tokens + ", " + str(i)
    generated_tokens.delete("0",tk.END)
    generated_tokens.insert(tk.END,f"{tokens}")
    queue_manager.tokens = tokens


def start_screen():
    global is_queue_running
    is_queue_running = True
    global first
    tokens = " "
    if len(queue_manager.queue) > 0 and first:
        global item
        first = False
        item = queue_manager.dequeue_token()
        #print(item)
        screen.config(text=f"{item}")
        speak(f"Token Number {item}")
        token_count.config(text=f"REMAINING NUMBER OF TOKENS: {count}")
        for i in queue_manager.queue:
            if tokens == " ":
                tokens = tokens +str(i)
            else:
                tokens = tokens + ", " + str(i)
        generated_tokens.delete("0",tk.END)
        generated_tokens.insert(tk.END,f"{tokens}")
        queue_manager.tokens = tokens
        send_message(item)      ##Send Message SMS

def next_token_screen():
    if is_queue_running:
        global item
        tokens = " "
        item = queue_manager.dequeue_token()
        #print(item)
        if item == None:
            to_queue()
        else:
            screen.config(text=f"{item}")
            speak(f"Token Number {item}")
        token_count.config(text=f"REMAINING NUMBER OF TOKENS: {count}")
        for i in queue_manager.queue:
            if tokens == " ":
                tokens = tokens +str(i)
            else:
                tokens = tokens + ", " + str(i)
        generated_tokens.delete("0",tk.END)
        generated_tokens.insert(tk.END,f"{tokens}")
        queue_manager.tokens = tokens
        send_message(item)      ##Send Message SMS


def to_queue():
    global count
    global item
    count_queue = 0
    queue_manager.queue.clear()
    for i in range(waiting_list.size()):
        
        count_queue = count_queue + 1
        queue_manager.queue.append(waiting_list.get(i))
        #print(to_queue)
        #print(count_queue)
        #print(queue_manager.queue)
    queue_manager.waiting = []
    waiting_list.delete(0,tk.END)
    count = count_queue
    item = queue_manager.dequeue_token()
    screen.config(text=f"{item}")
    speak(f"Token Number {item}")
    send_message(item)      ##Send Message SMS

    
        
def stop_screen():
    global is_queue_running
    global first
    first = True
    is_queue_running = False

def add_to_wait():
    global is_queue_running
    global item
    tokens = " "
    if is_queue_running:
        queue_manager.waiting.append(item)
        #print(queue_manager.waiting)
        waiting_list.insert(END,item)
        item = queue_manager.dequeue_token()
        if item == None:
            to_queue()
        else:
            screen.config(text=f"{item}")
            speak(f"Token Number {item}")
            send_message(item)      ##Send Message SMS
        token_count.config(text=f"REMAINING NUMBER OF TOKENS: {count}")
        for i in queue_manager.queue:
            if tokens == " ":
                tokens = tokens +str(i)
            else:
                tokens = tokens + ", " + str(i)
        generated_tokens.delete("0",tk.END)
        generated_tokens.insert(tk.END,f"{tokens}")
        queue_manager.tokens = tokens

def screen_insert():
    global item
    #print(item)
    item = waiting_list.get(ANCHOR)
    send_message_wait(item)      ##Send Message SMS
    #print(item1)
    tokens = " "
    queue_manager.waiting.remove(item)
    #print(queue_manager.waiting)
    screen.config(text=f"{item}")
    speak(f"Token Number {item}")
    token_count.config(text=f"REMAINING NUMBER OF TOKENS: {count}")
    for i in queue_manager.queue:
        if tokens == " ":
            tokens = tokens +str(i)
        else:
            tokens = tokens + ", " + str(i)
    generated_tokens.delete("0",tk.END)
    generated_tokens.insert(tk.END,f"{tokens}")
    queue_manager.tokens = tokens
    waiting_list.delete(ANCHOR)
    
#reset tokens
def token_reset():
    global count
    global row
    column = 0
    total_count = queue_manager.total_count
    count = 0
    queue_manager.__init__()
    token_count.config(text=f"REMAINING NUMBER OF TOKENS: {count}")
    generated_tokens.delete("0",tk.END)
    screen.config(text=" ")
    waiting_list.delete(0,tk.END)
    try:
        os.remove("token_data.csv")
        tk.messagebox.showinfo("Success", "Token data reset successful. The file has been cleared.")
    except FileNotFoundError:
        tk.messagebox.showerror("Error", "The file 'token_data.csv' does not exist.")

    # now = datetime.datetime.now()
    # current_date = now.strftime("%d/%m/%Y")
    #print(current_date)
    # current_time = now.strftime("%H:%M:%S")
    #print(current_time)
    #print(row)

    


style = ttk.Style()
style.theme_use("default")
style.configure("Vertical.TScrollbar", gripcount=0, background="#f0f0f0", troughcolor="#d9d9d9", bordercolor="#d9d9d9", darkcolor="#d9d9d9", lightcolor="#d9d9d9")
scrollbar = ttk.Scrollbar(root, style="Vertical.TScrollbar")
style.configure("Horizontal.TScrollbar", gripcount=0, background="#f0f0f0", troughcolor="#d9d9d9", bordercolor="#d9d9d9", darkcolor="#d9d9d9", lightcolor="#d9d9d9")
hscrollbar = ttk.Scrollbar(root, style="Horizontal.TScrollbar", orient=tk.HORIZONTAL)

screen = tk.Label(root, text="", font=("Arial", 30), bg="black", fg="white", width=19, height=5)
screen.place(x=850,y=180)

#----------To be corrected
start = tk.PhotoImage(file='buttons/start.png')
start_button = tk.Button(root,image=start, border=0, command=start_screen, bg="#353536")
start_button.place(x=1350,y=220)
#------------------

next = tk.PhotoImage(file='buttons/next.png')
next_token = tk.Button(root, image=next, command=next_token_screen, bg='#353536',border=0)

next_token.place(x=1145,y=600)

stop = tk.PhotoImage(file='buttons/stop.png')
stop_button = tk.Button(root, image=stop, command=stop_screen, bg='#353536',border=0)
stop_button.place(x=1355,y=310)

waiting_status = tk.Label(root,text = " ", font=("Arial", 16),fg="Black", bg='#BBC0D3',height=2)
waiting_status.place(x=100,y=150)
waiting_status.config(text="WAITING LIST")

waiting_list = tk.Listbox(root, font="Arial 16",  width=37, height=8)
waiting_list.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=waiting_list.yview)
waiting_list.place(x=100,y=200)
scrollbar.place(x=548, y=200, height=204)
for i in queue_manager.waiting:
    waiting_list.insert(tk.END,i)

#print(queue_manager.waiting)

generated = tk.Label(root,text = " ", font=("Arial", 16),fg="White",bg="#353536",height=1)
generated.config(text="GENERATED TOKENS:")
generated.place(x=850,y=425)

generated_tokens = tk.Listbox(root,font=("Arial", 18),fg="black",bg="white",width=34,height=1)
generated_tokens.place(x=850,y=470)
generated_tokens.config(xscrollcommand=hscrollbar.set)
hscrollbar.config(command=generated_tokens.xview)
hscrollbar.place(x=850, y=500, width=445, height=20)
generated_tokens.delete("0",tk.END)
generated_tokens.insert(tk.END,f"{queue_manager.tokens}")

wait = tk.PhotoImage(file='buttons/wait.png')
wait_button = tk.Button(root, image=wait, command=add_to_wait, bg='#BBC0D3',border=0)
wait_button.place(x=275,y=450)

insert = tk.PhotoImage(file='buttons/insert.png')
insert_button = tk.Button(root, image=insert, command=screen_insert, bg='#BBC0D3',border=0)
insert_button.place(x=222,y=550)

generate = tk.PhotoImage(file='buttons/generate.png')
generate_button = tk.Button(root, image=generate, command=open_window, bg='#353536',border=0)
generate_button.place(x=850,y=600)

reset = tk.PhotoImage(file='buttons/reset.png')
reset_button = tk.Button(root, image=reset, command=token_reset, bg='#353536',border=0)
reset_button.place(x=1420,y=680)


root.mainloop()