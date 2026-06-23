# DeepLearning Project 2: Instruction Fine-tuning

本项目为深度学习课程 Project 2，选择 **任务 A：Instruction Fine-tuning 实践**。

本项目参考 Stanford Alpaca 的 instruction tuning 思路，使用 `Qwen2.5-0.5B` 作为 base model，构造中英文混合 Alpaca-style instruction 数据集，并采用 LoRA 方法进行小规模监督微调。项目内容包括数据处理、prompt template 构造、LoRA 微调、训练过程记录、loss 曲线绘制、显存监控，以及 base model 与 fine-tuned model 的输出对比分析。

## 1. 小组信息

| 成员         | 分工                              |
| ---------- | ------------------------------- |
| TODO: 成员 1 | 环境配置、模型下载、LoRA 训练、训练日志整理        |
| TODO: 成员 2 | 数据集整理、prompt template 设计、测试指令设计 |
| TODO: 成员 3 | 推理结果分析、失败案例分析、报告撰写              |
| TODO: 成员 4 | GitHub 仓库整理、README、最终材料检查       |

本组选择的任务为：

```text
任务 A：Instruction Fine-tuning 实践
```

---

## 2. 项目目标

本项目的目标是完成一个完整的小规模 instruction fine-tuning 实验流程，包括：

1. 理解 Alpaca-style instruction 数据格式；
2. 构造 instruction prompt template；
3. 选择合适的小型开源 base model；
4. 使用 LoRA 进行参数高效 instruction fine-tuning；
5. 记录训练过程，包括主要超参数、训练 loss、训练时间和显存占用；
6. 对比 base model 和 fine-tuned model 在若干测试指令上的输出；
7. 分析 fine-tuning 后模型能力的变化、提升、不足和失败案例；
8. 整理代码、配置、日志、实验结果和最终报告。

---

## 3. Repository Structure

```text
.
├── README.md
├── requirements.txt
├── train_lora.py
├── inference_compare.py
├── configs/
│   └── train_config.yaml
├── data/
│   ├── train.json
│   ├── eval.json
│   └── dataset_stats.json
├── examples/
│   └── test_prompts.json
├── scripts/
│   ├── prepare_mixed_alpaca.py
│   ├── monitor_gpu.py
│   └── plot_loss.py
├── results/
│   ├── training_log_mixed_1k.txt
│   ├── train_time_mixed_1k.txt
│   ├── gpu_summary_mixed_1k.txt
│   ├── gpu_usage_mixed_1k.csv
│   ├── loss_curve_mixed_1k.png
│   ├── output_comparison.md
│   ├── output_comparison.json
│   └── run_summary_mixed_1k.md
└── report/
    └── project_report.pdf
```

说明：

* `train_lora.py`：LoRA 微调训练脚本；
* `inference_compare.py`：base model 与 fine-tuned model 输出对比脚本；
* `configs/train_config.yaml`：训练配置文件；
* `scripts/prepare_mixed_alpaca.py`：中英文混合数据集构造脚本；
* `scripts/monitor_gpu.py`：显存监控脚本；
* `scripts/plot_loss.py`：loss 曲线绘制脚本；
* `examples/test_prompts.json`：测试指令文件；
* `results/output_comparison.md`：微调前后输出对比结果；
* `results/loss_curve_mixed_1k.png`：训练 loss 曲线；
* `report/project_report.pdf`：最终报告。

---

## 4. Environment

本实验在 AutoDL 云平台上完成，主要实验环境如下：

| 项目                    | 配置                      |
| --------------------- | ----------------------- |
| GPU                   | NVIDIA GeForce RTX 5090 |
| GPU Memory            | 32607 MB                |
| PyTorch               | 2.8.0 + CUDA 12.8       |
| Transformers          | 5.12.1                  |
| Fine-tuning Framework | Transformers + PEFT     |
| Fine-tuning Method    | LoRA                    |

安装依赖：

```bash
pip install -r requirements.txt
```


---

## 5. Model

本实验使用：

```text
Qwen2.5-0.5B
```

作为 base model。


模型下载方式：

```python
from modelscope import snapshot_download

model_dir = snapshot_download(
    model_id="Qwen/Qwen2.5-0.5B",
    local_dir="models/Qwen2.5-0.5B"
)
```

注意：完整 base model 权重没有上传到 GitHub。需要复现实验时，请根据上述方式自行下载模型。

---

## 6. Dataset

### 6.1 使用的数据集

本实验使用中英文混合的 Alpaca-style instruction 数据，数据来源为：

```text
GPT-4-LLM Alpaca-GPT4 English + Chinese
```

我们分别从英文 Alpaca-GPT4 数据和中文 Alpaca-GPT4 数据中抽取样本，构造中英文混合训练集和验证集。

数据处理脚本为：

```bash
python scripts/prepare_mixed_alpaca.py
```

处理后生成：

```text
data/train.json
data/eval.json
data/dataset_stats.json
```

### 6.2 数据字段含义

每条样本包含以下字段：

| 字段            | 含义                           |
| ------------- | ---------------------------- |
| `instruction` | 用户希望模型完成的任务说明                |
| `input`       | 完成任务所需的额外输入，可以为空             |
| `output`      | 期望模型生成的标准回答                  |
| `lang`        | 样本语言，`en` 表示英文样本，`zh` 表示中文样本 |

样例：

```json
{
  "instruction": "请解释什么是过拟合。",
  "input": "",
  "output": "过拟合是指模型在训练数据上表现很好，但在未见过的数据上表现较差的现象。",
  "lang": "zh"
}
```

### 6.3 Prompt 构造方式

本实验采用 Alpaca-style prompt template。

当 `input` 为空时，prompt 构造为：

```text
### Instruction:
{instruction}

### Response:
{output}
```

当 `input` 不为空时，prompt 构造为：

```text
### Instruction:
{instruction}

### Input:
{input}

### Response:
{output}
```

在推理阶段，只提供 `instruction` 和可选的 `input`，让模型从 `### Response:` 后开始生成回答。

### 6.4 训练集和测试集划分

本实验共构造：

| 数据集   | 总样本数 | 英文样本数 | 中文样本数 |
| ----- | ---: | ----: | ----: |
| Train | 1000 |   500 |   500 |
| Eval  |   50 |    25 |    25 |

具体划分方式如下：

1. 分别读取英文 Alpaca-GPT4 数据和中文 Alpaca-GPT4 数据；
2. 对两种语言的数据分别打乱；
3. 从英文数据中抽取 500 条作为训练样本，25 条作为验证样本；
4. 从中文数据中抽取 500 条作为训练样本，25 条作为验证样本；
5. 合并英文和中文样本后再次打乱，得到最终的 `data/train.json` 和 `data/eval.json`。

随机种子设置为：

```text
42
```

以保证数据划分可复现。

### 6.5 数据清洗和筛选

本实验进行了简单的数据清洗和筛选：

1. 去除 `instruction` 为空的样本；
2. 去除 `output` 为空的样本；
3. 去除过长样本，具体规则为：

```text
len(instruction) + len(input) + len(output) > 1800
```

超过该长度的样本会被过滤掉，以避免第一次正式训练过慢或显存压力过大。

最终保留字段：

```text
instruction
input
output
lang
```

数据统计结果保存在：

```text
data/dataset_stats.json
```


---

## 7. Fine-tuning Method

本实验使用 LoRA 进行参数高效微调。

LoRA 的基本思想是在保持原始模型参数冻结的情况下，为部分线性层加入低秩可训练矩阵。训练过程中只更新这些 LoRA 参数，而不是更新完整模型参数。

本实验对以下模块加入 LoRA：

```text
q_proj
k_proj
v_proj
o_proj
gate_proj
up_proj
down_proj
```

LoRA 参数设置如下：

| 参数           |   数值 |
| ------------ | ---: |
| LoRA r       |    8 |
| LoRA alpha   |   16 |
| LoRA dropout | 0.05 |

训练过程中参数统计如下：

| 项目                   |          数值 |
| -------------------- | ----------: |
| Total parameters     | 498,431,872 |
| Trainable parameters |   4,399,104 |
| Trainable ratio      |     0.8826% |

可以看到，本实验只训练不到 1% 的模型参数，体现了 LoRA 参数高效微调的特点。

---

## 8. Training Configuration

训练配置文件为：

```text
configs/train_config.yaml
```

主要配置如下：

```yaml
model_name: models/Qwen2.5-0.5B
train_file: data/train.json
output_dir: results/qwen2.5-0.5b-lora-mixed-1k

max_seq_length: 512
num_train_epochs: 2
per_device_train_batch_size: 2
gradient_accumulation_steps: 8
learning_rate: 0.0002
logging_steps: 10
save_steps: 100

lora_r: 8
lora_alpha: 16
lora_dropout: 0.05
```

训练命令：

```bash
python train_lora.py 2>&1 | tee results/training_log_mixed_1k.txt
```

显存监控命令：

```bash
python scripts/monitor_gpu.py \
  --interval 1 \
  --csv results/gpu_usage_mixed_1k.csv \
  --summary results/gpu_summary_mixed_1k.txt
```

---

## 9. Training Results

正式训练结果如下：

| 指标                    |                      数值 |
| --------------------- | ----------------------: |
| Final train_loss      |                   1.576 |
| Trainer train_runtime |           118.7 seconds |
| Wall time             |             129 seconds |
| GPU                   | NVIDIA GeForce RTX 5090 |
| Peak GPU memory used  |                 5650 MB |
| Total GPU memory      |                32607 MB |
| Peak GPU utilization  |                     43% |

训练日志：

```text
results/training_log_mixed_1k.txt
```

训练时间记录：

```text
results/train_time_mixed_1k.txt
```

显存记录：

```text
results/gpu_summary_mixed_1k.txt
results/gpu_usage_mixed_1k.csv
```

loss 曲线：

```text
results/loss_curve_mixed_1k.png
```

训练摘要：

```text
results/run_summary_mixed_1k.md
```

---

## 10. Inference Comparison

为了比较微调前后模型能力变化，我们设计了 10 条测试指令，覆盖以下任务类型：

1. 中文问答；
2. 英译中；
3. 中译英；
4. 总结；
5. 代码解释；
6. 数学推理；
7. 逻辑判断；
8. 英文问答；
9. 日常助手类任务。

测试指令文件：

```text
examples/test_prompts.json
```

推理对比脚本：

```text
inference_compare.py
```

运行命令：

```bash
python inference_compare.py 2>&1 | tee results/inference_compare_log.txt
```

输出结果：

```text
results/output_comparison.md
results/output_comparison.json
```

对比内容包括：

```text
Instruction
Input
Base model output
Fine-tuned model output
Analysis
```

目前 `results/output_comparison.md` 中包含每个测试样例的输出对比和分析。分析重点包括：

1. fine-tuned model 是否更符合指令；
2. 回答是否更完整、更自然；
3. 是否存在跑题、重复、乱码、答非所问；
4. 哪些任务提升明显；
5. 哪些任务仍然失败或提升有限。

---


## 11. How to Reproduce

### 11.1 Install dependencies

```bash
pip install -r requirements.txt
```

### 11.2 Download base model

```python
from modelscope import snapshot_download

snapshot_download(
    model_id="Qwen/Qwen2.5-0.5B",
    local_dir="models/Qwen2.5-0.5B"
)
```

### 11.3 Prepare dataset

```bash
python scripts/prepare_mixed_alpaca.py
```

### 11.4 Train LoRA adapter

```bash
python train_lora.py 2>&1 | tee results/training_log_mixed_1k.txt
```

### 11.5 Plot loss curve

```bash
python scripts/plot_loss.py
```

### 11.6 Run inference comparison

```bash
python inference_compare.py 2>&1 | tee results/inference_compare_log.txt
```

---

## 12. Files Not Included

为了避免 GitHub 仓库过大，本项目没有上传以下内容：

```text
models/
data/raw/
完整 base model 权重
训练中间 checkpoint
```

如果需要复现实验，请根据 README 中的说明重新下载 base model，并运行数据处理脚本生成训练数据。

TODO：如果最终上传了 LoRA adapter，请删除下面这句话；如果没有上传，则保留。

```text
当前仓库未上传 adapter_model.safetensors，仅提供训练代码、配置、日志、loss 曲线和输出对比结果。
```

---

## 13. References

1. Stanford CRFM. Alpaca: A Strong, Replicable Instruction-Following Model.
   https://crfm.stanford.edu/2023/03/13/alpaca.html

2. Hu et al. LoRA: Low-Rank Adaptation of Large Language Models.
   https://arxiv.org/abs/2106.09685

3. Hugging Face Transformers Documentation.
   https://huggingface.co/docs/transformers

4. Hugging Face PEFT Documentation.
   https://huggingface.co/docs/peft

5. Qwen Model Documentation.
   https://qwenlm.github.io/

6. GPT-4-LLM Dataset.
   https://github.com/Instruction-Tuning-with-GPT-4/GPT-4-LLM

