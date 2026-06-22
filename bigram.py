from collections import defaultdict
import random

with open("data/shakespeare.txt", "r", encoding="utf-8") as f:
    text = f.read()

model = defaultdict(list)

for c1, c2 in zip(text, text[1:]):
    model[c1].append(c2)

current = random.choice(text)

generated = current

for _ in range(500):

    if current not in model:
        break

    next_char = random.choice(model[current])

    generated += next_char

    current = next_char

print(generated)