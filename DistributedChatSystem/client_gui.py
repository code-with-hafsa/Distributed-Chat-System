import socket
import threading
import tkinter as tk
from tkinter import simpledialog
from datetime import datetime

HOST = '127.0.0.1'
PORT = 5555


class WhatsAppChat:
    def __init__(self, root):
        self.root = root
        self.root.title("Distributed Chat")
        self.root.geometry("750x600")
        self.root.minsize(450, 400)
        self.root.configure(bg="#0b141a")

        self.nickname = simpledialog.askstring(
            "Name", "Enter your nickname:", parent=root
        )

        # HEADER
        self.header = tk.Label(
            root,
            text="💬 Distributed Chat System",
            bg="#0b141a",
            fg="white",
            font=("Arial", 14, "bold")
        )
        self.header.pack(pady=10)

        # CHAT AREA (canvas for bubbles)
        self.chat_frame = tk.Frame(root, bg="#0b141a")
        self.chat_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.chat_frame, bg="#0b141a", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.chat_frame, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.message_frame = tk.Frame(self.canvas, bg="#0b141a")
        self.canvas.create_window((0, 0), window=self.message_frame, anchor="nw")

        self.message_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # INPUT AREA (FIXED)
        self.input_frame = tk.Frame(root, bg="#0b141a")
        self.input_frame.pack(fill=tk.X, padx=10, pady=10)

        self.msg_entry = tk.Entry(
            self.input_frame,
            font=("Arial", 12),
            bg="#1f2c34",
            fg="white",
            insertbackground="white"
        )
        self.msg_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
        self.msg_entry.bind("<Return>", self.send_message)

        self.send_btn = tk.Button(
            self.input_frame,
            text="Send",
            bg="#00a884",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.send_message
        )
        self.send_btn.pack(side=tk.RIGHT)

        # SOCKET
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))

        threading.Thread(target=self.receive, daemon=True).start()

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')

                if message == "NICK":
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    self.add_message(message, incoming=True)

            except:
                break

    def send_message(self, event=None):
        msg = self.msg_entry.get()

        if msg:
            time = datetime.now().strftime("%H:%M")
            full_msg = f"[{time}] {self.nickname}: {msg}"

            self.client.send(full_msg.encode('utf-8'))
            self.msg_entry.delete(0, tk.END)

    def add_message(self, msg, incoming=False):
        bubble_frame = tk.Frame(self.message_frame, bg="#0b141a")

        if incoming:
            bg = "#1f2c34"
            anchor = "w"
        else:
            bg = "#005c4b"
            anchor = "e"

        label = tk.Label(
            bubble_frame,
            text=msg,
            bg=bg,
            fg="white",
            font=("Arial", 11),
            wraplength=400,
            justify="left",
            padx=10,
            pady=5
        )

        label.pack(anchor=anchor, pady=3, padx=10)
        bubble_frame.pack(fill=tk.X, anchor=anchor)

        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1)


root = tk.Tk()
app = WhatsAppChat(root)
root.mainloop()