# ==========================================================
# Week 1 - Tokenizer
# Membuat Character Vocabulary, STOI, ITOS,
# Encode, Decode, dan menyimpan hasil ke file.
# ==========================================================

# ==========================
# Membaca Dataset
# ==========================

with open("data/shakespeare.txt", "r", encoding="utf-8") as f:
    text = f.read()

print("=" * 50)
print("Dataset berhasil dibaca.")
print("Jumlah karakter :", len(text))
print("=" * 50)


# ==========================
# Membuat Character Vocabulary
# ==========================

chars = sorted(list(set(text)))

print("\nVocabulary:")
print(chars)

print("\nJumlah Vocabulary:", len(chars))


# ==========================
# Membuat STOI dan ITOS
# ==========================

stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for i, ch in enumerate(chars)}

print("\nSTOI (String to Integer):")
print(stoi)

print("\nITOS (Integer to String):")
print(itos)


# ==========================
# Encode Function
# Mengubah teks menjadi Token ID
# ==========================

def encode(text):
    return [stoi[c] for c in text]


# ==========================
# Decode Function
# Mengubah Token ID menjadi teks
# ==========================

def decode(tokens):
    return "".join([itos[i] for i in tokens])


# ==========================
# Contoh Encode & Decode
# ==========================

sample = "To be"

encoded = encode(sample)
decoded = decode(encoded)

print("\n" + "=" * 50)
print("Contoh Encode & Decode")
print("=" * 50)

print("Text    :", sample)
print("Encode  :", encoded)
print("Decode  :", decoded)


# ==========================
# Membuat Folder Output
# ==========================

import os

os.makedirs("Week1/output", exist_ok=True)


# ==========================
# Simpan Vocabulary
# ==========================

with open("Week1/output/vocabulary.txt", "w", encoding="utf-8") as f:
    f.write("=== Vocabulary ===\n\n")

    for i, ch in enumerate(chars):
        if ch == "\n":
            f.write(f"{i:>3} : \\n\n")
        elif ch == " ":
            f.write(f"{i:>3} : [SPACE]\n")
        else:
            f.write(f"{i:>3} : {ch}\n")

    f.write("\n")
    f.write(f"Jumlah Vocabulary : {len(chars)}")


# ==========================
# Simpan STOI & ITOS
# ==========================

with open("Week1/output/stoi_itos.txt", "w", encoding="utf-8") as f:

    f.write("========== STOI ==========\n\n")

    for k, v in stoi.items():
        if k == "\n":
            f.write(f"\\n -> {v}\n")
        elif k == " ":
            f.write(f"[SPACE] -> {v}\n")
        else:
            f.write(f"{k} -> {v}\n")

    f.write("\n\n========== ITOS ==========\n\n")

    for k, v in itos.items():
        if v == "\n":
            f.write(f"{k} -> \\n\n")
        elif v == " ":
            f.write(f"{k} -> [SPACE]\n")
        else:
            f.write(f"{k} -> {v}\n")


# ==========================
# Simpan Encode & Decode
# ==========================

with open("Week1/output/sample_encode_decode.txt", "w", encoding="utf-8") as f:

    f.write("=== Sample Encode & Decode ===\n\n")

    f.write(f"Text   : {sample}\n")
    f.write(f"Encode : {encoded}\n")
    f.write(f"Decode : {decoded}\n")


# ==========================
# Informasi Akhir
# ==========================

print("\n" + "=" * 50)
print("Semua hasil berhasil disimpan!")
print("=" * 50)

print("Folder output:")
print("├── vocabulary.txt")
print("├── stoi_itos.txt")
print("└── sample_encode_decode.txt")