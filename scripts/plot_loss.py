import ast
import re
from pathlib import Path
import matplotlib.pyplot as plt

log_path = Path("results/training_log_mixed_1k.txt")
out_path = Path("results/loss_curve_mixed_1k.png")

text = log_path.read_text(encoding="utf-8", errors="ignore")

# 去掉终端颜色/进度条控制字符
ansi_escape = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
text = ansi_escape.sub("", text)

losses = []
epochs = []
steps = []

# 从日志中提取形如 {'loss': ..., 'epoch': ...} 的字典
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
        steps.append(len(losses))

print("Found loss records:", len(losses))
print("Losses:", losses)
print("Epochs:", epochs)

if not losses:
    print("ERROR: No loss records found. Please check results/training_log_mixed_1k.txt")
    raise SystemExit(1)

plt.figure(figsize=(8, 5))
plt.plot(epochs, losses, marker="o")
plt.xlabel("Epoch")
plt.ylabel("Training Loss")
plt.title("LoRA Fine-tuning Loss Curve")
plt.grid(True)
plt.savefig(out_path, dpi=300, bbox_inches="tight")

print(f"Saved to {out_path}")
