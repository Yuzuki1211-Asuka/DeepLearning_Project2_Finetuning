# Training Summary: Qwen2.5-0.5B LoRA Mixed 1K

## Model
- Base model: Qwen2.5-0.5B
- Fine-tuning method: LoRA
- Trainable parameters: 4,399,104
- Total parameters: 498,431,872
- Trainable ratio: 0.8826%

## Dataset
- Dataset type: Alpaca-style instruction data
- Source: GPT-4-LLM Alpaca-GPT4 English + Chinese
- Train samples: 1000
- English train samples: 500
- Chinese train samples: 500
- Eval samples: 50
- English eval samples: 25
- Chinese eval samples: 25

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
- Final train_loss: 1.576
- Trainer train_runtime: 118.7 seconds
- Wall time: 129 seconds

## GPU Usage
- GPU: NVIDIA GeForce RTX 5090
- Peak memory used: 5650 MB
- Total GPU memory: 32607 MB
- Peak GPU utilization: 43%

## Output
- LoRA adapter path: results/qwen2.5-0.5b-lora-mixed-1k
- Training log: results/training_log_mixed_1k.txt
- GPU usage CSV: results/gpu_usage_mixed_1k.csv
