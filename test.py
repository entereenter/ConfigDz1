import os
import unittest
from vfs import VirtualFileSystem
from shell import Shell
import platform

class TestVirtualFileSystem(unittest.TestCase):
    def setUp(self):
        self.tar_path = "archive.tar"
        self.vfs = VirtualFileSystem(self.tar_path)

    def test_list_files_success(self):
        files = self.vfs.list_files()
        self.assertTrue(len(files) > 0, "Файлы должны быть в архиве")

    def test_list_files_nonexistent_path(self):
        with self.assertRaises(FileNotFoundError):
            self.vfs.list_files("/nonexistent")

    def test_change_directory_success(self):
        result = self.vfs.change_directory(".")
        expected_path = os.path.normpath(self.vfs.extract_path)  # Нормализация пути
        self.assertIn(expected_path, result)

    def test_change_directory_failure(self):
        with self.assertRaises(FileNotFoundError):
            self.vfs.change_directory("/nonexistent")

    def test_wc_success(self):
        file_name = next(f for f in self.vfs.list_files() if os.path.isfile(os.path.join(self.vfs.current_dir, f)))
        lines, words, chars = self.vfs.wc(file_name)
        self.assertTrue(lines > 0, "Файл должен содержать строки")
        self.assertTrue(words > 0, "Файл должен содержать слова")
        self.assertTrue(chars > 0, "Файл должен содержать символы")

    def test_wc_failure(self):
        with self.assertRaises(FileNotFoundError):
            self.vfs.wc("nonexistent.txt")


class TestShell(unittest.TestCase):
    def setUp(self):
        self.tar_path = "archive.tar"  # Укажите свой путь
        self.vfs = VirtualFileSystem(self.tar_path)
        self.shell = Shell("testuserxD", self.vfs)

    def test_ls_command(self):
        result = self.shell.execute_command("ls")
        self.assertTrue(len(result) > 0, "Команда ls должна возвращать файлы")

    def test_ls_nonexistent(self):
        result = self.shell.execute_command("ls /nonexistent")
        self.assertIn("does not exist", result)

    def test_cd_command(self):
        result = self.shell.execute_command("cd .")
        self.assertIn("Changed directory", result)

    def test_cd_nonexistent(self):
        result = self.shell.execute_command("cd /nonexistent")
        self.assertIn("does not exist", result)

    def test_wc_command(self):
        file_name = next(f for f in self.vfs.list_files() if os.path.isfile(os.path.join(self.vfs.current_dir, f)))
        result = self.shell.execute_command(f"wc {file_name}")
        self.assertIn("Lines:", result)
        self.assertIn("Words:", result)
        self.assertIn("Characters:", result)

    def test_wc_nonexistent(self):
        result = self.shell.execute_command("wc nonexistent.txt")
        self.assertIn("does not exist", result)

    def test_uname_command(self):
        result = self.shell.execute_command("uname")
        self.assertIn(platform.system(), result)

    def test_invalid_command(self):
        result = self.shell.execute_command("invalid")
        self.assertIn("not found", result)


if __name__ == "__main__":
    unittest.main()
