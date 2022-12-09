import re
import logging

DEBUG = 0
DEBUG_LOAD = 0
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO, format='%(message)s')

DISKMAX_SIZE = 70000000
UPDATE_SIZE = 30000000

class File:
    def __init__(self, name: str, size: int = 0, parent=None):
        self.name = name
        self.size = size
        self.parent = parent

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name} (file, size={self.size})"

    @property
    def pwd(self):
        if self.parent:
            name = self.name if self.parent.pwd == "/" else f"/{self.name}"
            return self.parent.pwd + name
        return self.name

    @property
    def is_file(self):
        return self.__class__.__name__ == "File"

    @property
    def is_dir(self):
        return self.__class__.__name__ == "Directory"

class Directory(File):
    def __init__(self, name: str, parent=None):
        self.name = name
        self.parent = parent
        self.files = list()

    def __getitem__(self, obj: [str, File]) -> File:
        if isinstance(obj, File):
            obj = obj.name
        for file in self.files:
            if file.name == obj:
                return file
        return None

    def add(self, file: File):
        file.parent = self
        self.files.append(file)
        return self

    def cd(self, path: str):
        if path == '.':
            return self
        elif path == '..':
            return self.parent.cd(".") if self.parent else self
        elif path == '/':
            return self.parent.cd("/") if self.parent else self
        for directory in self.files:
            if directory.name == path:
                return directory

    @property
    def has_subdirs(self):
        for file in self.files:
            if file.is_dir:
                return True
        return False

    @property
    def size(self):
        total = 0
        for file in self.files:
            total += file.size
        return total

    @property
    def ls(self):
        txt = list()
        for file in self.files:
            if isinstance(file, File):
                txt.append(f"{file.size} {file.name}")
            else:
                txt.append(f"dir {file.name}")
        return '\n'.join(txt)

    def __repr__(self):
        return f"{self.name} (dir)"

def shell(text, system, return_to_root=False):
    fileCreation = False

    for output in text.split('\n'):
        output = output.strip()
        if not output:
            continue

        if DEBUG_LOAD:
            logging.debug(output)

        if output.startswith('$ '):
            #logging.debug(f"# ls out")
            fileCreation = False
            command = re.search('cd (?P<path>.+)', output)
            if command:
                if DEBUG_LOAD:
                    logging.debug(f"# chdir {command.group('path')}")
                system = system.cd(command.group('path'))
                continue

            command = re.search('ls', output)
            if command:
                if DEBUG_LOAD:
                    logging.debug(f"# prepare to ls")
                fileCreation = True
                continue

        if fileCreation:
            obj = re.match('(?P<size>\d+) (?P<name>[\w.]+)', output)
            if obj:
                name = str(obj.group('name'))
                size = int(obj.group('size'))
                file = File(name, size)
                if DEBUG_LOAD:
                    logging.debug(f"# Create {file}")
                system = system.add(file)

            obj = re.match('dir (?P<name>[\w.]+)', output)
            if obj:
                name = str(obj.group('name'))
                file = Directory(name)
                if DEBUG_LOAD:
                    logging.debug(f"# Create dir {file}")
                system = system.add(file)

    if return_to_root:
        system = system.cd("/")
    return system

test_root = Directory("/")
test_commands = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
test_root = shell(test_commands, test_root, return_to_root=True)

assert test_root.cd("a").cd("e").size == 584
assert test_root.cd("a").size == 94853
assert test_root.cd("d").size == 24933642
assert test_root.cd("/").size == 48381165

root = Directory("/")
with open('input', 'r') as output:
    commands = output.readlines()
    root = shell(''.join(commands), root, return_to_root=True)

def recursive_size(folder, lim = 100000):
    TOTAL_SIZE = 0
    logging.debug(f">> {folder.pwd}")
    for file in folder.files:
        logging.debug(repr(file))
    if folder.has_subdirs:
        for file in folder.files:
            if file.is_dir:
                TOTAL_SIZE += recursive_size(file, lim)
    if folder.pwd != "/" and folder.size <= lim:
        TOTAL_SIZE += folder.size
    return TOTAL_SIZE

def cleanup(folder, target: int):
    folders = list()
    if folder.has_subdirs:
        for file in folder.files:
            if file.is_dir:
                folders = folders + cleanup(file, target)
    if folder.size >= target:
        folders.append(folder)
    if folder.pwd != "/":
        return folders
    return sorted(folders, key=lambda x: x.size, reverse=False)[0]


print(recursive_size(root))

TARGET_SIZE = UPDATE_SIZE - (DISKMAX_SIZE - root.cd("/").size)
print(cleanup(root, TARGET_SIZE).size)
