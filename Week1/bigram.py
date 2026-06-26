# ==========================================================
# Week 1 - Bigram Generator
# Membuat teks sederhana menggunakan Bigram
# ==========================================================

import random
import os

# ==========================
# Membaca Dataset
# ==========================

with open("data/shakespeare.txt", "r", encoding="utf-8") as f:
    text = f.read()

# ==========================
# Membuat Bigram
# ==========================

bigram = {}

for i in range(len(text) - 1):

    current = text[i]
    next_char = text[i + 1]

    if current not in bigram:
        bigram[current] = []

    bigram[current].append(next_char)

print("=" * 50)
print("Jumlah karakter unik:", len(bigram))
print("=" * 50)

# ==========================
# Membuat Teks Baru
# ==========================

current = random.choice(list(bigram.keys()))

generated = current

for _ in range(500):

    if current not in bigram:
        break

    current = random.choice(bigram[current])

    generated += current

# ==========================
# Tampilkan Hasil
# ==========================

print("\n=== Sample Generated Text ===\n")
print(generated)

# ==========================
# Membuat Folder Output
# ==========================

os.makedirs("Week1/output", exist_ok=True)

# ==========================
# Simpan ke File
# ==========================

with open("Week1/output/generated_text.txt", "w", encoding="utf-8") as f:

    f.write(generated)

print("\nGenerated text berhasil disimpan.")
print("Week1/output/generated_text.txt")