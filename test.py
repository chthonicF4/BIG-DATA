
data = ["a","b","c","d"]

combos = []

for x in range(len(data)):
    for y in range(x-1):
        y+= x
        if x < y :
            combos.append((data[x],data[y]))

print(combos)
