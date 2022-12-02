from dataclasses import dataclass
from typing import Optional

LOSE = 0
DRAW = 3
WIN = 6

@dataclass
class Element:
    name: str
    value: int
    matches: list[str]
    beats: Optional = None

    def __str__(self):
        return self.name

    def __gt__(self, element):
        self.beats = element

    def __eq__(self, element):
        if not element:
            return False
        return self.value == element.value

    # >>
    def __rshift__(self, element):
        return self.value + self.__ge__(element)

    # >=
    def __ge__(self, element):
        if self == element:
            return DRAW
        if element == self.beats:
            return WIN
        return LOSE

ROCK = Element("Rock", 1, ["A", "X"])
PAPER = Element("Paper", 2, ["B", "Y"])
SCISSORS = Element("Scissors", 3, ["C", "Z"])

# set rules:
ROCK > SCISSORS
SCISSORS > PAPER 
PAPER > ROCK

def materialize(player) -> Element:
    for element in [ROCK, PAPER, SCISSORS]:
        if player in element.matches:
            return element

def prompt_play(play, opponent):
    matches = {"X": LOSE, "Y": DRAW, "Z": WIN}
    for element in [ROCK, PAPER, SCISSORS]:
        if (element >= opponent) == matches.get(play):
            return element 

POINTS = 0

with open("input", "r") as rounds:
    for fight in rounds.readlines():
        # remove newline
        players = fight.strip().split(" ")
        opponent = materialize(players[0])
        myself = materialize(players[1])

        POINTS += myself >> opponent

print(POINTS)

# -----
POINTS = 0

with open("input", "r") as rounds:
    for fight in rounds.readlines():
        players = fight.strip().split(" ")
        opponent = materialize(players[0])
        myself = prompt_play(players[1], opponent)

        POINTS += myself >> opponent

print(POINTS)
