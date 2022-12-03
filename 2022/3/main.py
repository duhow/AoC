
TOTAL = 0
TOTAL_GROUP = 0
GROUP = 0
GROUP_RUCKSACK = []

def prioritize(item) -> int:
    MAYUS = int(item == item.upper())
    # a-z = 1-26, A-Z = 27-52
    if not MAYUS:
        value = ord(item) - (1 << 6) - (1 << 5)
    else:
        value = ord(item) - (1 << 6) + 26
    return value


with open('input', 'r') as bags:
    for rucksack in bags.readlines():
        rucksack = rucksack.strip()
        items = len(rucksack)
        half_part = int(items / 2)
        part1 = rucksack[0:half_part]
        part2 = rucksack[half_part:]
        assert len(part1) == len(part2), "wut"

        # apparently there's only one?
        common = set()
        for item in part1:
            if item in part2:
                common.add(item)

        maxval = 0
        for item in common:
            value = prioritize(item)
            if value > maxval:
                maxval = value
        #print(f"{common} {maxval} {rucksack}")
        TOTAL += maxval

        GROUP += 1
        GROUP_RUCKSACK.append(rucksack)
        if GROUP == 3:
            for item in rucksack:
                if (
                    item in GROUP_RUCKSACK[0] and
                    item in GROUP_RUCKSACK[1] and
                    item in GROUP_RUCKSACK[2]
                ):
                    TOTAL_GROUP += prioritize(item)
                    #print(f"{item} {prioritize(item)} {GROUP_RUCKSACK}")
                    break # one!

            #print(">>")
            # empty and restart
            GROUP_RUCKSACK = []
            GROUP = 0

print(TOTAL)
print(TOTAL_GROUP)
