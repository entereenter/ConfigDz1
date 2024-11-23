import os
import tarfile

class VirtualFileSystem:
    def __init__(self, tar_path):
        self.tar_path = tar_path
        self.extract_path = '/tmp/vfs'
        self.current_dir = self.extract_path
        self.mount()

    def mount(self):
        if not os.path.exists(self.extract_path):
            os.makedirs(self.extract_path)
        with tarfile.open(self.tar_path, 'r') as archive:
            archive.extractall(self.extract_path)

    def list_files(self, path=None):
        path = path or self.current_dir
        if os.path.exists(path):
            return os.listdir(path)
        else:
            raise FileNotFoundError(f"Path {path} does not exist.")

    def change_directory(self, relative_path):

        if relative_path == "-":
            parent_dir = os.path.dirname(self.current_dir)
            if parent_dir == self.current_dir:
                return "No previous directory to return to."
            self.current_dir = parent_dir
            return f"Changed directory to {self.current_dir}"
        else:

            new_path = os.path.abspath(os.path.join(self.current_dir, relative_path))
            if os.path.exists(new_path) and os.path.isdir(new_path):
                self.current_dir = new_path
                return f"Changed directory to {self.current_dir}"
            else:
                raise FileNotFoundError(f"Directory {relative_path} does not exist.")

    def read_file(self, file_name):
        file_path = os.path.join(self.current_dir, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return f.read()
        else:
            raise FileNotFoundError(f"File {file_name} does not exist.")

    def wc(self, file_name):
        content = self.read_file(file_name)
        lines = content.splitlines()
        words = content.split()
        chars = len(content)
        return len(lines), len(words), chars
