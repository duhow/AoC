class Position:
    def __init__(self, x=0, y=0, name="none"):
        self.x = int(x)
        self.y = int(y)
        self.name = name

    def __hash__(self):
        return 0

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self} ({self.x}, {self.y})"

    def get_from(self, pos, max_corner=None):
        """ Return a new copy, do not modify original """
        new = self.__class__(self.x, self.y, self.name)
        if pos.x == -1:
            new.x = 0
        if pos.x == 1 and max_corner:
            new.x = max_corner.x
        if pos.y == -1:
            new.y = 0
        if pos.y == 1 and max_corner:
            new.y = max_corner.y
        return new

    def generate_to(self, pos):
        if self == pos:
            return
        if self.x == pos.x:
            if self.y > pos.y:
                while self != pos:
                    yield self
                    self.y -= 1
            else:
                while self != pos:
                    yield self
                    self.y += 1
        elif self.y == pos.y:
            if self.x > pos.x:
                while self != pos:
                    yield self
                    self.x -= 1
            else:
                while self != pos:
                    yield self
                    self.x += 1

TOP = Position(0, -1, "TOP")
LEFT = Position(-1, 0, "LEFT")
RIGHT = Position(1, 0, "RIGHT")
BOTTOM = Position(0, 1, "BOTTOM")

class Tree:
    def __init__(self, height: int):
        self.height = int(height)

    def __str__(self):
        return str(self.height)

    def __repr__(self):
        return f"{self.__class__.__name__} ({self.height})"

    def __gt__(self, other):
        return self.height > other.height

    def __ge__(self, other):
        return self.height >= other.height

    def __lt__(self, other):
        return self.height < other.height

class Forest:
    def __init__(self, string_forest: str):
        self.trees = list()
        self.selected = None
        self.x = None
        self.y = None
        self.count_x = 0
        self.count_y = 0

        for row in string_forest.split('\n'):
            if not row:
                continue
            row_trees = list()
            for tree_num in row:
                row_trees.append(Tree(tree_num))
            assert self.count_x in (0, len(row_trees)), "Different amount of row trees!"
            self.count_x = len(row_trees)
            self.trees.append(row_trees)
        self.count_y = len(self.trees)
        # count - 1 ?
        self.position_max = Position(self.count_x - 1, self.count_y - 1)

    def __str__(self):
        txt = ""
        for row in range(len(self.trees)):
            txt += ''.join([str(tree) for tree in self.trees[row]]) + '\n'
        return txt.strip()

    def at(self, x: [int, Position], y: int):
        if isinstance(x, Position):
            y = x.y
            x = x.x
        self.x = x
        self.y = y
        self.selected = self.get(x, y)
        return self

    def get(self, x: [int, Position], y: int = None) -> Tree:
        if isinstance(x, Position):
            y = x.y
            x = x.x
        return self.trees[y][x]

    def is_visible(self, x: int = None, y: int = None) -> set:
        if x is None and self.x is not None:
            x = self.x
        if y is None and self.y is not None:
            y = self.y
        assert x is not None and y is not None, "Position not specified"

        my_pos = Position(x, y)
        my_tree = self.get(my_pos)
        found = set()

        for direction in [TOP, LEFT, RIGHT, BOTTOM]:
            is_accepted = True
            for position_to_check in my_pos.get_from(direction, self.position_max).generate_to(my_pos):
                that_tree = self.get(position_to_check)
                #print(f"{my_tree} < {that_tree}? ({position_to_check.x} {position_to_check.y})")
                if that_tree >= my_tree:
                    is_accepted = False
                    break
            if is_accepted:
                found.add(direction)
            #print("-----")
        return found

test_position = Position(4, 6)
test_position_max = Position(10, 10)

def test_position_generator(pos, get_from, expected, max_corner=None):
    count = 0 
    for x in pos.get_from(get_from, max_corner).generate_to(pos):
        count += 1
    assert count == expected, f"Expected {expected}, but count is {count}"

test_position_generator(test_position, TOP, 6)
test_position_generator(test_position, LEFT, 4)

forest_str = """
30373
25512
65332
33549
35390
"""

test_forest = Forest(forest_str)

def test_forest_visible(x, y, positions):
    if isinstance(positions, list):
        positions = set(positions)
    visible = test_forest.at(x, y).is_visible()
    assert visible == positions, f"Tree {test_forest.get(x, y)} visible in ({x}, {y}) does not match {visible} -> {positions} (expected)"

test_forest_visible(1, 1, [TOP, LEFT])
test_forest_visible(2, 1, [TOP, RIGHT])
test_forest_visible(3, 1, [])
test_forest_visible(1, 2, [RIGHT])
test_forest_visible(2, 2, [])
test_forest_visible(3, 2, [RIGHT])
test_forest_visible(1, 3, [])
test_forest_visible(2, 3, [LEFT, BOTTOM])
test_forest_visible(3, 3, [])

with open('input', 'r') as forest_file:
    forest_txt = ''.join(forest_file.readlines())

TOTAL_VISIBLE = 0
forest = Forest(forest_txt)

for x in range(forest.count_x):
    for y in range(forest.count_y):
        if forest.at(x, y).is_visible():
            TOTAL_VISIBLE += 1

print(TOTAL_VISIBLE)
