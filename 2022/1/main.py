maxcals = 0
with open('input', 'r') as duendes:
    actual = 0
    for kcal in duendes.readlines():
        if not kcal.strip().isnumeric():
            if actual > maxcals:
                maxcals = actual
            actual = 0
        else:
            actual += int(kcal)
print(maxcals)

# ---

maxcals = []
with open('input', 'r') as duendes:
    actual = 0
    for kcal in duendes.readlines():
        if not kcal.strip().isnumeric():
            maxcals.append(actual)
            actual = 0
        else:
            actual += int(kcal)

maxcals = sorted(maxcals, reverse=True)
for i in range(0, 3):
    print(maxcals[i])
