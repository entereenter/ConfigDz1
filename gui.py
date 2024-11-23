import tkinter as tk
from tkinter import scrolledtext
from shell import Shell
#Класс для графического интерфейса
class ShellGUI:
    #Конструктор
    def __init__(self, master, user, vfs):
        self.master = master
        self.shell = Shell(user, vfs)
        # Поле для вывода результатов команд
        self.output = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=80, height=20)
        self.output.pack() #Размещение в окне

        # Поле для ввода команд
        self.entry = tk.Entry(master, width=80)
        self.entry.pack()
        self.entry.bind("<Return>", self.run_command) #Привязка enter к выполнению команд

        self.output.insert(tk.END, f"{user}@shell:~$ Welcome to the shell emulator!\n\n")
    #Обработка ввода команд
    def run_command(self, event):
        command = self.entry.get()
        self.output.insert(tk.END, f"{self.shell.user}@shell:~$ {command}\n") #Отображение команды
        result = self.shell.execute_command(command)
        self.output.insert(tk.END, f"{result}\n") #Отображение результата работы команды
        self.entry.delete(0, tk.END)
        if command.strip() == "exit":
            self.master.quit()
