from collections import Counter

with open("data/shakespeare.txt", "r", encoding="utf-8") as f:
    text = f.read()

freq = Counter(text)

print("=== TOKEN FREQUENCY ===")

for char, count in freq.most_common():
    print(repr(char), count)