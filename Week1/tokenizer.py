# Membaca dataset
with open("data/shakespeare.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Membuat vocabulary karakter unik
chars = sorted(list(set(text)))

# Menampilkan vocabulary
print("Vocabulary:")
print(chars)

print("\nJumlah Vocabulary:", len(chars))

# Membuat STOI mapping karakter -> angka
stoi = {ch: i for i, ch in enumerate(chars)} 

# Membuat ITOS mapping angka -> karakter
itos = {i: ch for i, ch in enumerate(chars)}

print("\nSTOI:")
print(stoi)

print("\nITOS:")
print(itos)

# Fungsi encode
def encode(text):
    return [stoi[c] for c in text]

# Fungsi decode
def decode(tokens):
    return "".join([itos[i] for i in tokens])

# Contoh penggunaan
contoh = "To be"

encoded = encode(contoh)
print("\nHasil Encode:")
print(encoded)

decoded = decode(encoded)
print("\nHasil Decode:")
print(decoded)