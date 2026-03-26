import tkinter as tk

def start_fake_update():
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.attributes('-topmost', True)
    root.configure(background='#0078d7')
    root.config(cursor="none")

    # Display Text
    label = tk.Label(root, text="Working on updates 27%\nPlease keep your computer on. Your PC will restart several times.", 
                     fg="white", bg="#0078d7", font=("Segoe UI", 25))
    label.pack(expand=True)

    # Secret sequence tracker
    typed_secret = ""
    secret_key = "niyal"

    def check_key(event):
        nonlocal typed_secret
        # Sirf letters ko track karo
        char = event.char.lower()
        
        if char:
            typed_secret += char
            # Agar sequence match ho gaya
            if secret_key in typed_secret:
                root.destroy()
            
            # Memory clean-up: Agar string bahut lambi ho jaye toh reset kar do
            if len(typed_secret) > 20:
                typed_secret = typed_secret[-5:]

    # Saari keypresses ko bind karo
    root.bind('<Key>', check_key)
    
    # Rokne ke liye Alt+F4 wagera block karna (Optional but pro)
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    
    root.mainloop()