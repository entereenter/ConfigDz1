import sys
from tkinter import Tk
from vfs import VirtualFileSystem
from gui import ShellGUI


def main():
    if len(sys.argv)!=3:
        print("Usage: python main.py <username> <tar_path>")
        sys.exit(1)

    username = sys.argv[1]
    tar_path = sys.argv[2]

    try:
        vfs = VirtualFileSystem(tar_path)
    except Exception as e:
        print(f"Error initializing virtual file system: {e}")
        sys.exit(1)
#создание и запуск
    root = Tk()
    root.title("Dz1 Shell Emulator xD")
    gui = ShellGUI(root, username, vfs)
    root.mainloop()
if __name__ == "__main__":
    main()