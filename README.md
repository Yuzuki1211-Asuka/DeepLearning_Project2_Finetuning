# DeepLearning Project2: Instruction Fine-tuning

本项目为深度学习课程 Project 2，选择任务 A：Instruction Fine-tuning 实践。

本项目使用 Qwen2.5-0.5B 作为 base model，采用 LoRA 方法，在中英文混合 Alpaca-style instruction 数据集上进行小规模监督微调。

## Current Results

- Base model: Qwen2.5-0.5B
- Fine-tuning method: LoRA
- Training samples: 1000
  - English: 500
  - Chinese: 500
- Epochs: 2
- Final train_loss: 1.576
- Training wall time: 129 seconds
- GPU: NVIDIA GeForce RTX 5090
- Peak GPU memory: 5650 MB

## Repository Structure

- `train_lora.py`: LoRA training script
- `inference_compare.py`: base model vs fine-tuned model inference comparison
- `configs/train_config.yaml`: training configuration
- `scripts/`: data preparation, GPU monitor, loss plotting scripts
- `data/`: processed Alpaca-style train/eval data
- `examples/test_prompts.json`: test instructions
- `results/`: training logs, loss curve, output comparison, GPU summary
- `report/`: final report files

## Notes

完整 base model 权重未上传到 GitHub。模型可从 ModelScope 下载。LoRA adapter 是否上传取决于仓库设置。
