# ==========================================================
# Week 2 - PyTorch Training Basics
# LLM From Scratch
# ==========================================================

import os
import torch
import torch.nn as nn
import torch.nn.functional as F

# ==========================================================
# Hyperparameter
# ==========================================================

batch_size = 32
block_size = 8
max_iters = 1000
eval_interval = 100
learning_rate = 1e-2

torch.manual_seed(1337)

# ==========================================================
# Membaca Dataset
# ==========================================================

with open("data/shakespeare.txt", "r", encoding="utf-8") as f:
    text = f.read()

print("=" * 60)
print("Dataset berhasil dibaca")
print(f"Jumlah karakter : {len(text)}")
print("=" * 60)

# ==========================================================
# Vocabulary
# ==========================================================

chars = sorted(list(set(text)))
vocab_size = len(chars)

print(f"Jumlah Vocabulary : {vocab_size}")

# ==========================================================
# STOI & ITOS
# ==========================================================

stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for i, ch in enumerate(chars)}

# ==========================================================
# Encode
# ==========================================================

def encode(s):
    return [stoi[c] for c in s]

# ==========================================================
# Decode
# ==========================================================

def decode(tokens):
    return "".join([itos[i] for i in tokens])

# ==========================================================
# Mengubah Dataset menjadi Tensor
# ==========================================================

data = torch.tensor(
    encode(text),
    dtype=torch.long
)

print("\nDataset berhasil diubah menjadi Tensor")
print("Shape :", data.shape)

# ==========================================================
# Train & Validation Split
# ==========================================================

n = int(0.9 * len(data))

train_data = data[:n]
validation_data = data[n:]

print("\n===== DATASET =====")

print("Total Token      :", len(data))
print("Train Token      :", len(train_data))
print("Validation Token :", len(validation_data))

# ==========================================================
# Membuat Batch Data
# ==========================================================

def get_batch(split):

    # Memilih dataset train atau validation
    data_source = train_data if split == "train" else validation_data

    # Mengambil index secara acak
    ix = torch.randint(
        len(data_source) - block_size,
        (batch_size,)
    )

    # Input
    x = torch.stack([
        data_source[i:i + block_size]
        for i in ix
    ])

    # Target (geser satu token)
    y = torch.stack([
        data_source[i + 1:i + block_size + 1]
        for i in ix
    ])

    return x, y


# ==========================================================
# Contoh Batch
# ==========================================================

x, y = get_batch("train")

print("\n========== BATCH ==========")

print("\nInput (x)")
print(x)

print("\nTarget (y)")
print(y)

print("\nShape x :", x.shape)
print("Shape y :", y.shape)


# ==========================================================
# Membuat Folder Output
# ==========================================================

os.makedirs("Week2/output", exist_ok=True)


# ==========================================================
# Simpan Statistik Dataset
# ==========================================================

with open("Week2/output/train_stats.txt", "w", encoding="utf-8") as f:

    f.write("========== DATASET ==========\n\n")

    f.write(f"Total Token      : {len(data)}\n")
    f.write(f"Train Token      : {len(train_data)}\n")
    f.write(f"Validation Token : {len(validation_data)}\n\n")

    f.write("========== HYPERPARAMETER ==========\n\n")

    f.write(f"Vocabulary : {vocab_size}\n")
    f.write(f"Batch Size : {batch_size}\n")
    f.write(f"Block Size : {block_size}\n")
    f.write(f"Learning Rate : {learning_rate}\n")
    f.write(f"Max Iteration : {max_iters}\n")


# ==========================================================
# Simpan Informasi Tensor
# ==========================================================

with open("Week2/output/tensor_info.txt", "w", encoding="utf-8") as f:

    f.write("========== INPUT ==========\n\n")

    f.write(str(x))

    f.write("\n\nShape x : ")

    f.write(str(x.shape))

    f.write("\n\n")

    f.write("========== TARGET ==========\n\n")

    f.write(str(y))

    f.write("\n\nShape y : ")

    f.write(str(y.shape))

print("\nOutput train_stats.txt berhasil dibuat.")
print("Output tensor_info.txt berhasil dibuat.")

# ==========================================================
# Bigram Language Model
# ==========================================================

class BigramLanguageModel(nn.Module):

    def __init__(self, vocab_size):
        super().__init__()

        # Setiap token memiliki peluang untuk token berikutnya
        self.token_embedding_table = nn.Embedding(
            vocab_size,
            vocab_size
        )

    def forward(self, idx, targets=None):

        # Mengubah token ID menjadi logits
        logits = self.token_embedding_table(idx)

        # Jika hanya ingin prediksi
        if targets is None:
            loss = None

        # Jika sedang training
        else:

            B, T, C = logits.shape

            logits = logits.view(B * T, C)
            targets = targets.view(B * T)

            loss = F.cross_entropy(
                logits,
                targets
            )

        return logits, loss

    # ======================================================
    # Generate Text
    # ======================================================

    def generate(self, idx, max_new_tokens):

        for _ in range(max_new_tokens):

            logits, loss = self(idx)

            # Ambil token terakhir
            logits = logits[:, -1, :]

            # Ubah menjadi probabilitas
            probs = F.softmax(logits, dim=-1)

            # Ambil token berikutnya
            next_token = torch.multinomial(
                probs,
                num_samples=1
            )

            # Gabungkan ke input
            idx = torch.cat(
                (idx, next_token),
                dim=1
            )

        return idx


# ==========================================================
# Membuat Model
# ==========================================================

model = BigramLanguageModel(vocab_size)

print("\n========== MODEL ==========")
print(model)


# ==========================================================
# Test Forward
# ==========================================================

logits, loss = model(x, y)

print("\n========== FORWARD ==========")

print("Shape Logits :", logits.shape)

print("Loss Awal :", loss.item())

# ==========================================================
# Optimizer
# ==========================================================

optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=learning_rate
)

print("\nOptimizer berhasil dibuat.")


# ==========================================================
# Training Loop
# ==========================================================

print("\n========== TRAINING ==========\n")

loss_history = []

for step in range(max_iters):

    # Ambil batch
    xb, yb = get_batch("train")

    # Forward
    logits, loss = model(xb, yb)

    # Reset gradient
    optimizer.zero_grad()

    # Backpropagation
    loss.backward()

    # Update parameter
    optimizer.step()

    # Simpan loss setiap eval_interval
    if step % eval_interval == 0:

        print(f"Step {step:4d} | Loss = {loss.item():.4f}")

        loss_history.append(
            (step, loss.item())
        )


print("\nTraining selesai.")


# ==========================================================
# Simpan Loss
# ==========================================================

with open("Week2/output/loss_log.txt", "w", encoding="utf-8") as f:

    f.write("Step\tLoss\n")

    for step, loss_value in loss_history:

        f.write(f"{step}\t{loss_value:.4f}\n")

print("loss_log.txt berhasil dibuat.")


# ==========================================================
# Generate Sample Text
# ==========================================================

context = torch.zeros((1, 1), dtype=torch.long)

generated = decode(

    model.generate(

        context,

        max_new_tokens=300

    )[0].tolist()

)

print("\n========== GENERATED TEXT ==========\n")

print(generated)

with open(
    "Week2/output/generated_sample.txt",
    "w",
    encoding="utf-8"
) as f:

    f.write(generated)

print("\ngenerated_sample.txt berhasil dibuat.")


# ==========================================================
# Informasi Akhir
# ==========================================================

print("\n" + "=" * 60)
print("           WEEK 2 SELESAI")
print("=" * 60)

print("\nFile Output:")

print("✔ train_stats.txt")
print("✔ tensor_info.txt")
print("✔ loss_log.txt")
print("✔ generated_sample.txt")