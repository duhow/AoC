def locateStartPacket(text, lenght=4) -> int:
    for idx in range(len(text)):
        packet = text[idx:idx+lenght]
        found = False
        #print(packet)
        for letter in packet:
            # finding a unique letter,
            # if lenght is less than expected, then key is repeated
            if len(packet.replace(letter, '')) != (lenght - 1):
                #print(f"{letter=} in {packet=}")
                found = True
                break
        if not found:
            return idx+lenght

tests = [
    ["bvwbjplbgvbhsrlpgdmjqwftvncz", 5],
    ["nppdvjthqldpwncqszvftbrmjlhg", 6],
    ["nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10],
    ["zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11]
]

for test in tests:
    location = locateStartPacket(test[0])
    assert location == test[1], f"Location is {location}"

with open('input', 'r') as broadcast:
    message = broadcast.readline().strip()
    print(locateStartPacket(message))
    print(locateStartPacket(message, 14))
