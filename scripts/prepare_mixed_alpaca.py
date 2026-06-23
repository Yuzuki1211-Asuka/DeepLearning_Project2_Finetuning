import json
import random
import urllib.request
from pathlib import Path


SEED = 42
random.seed(SEED)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

RAW_DIR = DATA_DIR / "raw"
RAW_DIR.mkdir(exist_ok=True)

# GPT-4-LLM Alpaca-GPT4 English and Chinese data
URLS = {
    "en": "https://raw.githubusercontent.com/Instruction-Tuning-with-GPT-4/GPT-4-LLM/main/data/alpaca_gpt4_data.json",
    "zh": "https://raw.githubusercontent.com/Instruction-Tuning-with-GPT-4/GPT-4-LLM/main/data/alpaca_gpt4_data_zh.json",
}

RAW_FILES = {
    "en": RAW_DIR / "alpaca_gpt4_data_en.json",
    "zh": RAW_DIR / "alpaca_gpt4_data_zh.json",
}


def download_if_needed(lang):
    path = RAW_FILES[lang]
    if path.exists():
        print(f"[OK] {path} already exists")
        return

    url = URLS[lang]
    print(f"[Download] {lang}: {url}")
    urllib.request.urlretrieve(url, path)
    print(f"[Saved] {path}")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_item(item, lang):
    instruction = str(item.get("instruction", "")).strip()
    input_text = str(item.get("input", "")).strip()
    output = str(item.get("output", "")).strip()

    if not instruction or not output:
        return None

    # 简单过滤太长样本，避免第一次正式训练太慢
    total_len = len(instruction) + len(input_text) + len(output)
    if total_len > 1800:
        return None

    return {
        "instruction": instruction,
        "input": input_text,
        "output": output,
        "lang": lang,
    }


def main():
    for lang in ["en", "zh"]:
        download_if_needed(lang)

    en_raw = load_json(RAW_FILES["en"])
    zh_raw = load_json(RAW_FILES["zh"])

    en_data = [normalize_item(x, "en") for x in en_raw]
    zh_data = [normalize_item(x, "zh") for x in zh_raw]

    en_data = [x for x in en_data if x is not None]
    zh_data = [x for x in zh_data if x is not None]

    random.shuffle(en_data)
    random.shuffle(zh_data)

    # 第一次正式实验：1000 train + 50 eval
    train_en = en_data[:500]
    train_zh = zh_data[:500]

    eval_en = en_data[500:525]
    eval_zh = zh_data[500:525]

    train_data = train_en + train_zh
    eval_data = eval_en + eval_zh

    random.shuffle(train_data)
    random.shuffle(eval_data)

    with open(DATA_DIR / "train.json", "w", encoding="utf-8") as f:
        json.dump(train_data, f, ensure_ascii=False, indent=2)

    with open(DATA_DIR / "eval.json", "w", encoding="utf-8") as f:
        json.dump(eval_data, f, ensure_ascii=False, indent=2)

    stats = {
        "source": "GPT-4-LLM Alpaca-GPT4 English + Chinese",
        "train_total": len(train_data),
        "train_en": len(train_en),
        "train_zh": len(train_zh),
        "eval_total": len(eval_data),
        "eval_en": len(eval_en),
        "eval_zh": len(eval_zh),
        "seed": SEED,
        "fields": ["instruction", "input", "output", "lang"],
    }

    with open(DATA_DIR / "dataset_stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(json.dumps(stats, ensure_ascii=False, indent=2))
    print("[Done] Saved data/train.json and data/eval.json")


if __name__ == "__main__":
    main()
