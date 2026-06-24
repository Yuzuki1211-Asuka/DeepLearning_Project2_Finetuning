import json
import gc
from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel


BASE_MODEL_PATH = "models/Qwen2.5-0.5B"
LORA_ADAPTER_PATH = "results/qwen2.5-0.5b-lora-mixed-3k"
PROMPT_FILE = "examples/test_prompts.json"

OUT_JSON = "results/output_comparison_3k.json"
OUT_MD = "results/output_comparison_3k.md"


def build_prompt(example):
    instruction = example["instruction"].strip()
    input_text = example.get("input", "").strip()

    if input_text:
        return (
            "### Instruction:\n"
            f"{instruction}\n\n"
            "### Input:\n"
            f"{input_text}\n\n"
            "### Response:\n"
        )
    else:
        return (
            "### Instruction:\n"
            f"{instruction}\n\n"
            "### Response:\n"
        )


def clean_response(text):
    # 防止模型继续生成新的 instruction block
    stop_markers = [
        "\n### Instruction:",
        "\n### Input:",
        "\nInstruction:",
        "\nInput:"
    ]
    for marker in stop_markers:
        if marker in text:
            text = text.split(marker)[0]
    return text.strip()


@torch.inference_mode()
def generate_one(model, tokenizer, prompt, max_new_tokens=180):
    device = next(model.parameters()).device
    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    output_ids = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=False,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id,
    )

    full_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    # 去掉 prompt，只保留模型新生成的内容
    if full_text.startswith(prompt):
        response = full_text[len(prompt):]
    else:
        response = full_text

    return clean_response(response)


def load_base_model():
    tokenizer = AutoTokenizer.from_pretrained(
        BASE_MODEL_PATH,
        trust_remote_code=True,
        local_files_only=True,
    )

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_PATH,
        trust_remote_code=True,
        local_files_only=True,
        dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto",
    )
    model.eval()
    return model, tokenizer


def unload_model(model):
    del model
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def main():
    Path("results").mkdir(exist_ok=True)

    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        test_prompts = json.load(f)

    results = []

    print("Loading base model...")
    base_model, tokenizer = load_base_model()

    print("Generating base model outputs...")
    base_outputs = []
    for i, ex in enumerate(test_prompts):
        prompt = build_prompt(ex)
        print(f"[Base] {i + 1}/{len(test_prompts)} {ex.get('category', '')}")
        base_outputs.append(generate_one(base_model, tokenizer, prompt))

    unload_model(base_model)

    print("Loading fine-tuned LoRA model...")
    ft_model, tokenizer = load_base_model()
    ft_model = PeftModel.from_pretrained(
        ft_model,
        LORA_ADAPTER_PATH,
        local_files_only=True,
    )
    ft_model.eval()

    print("Generating fine-tuned model outputs...")
    ft_outputs = []
    for i, ex in enumerate(test_prompts):
        prompt = build_prompt(ex)
        print(f"[Fine-tuned] {i + 1}/{len(test_prompts)} {ex.get('category', '')}")
        ft_outputs.append(generate_one(ft_model, tokenizer, prompt))

    unload_model(ft_model)

    for ex, base_out, ft_out in zip(test_prompts, base_outputs, ft_outputs):
        results.append({
            "category": ex.get("category", ""),
            "instruction": ex["instruction"],
            "input": ex.get("input", ""),
            "base_model_output": base_out,
            "fine_tuned_model_output": ft_out,
        })

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("# Base Model vs Fine-tuned Model Output Comparison\n\n")
        f.write("- Base model: Qwen2.5-0.5B\n")
        f.write("- Fine-tuned model: Qwen2.5-0.5B + LoRA adapter trained on mixed 1K Alpaca-style data\n\n")

        for idx, r in enumerate(results, 1):
            f.write(f"## Example {idx}: {r['category']}\n\n")
            f.write("### Instruction\n\n")
            f.write(r["instruction"] + "\n\n")

            if r["input"]:
                f.write("### Input\n\n")
                f.write("```text\n" + r["input"] + "\n```\n\n")

            f.write("### Base model output\n\n")
            f.write("```text\n" + r["base_model_output"] + "\n```\n\n")

            f.write("### Fine-tuned model output\n\n")
            f.write("```text\n" + r["fine_tuned_model_output"] + "\n```\n\n")

            f.write("### Analysis\n\n")
            f.write("TODO: 在这里分析微调前后输出的差异，例如指令遵循、语言质量、是否跑题、是否有事实错误或推理错误。\n\n")
            f.write("---\n\n")

    print(f"Saved JSON to {OUT_JSON}")
    print(f"Saved Markdown to {OUT_MD}")


if __name__ == "__main__":
    main()
