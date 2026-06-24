# Training Summary: Qwen2.5-0.5B LoRA Mixed 3K

## Model
- Base model: Qwen2.5-0.5B
- Fine-tuning method: LoRA

## Dataset
- Dataset type: Alpaca-style instruction data
- Source: GPT-4-LLM Alpaca-GPT4 English + Chinese
- Train samples: 3000
- English train samples: 1500
- Chinese train samples: 1500
- Eval samples: 100
- English eval samples: 50
- Chinese eval samples: 50

## Hyperparameters
- Epochs: 2
- Max sequence length: 512
- Per-device train batch size: 2
- Gradient accumulation steps: 8
- Effective batch size: 16
- Learning rate: 0.0002
- LoRA r: 8
- LoRA alpha: 16
- LoRA dropout: 0.05

## Training Result
- Final train_loss: 1.602
- Trainer train_runtime: 355.8 seconds
- Wall time: 367 seconds

## GPU Usage
- GPU: NVIDIA GeForce RTX 5090
- Peak memory used: 5650 MB
- Total GPU memory: 32607 MB
- Peak GPU utilization: 44%

## Output
- LoRA adapter path: results/qwen2.5-0.5b-lora-mixed-3k
- Training log: results/training_log_mixed_3k.txt
- GPU usage CSV: results/gpu_usage_mixed_3k.csv
