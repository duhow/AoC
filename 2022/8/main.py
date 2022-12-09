class Position:
    def __init__(self, x, y, name="none"):
        self.x = int(x)
        self.y = int(y)
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self} ({self.x}, {self.y})"


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

    def is_visible(self, x: int = None, y: int = None) -> list:
        if x is None and self.x is not None:
            x = self.x
        if y is None and self.y is not None:
            y = self.y
        assert x is not None and y is not None, "Position not specified"
        my_tree = self.get(x, y)
        found = list()
        for position in [TOP, LEFT, RIGHT, BOTTOM]:
            target = Position((x + position.x), (y + position.y))
            if target.x < 0 or target.x >= self.count_x:
                continue
            if target.y < 0 or target.y >= self.count_y:
                continue
            if my_tree > self.get(target):
                found.append(position)
        return found

forest_str = """
30373
25512
65332
33549
35390
"""

test_forest = Forest(forest_str)

def test_forest_visible(x, y, positions):
    visible = test_forest.at(x, y).is_visible()
    assert visible == positions, f"Tree {test_forest.get(x, y)} visible in ({x}, {y}) does not match {visible} -> {positions} (expected)"

test_forest_visible(1, 1, [TOP, LEFT])
test_forest_visible(2, 1, [TOP, RIGHT])
test_forest_visible(3, 1, [])
test_forest_visible(1, 2, [RIGHT])
test_forest_visible(2, 2, [])
test_forest_visible(3, 2, [RIGHT])
test_forest_visible(1, 3, [])
test_forest_visible(2, 3, [BOTTOM, LEFT])
test_forest_visible(3, 3, [])
