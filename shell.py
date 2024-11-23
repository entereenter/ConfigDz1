import platform
#Класс для обработки команд
class Shell:
    #Конструктор
    def __init__(self, user, vfs):
        self.user = user
        self.vfs = vfs
    #Обработка введенной команды
    def execute_command(self, command):
        parts = command.strip().split()#Отделяем ком


        cmd = parts[0]
        args = parts[1:]

        if cmd == "ls":
            return self.list_files(args)
        elif cmd == "cd":
            return self.change_directory(args)
        elif cmd == "wc":
            return self.word_count(args)
        elif cmd == "exit":
            return "Exiting..."
        elif cmd == "uname":
            return self.uname()
        else:
            return f"Command '{cmd}' not found."
    #Командла ls
    def list_files(self, args):
        try:
            path = args[0] if args else None
            files = self.vfs.list_files(path)
            return "\n".join(files)
        except Exception as e:
            return str(e)
    #Команда cd
    def change_directory(self, args):
        if not args:
            return "Usage: cd <path>"
        try:
            new_path = self.vfs.change_directory(args[0])
            return f"Changed directory to {new_path}"
        except Exception as e:
            return str(e)
    #Команда wc
    def word_count(self, args):
        if not args:
            return "Usage: wc <file_name>"
        try:
            lines, words, chars = self.vfs.wc(args[0])
            return f"Lines: {lines}, Words: {words}, Characters: {chars}"
        except Exception as e:
            return str(e)
    #Команда uname
    def uname(self):
        return platform.system()
