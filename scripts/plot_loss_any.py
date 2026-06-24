import ast
import re
import argparse
from pathlib import Path
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--log", required=True)
parser.add_argument("--out", required=True)
parser.add_argument("--title", default="LoRA Fine-tuning Loss Curve")
args = parser.parse_args()

text = Path(args.log).read_text(encoding="utf-8", errors="ignore")
ansi_escape = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
text = ansi_escape.sub("", text)

losses = []
epochs = []

for match in re.finditer(r"\{[^{}]*\}", text):
    s = match.group(0)
    if "'loss'" not in s and '"loss"' not in s:
        continue
    if "train_loss" in s:
        continue
    try:
        d = ast.literal_eval(s)
    except Exception:
        continue
    if "loss" in d and "epoch" in d:
        losses.append(float(d["loss"]))
        epochs.append(float(d["epoch"]))

print("Found loss records:", len(losses))
print("Losses:", losses)

if not losses:
    raise SystemExit("No loss records found.")

plt.figure(figsize=(8, 5))
plt.plot(epochs, losses, marker="o")
plt.xlabel("Epoch")
plt.ylabel("Training Loss")
plt.title(args.title)
plt.grid(True)
plt.savefig(args.out, dpi=300, bbox_inches="tight")
print(f"Saved to {args.out}")
