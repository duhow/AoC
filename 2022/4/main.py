def rangify(text):
    """Split and return range + 1 to include same number."""
    values = text.split('-')
    return range(int(values[0]), int(values[1]) + 1)
    #amount = range(int(values[0]), int(values[1]) + 1)
    #return [*amount]

def contains(one, two):
    for section in one:
        if section not in two:
            return False
    return True

def includes(one, two):
    for section in one:
        if section in two:
            return True
    return False

TOTAL_CONTAINED = 0
TOTAL_INCLUDED = 0

with open('input', 'r') as ships:
    for ship in ships.readlines():
        section = ship.strip().split(',')
        elf1 = rangify(section[0])
        elf2 = rangify(section[1])

        if contains(elf1, elf2) or contains(elf2, elf1):
            TOTAL_CONTAINED += 1

        if includes(elf1, elf2) or includes(elf2, elf1):
            TOTAL_INCLUDED += 1

print(TOTAL_CONTAINED)
print(TOTAL_INCLUDED)
