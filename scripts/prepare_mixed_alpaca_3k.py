import json
import random
from pathlib import Path

SEED = 43
random.seed(SEED)

DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"

RAW_FILES = {
    "en": RAW_DIR / "alpaca_gpt4_data_en.json",
    "zh": RAW_DIR / "alpaca_gpt4_data_zh.json",
}

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize_item(item, lang):
    instruction = str(item.get("instruction", "")).strip()
    input_text = str(item.get("input", "")).strip()
    output = str(item.get("output", "")).strip()

    if not instruction or not output:
        return None

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
    en_raw = load_json(RAW_FILES["en"])
    zh_raw = load_json(RAW_FILES["zh"])

    en_data = [normalize_item(x, "en") for x in en_raw]
    zh_data = [normalize_item(x, "zh") for x in zh_raw]

    en_data = [x for x in en_data if x is not None]
    zh_data = [x for x in zh_data if x is not None]

    random.shuffle(en_data)
    random.shuffle(zh_data)

    train_en = en_data[:1500]
    train_zh = zh_data[:1500]

    eval_en = en_data[1500:1550]
    eval_zh = zh_data[1500:1550]

    train_data = train_en + train_zh
    eval_data = eval_en + eval_zh

    random.shuffle(train_data)
    random.shuffle(eval_data)

    with open(DATA_DIR / "train_3k.json", "w", encoding="utf-8") as f:
        json.dump(train_data, f, ensure_ascii=False, indent=2)

    with open(DATA_DIR / "eval_3k.json", "w", encoding="utf-8") as f:
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
        "filter_rule": "remove empty instruction/output and samples with total_len > 1800",
        "fields": ["instruction", "input", "output", "lang"],
    }

    with open(DATA_DIR / "dataset_stats_3k.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(json.dumps(stats, ensure_ascii=False, indent=2))
    print("[Done] Saved data/train_3k.json and data/eval_3k.json")

if __name__ == "__main__":
    main()
