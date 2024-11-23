import os
import tarfile

#Класс для работы с виртуальной файловой системы
class VirtualFileSystem:
    #Коснтруктор
    def __init__(self, tar_path):
        self.tar_path = tar_path
        self.extract_path = '/tmp/vfs'
        self.current_dir = self.extract_path
        self.mount() #Распаковываем архив

#Распаковка архива
    def mount(self):
        if not os.path.exists(self.extract_path):
            os.makedirs(self.extract_path)#Создаем папку если отсутствует
        with tarfile.open(self.tar_path, 'r') as archive: #Открываем архив в режиме чтения
            archive.extractall(self.extract_path) #Извлекаем содержимое

#Функция ls
    def list_files(self, path=None):
        path = path or self.current_dir
        if os.path.exists(path):
            return os.listdir(path) #Возвращаем список файлов и папок
        else:
            raise FileNotFoundError(f"Path {path} does not exist.")
#Функция cd
    def change_directory(self, relative_path):
    #Переход в родительскую директорию
        if relative_path == "-":
            parent_dir = os.path.dirname(self.current_dir)
            if parent_dir == self.current_dir: #Текущая директория является корневой
                return "No previous directory to return to."
            self.current_dir = parent_dir #Обновление текущей директории
            return f"Changed directory to {self.current_dir}"
        else:
            #создание абсолютного пути и его проверка
            new_path = os.path.abspath(os.path.join(self.current_dir, relative_path))
            if os.path.exists(new_path) and os.path.isdir(new_path): #Проверка пути и директории
                self.current_dir = new_path #Обновление текущей директории
                return f"Changed directory to {self.current_dir}"
            else:
                raise FileNotFoundError(f"Directory {relative_path} does not exist.")
#Функция для чтения файла
    def read_file(self, file_name):
        file_path = os.path.join(self.current_dir, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f: #Открываем в режиме чтения
                return f.read()
        else:
            raise FileNotFoundError(f"File {file_name} does not exist.")
#Функция wc
    def wc(self, file_name):
        content = self.read_file(file_name)
        lines = content.splitlines()#Разбить на строки
        words = content.split()#Разюить на слова
        chars = len(content)#Разбить на символы
        return len(lines), len(words), chars
