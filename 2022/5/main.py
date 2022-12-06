import re
import logging

MOVE_ORDER = r"move (?P<amount>\d+) from (?P<from>\d+) to (?P<to>\d+)"
DEBUG = 0

logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)

class Cargo:
    def __init__(self, text):
        # get numbers from last line, count how many are 
        last_line = text.split('\n')[-1].replace(' ', ',')
        last_num = -1
        for element in last_line.split(','):
            if element and element.isnumeric() and int(element) > last_num:
                last_num = int(element)

        count = int(last_num)

        # initialize cargo
        self.stacks = list()
        for n in range(count):
            self.stacks.append(list())

        for line in text.split('\n'):
            for idx in range(count):
                stack = line[idx*4:idx*4+3].strip()
                if stack and stack.startswith('[') and stack.endswith(']'):
                    # get letter in second position
                    self.stacks[idx].insert(0, stack[1])

    def move(self, amount: int, _from: int, to: int, multiple=False):
        # arrays start at one :) 
        amount = int(amount)
        _from = int(_from)
        to = int(to)

        _from = _from - 1
        to = to - 1

        logging.debug(f"{amount=} {_from=} {to=}")
        if not multiple:
            for count in range(amount):
                try:
                    stack = self.stacks[_from].pop()
                    self.stacks[to].append(stack)
                except IndexError:
                    logging.warning(f"No more cargo left! {count=}")
                    #raise Exception(f"No more cargo left! {count=}")
                    pass
        elif multiple:
            # including the new position to insert into
            last_position = len(self.stacks[to])
            for count in range(amount):
                try:
                    stack = self.stacks[_from].pop()
                    self.stacks[to].insert(last_position, stack)
                except IndexError:
                    logging.warning(f"No more cargo left! {count=}")
                    #raise Exception(f"No more cargo left! {count=}")
                    pass

    def __str__(self):
        max_len = 0
        for stack in self.stacks:
            if len(stack) > max_len:
                max_len = len(stack) - 1

        text = ""
        for idx in range(max_len, 0 - 1, -1):
            for stack in self.stacks:
                try:
                    text += f"[{stack[idx]}] "
                except IndexError:
                    text += " " * 4
                    pass
            text += "\n"

        for idx in range(len(self.stacks)):
            text += f" {idx + 1}  "

        return text


    @property
    def top_stacks(self):
        return ''.join([self.stacks[x][-1] for x in range(len(self.stacks))])

# ---
test_cargo = Cargo("""
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 """)

assert test_cargo, "Error on creating cargo"

orders = """
move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""

for line in orders.split('\n'):
    order = re.match(MOVE_ORDER, line)
    if not order:
        continue
    amount, source, target = order.groups()
    test_cargo.move(amount, source, target)

assert test_cargo.top_stacks == "CMZ", f"Cargo top stacks don't match: {test_cargo.top_stacks}"

# ---

lines = []
with open('input', 'r') as cargo:
    for line in cargo.readlines():
        # WARNING!!!! DO NOT STRIP!
        line = line.replace('\n', '')
        if line and not 'move' in line:
            lines.append(line)
        if 'move' in line:
            break

lines = '\n'.join(lines)
cargo = Cargo(lines)
cargo_modern = Cargo(lines)

with open('input', 'r') as orders:
    for line in orders.readlines():
        line = line.strip()
        if not 'move' in line:
            continue
        order = re.match(MOVE_ORDER, line)
        if not order:
            continue

        amount, source, target = order.groups()
        logging.debug(line)
        cargo.move(amount, source, target)
        cargo_modern.move(amount, source, target, multiple=True)

print(cargo.top_stacks)
print(cargo_modern.top_stacks)
