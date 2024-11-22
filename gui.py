import tkinter as tk
from tkinter import scrolledtext
from shell import Shell
class ShellGUI:
    def __init__(self, master, user, vfs):
        self.master = master
        self.shell = Shell(user, vfs)

        self.output = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=80, height=20)
        self.output.pack()

        self.entry = tk.Entry(master, width=80)
        self.entry.pack()
        self.entry.bind("<Return>", self.run_command)

        self.output.insert(tk.END, f"{user}@shell:~$ Welcome to the shell emulator!\n\n")

    def run_command(self, event):
        command = self.entry.get()
        self.output.insert(tk.END, f"{self.shell.user}@shell:~$ {command}\n")
        result = self.shell.execute_command(command)
        self.output.insert(tk.END, f"{result}\n\n")
        self.entry.delete(0, tk.END)
        if command.strip() == "exit":
            self.master.quit()
