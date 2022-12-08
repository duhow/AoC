import re
import logging

DEBUG = 1
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO, format='%(message)s')

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
        #if not self.files:
        #        return ''
        #    cwd = []
        #    for file in self.files:
        #        if isinstance(file, File):
        #            cwd.append(repr(file))
        #        else:
        #            cwd.append({repr(file): str(file)})
        #    data = cwd
        #    return yaml.dump(data)

def shell(text, system):
    fileCreation = False

    for output in text.split('\n'):
        output = output.strip()
        if not output:
            continue

        logging.debug(output)

        if output.startswith('$ '):
            #logging.debug(f"# ls out")
            fileCreation = False
            command = re.search('cd (?P<path>.+)', output)
            if command:
                logging.debug(f"# chdir {command.group('path')}")
                system = system.cd(command.group('path'))
                continue

            command = re.search('ls', output)
            if command:
                logging.debug(f"# prepare to ls")
                fileCreation = True
                continue

        if fileCreation:
            obj = re.match('(?P<size>\d+) (?P<name>[\w.]+)', output)
            if obj:
                name = str(obj.group('name'))
                size = int(obj.group('size'))
                file = File(name, size)
                logging.debug(f"# Create {file}")
                system = system.add(file)

            obj = re.match('dir (?P<name>[\w.]+)', output)
            if obj:
                name = str(obj.group('name'))
                file = Directory(name)
                logging.debug(f"# Create dir {file}")
                system = system.add(file)

    return system

#root = Directory("/")
#root.add(Directory("a")) \
#    .add(File("b.txt", 14848514)) \
#    .add(File("c.dat", 8504156)) \
#    .add(Directory("d"))
#
#root.cd("a") \
#    .add(Directory("e")) \
#    .add(File("f", 29116)) \
#    .add(File("g", 2557)) \
#    .add(File("h.lst", 62596))
#print(root.size)

root = Directory("/")
with open('input', 'r') as output:
    commands = output.readlines()
    root = shell(''.join(commands), root)

print("# -------")
root = root.cd("/")
print(root.ls)
print("# -------")

def recursive_size(folder, lim = 100000):
    TOTAL_SIZE = 0
    logging.debug(f">> {folder.pwd}")
    for file in folder.files:
        print(repr(file))
    if folder.has_subdirs:
        for file in folder.files:
            if file.is_dir:
                return recursive_size(file, lim)
    if folder.pwd != "/":
        TOTAL_SIZE += folder.size
    return TOTAL_SIZE
#    for file in folder.files:
#        logging.debug(f"># {repr(file)}")
#        if file.is_dir and file.has_subdirs:
#            return recursive_size(file)
#        if file.is_dir and file.size > lim:
#            logging.debug(f"Size of {file.pwd}")
#            TOTAL_SIZE += file.size
#    return TOTAL_SIZE

print(recursive_size(root))
