# ==========================================================
# Week 1 - Frequency Analyzer
# Menghitung frekuensi setiap karakter pada dataset
# ==========================================================

from collections import Counter
import os

# ==========================
# Membaca Dataset
# ==========================

with open("data/shakespeare.txt", "r", encoding="utf-8") as f:
    text = f.read()

print("=" * 50)
print("Dataset berhasil dibaca")
print("Jumlah karakter:", len(text))
print("=" * 50)

# ==========================
# Menghitung Frekuensi
# ==========================

counter = Counter(text)

# Urutkan dari yang paling sering muncul
frequency = counter.most_common()

# ==========================
# Tampilkan Hasil
# ==========================

print("\n=== 20 Karakter Terbanyak ===")

for char, freq in frequency[:20]:
    if char == "\n":
        display = "\\n"
    elif char == " ":
        display = "[SPACE]"
    else:
        display = char

    print(f"{display:10} : {freq}")

# ==========================
# Membuat Folder Output
# ==========================

os.makedirs("Week1/output", exist_ok=True)

# ==========================
# Simpan ke File
# ==========================

with open("Week1/output/frequency_table.txt", "w", encoding="utf-8") as f:

    f.write("Karakter\tFrekuensi\n")
    f.write("-" * 30 + "\n")

    for char, freq in frequency:

        if char == "\n":
            display = "\\n"
        elif char == " ":
            display = "[SPACE]"
        else:
            display = char

        f.write(f"{display}\t{freq}\n")

print("\nFrekuensi berhasil disimpan di:")
print("Week1/output/frequency_table.txt")