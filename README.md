# DeepLearning Project 2: Instruction Fine-tuning

本项目为深度学习课程 Project 2，选择 **任务 A：Instruction Fine-tuning 实践**。

本项目参考 Stanford Alpaca 的 instruction tuning 思路，使用 `Qwen2.5-0.5B` 作为 base model，构造中英文混合 Alpaca-style instruction 数据集，并采用 LoRA 方法进行小规模监督微调。项目内容包括数据处理、prompt template 构造、LoRA 微调、训练过程记录、loss 曲线绘制、显存监控，以及 base model 与 fine-tuned model 的输出对比分析。

## 1. 小组信息

| 成员         | 分工                              |
| ---------- | ------------------------------- |
| 2024214749 杨子木 | 环境配置、模型下载、LoRA 训练、训练日志整理        |
| 2024214709 申婧 | 数据集整理、prompt template 设计、测试指令设计 |
| 2024214739 康馨文 | 推理结果分析、失败案例分析、报告撰写              |

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
├── README.md
├── requirements.txt
├── train_lora.py
├── inference_compare.py
├── configs/
│   └── train_config.yaml
├── data/
│   ├── train.json
│   ├── eval.json
│   ├── dataset_stats.json
│   ├── train_3k.json
│   ├── eval_3k.json
│   └── dataset_stats_3k.json
├── examples/
│   └── test_prompts.json
├── scripts/
│   ├── prepare_mixed_alpaca.py
│   ├── prepare_mixed_alpaca_3k.py
│   └── plot_loss_any.py
├── results/
│   ├── training_log_mixed_1k.txt
│   ├── train_time_mixed_1k.txt
│   ├── gpu_summary_mixed_1k.txt
│   ├── gpu_usage_mixed_1k.csv
│   ├── loss_curve_mixed_1k.png
│   ├── output_comparison.md
│   ├── output_comparison.json
│   ├── run_summary_mixed_1k.md
│   ├── training_log_mixed_3k.txt
│   ├── train_time_mixed_3k.txt
│   ├── gpu_summary_mixed_3k.txt
│   ├── gpu_usage_mixed_3k.csv
│   ├── loss_curve_mixed_3k.png
│   ├── output_comparison_3k.md
│   ├── output_comparison_3k.json
│   └── run_summary_mixed_3k.md
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

## 6. 数据集

本项目使用 GPT-4-LLM Alpaca-GPT4 English 和 Chinese 数据集中的 Alpaca-style instruction-following 数据。为了支持中英文混合指令微调，我们分别从英文数据和中文数据中采样，并构造了中英文比例均衡的混合训练集。

每条样本包含以下字段：

| 字段            | 含义                           |
| ------------- | ---------------------------- |
| `instruction` | 用户指令或任务描述                    |
| `input`       | 可选输入内容，部分任务为空                |
| `output`      | 期望模型生成的回答                    |
| `lang`        | 语言标记，`en` 表示英文样本，`zh` 表示中文样本 |

本项目共进行了两组不同数据规模的实验：

| 实验设置     | 训练样本数 | 英文训练样本数 | 中文训练样本数 | 验证样本数 |
| -------- | ----: | ------: | ------: | ----: |
| Mixed 1K |  1000 |     500 |     500 |    50 |
| Mixed 3K |  3000 |    1500 |    1500 |   100 |

其中，Mixed 1K 的验证集包含 25 条英文样本和 25 条中文样本；Mixed 3K 的验证集包含 50 条英文样本和 50 条中文样本。

数据预处理过程中，我们采用了以下清洗规则：

* 删除 `instruction` 或 `output` 为空的样本；
* 删除总长度过长的样本，即 `len(instruction) + len(input) + len(output) > 1800` 的样本；
* 保持英文和中文样本数量均衡；
* 将所有样本转换为 Alpaca-style prompt-response 格式。

数据预处理脚本如下：

```bash
python scripts/prepare_mixed_alpaca.py
python scripts/prepare_mixed_alpaca_3k.py
```

处理后的数据文件如下：

```text
data/train.json
data/eval.json
data/train_3k.json
data/eval_3k.json
data/dataset_stats.json
data/dataset_stats_3k.json
```

由于原始数据文件较大，`data/raw/` 目录未上传到 GitHub 仓库。

## 7. Prompt Template

本项目采用 Alpaca-style prompt template 构造训练样本。对于包含 `input` 字段的样本，prompt 格式如下：

```text
### Instruction:
{instruction}

### Input:
{input}

### Response:
{output}
```

对于不包含 `input` 字段的样本，prompt 格式如下：

```text
### Instruction:
{instruction}

### Response:
{output}
```

训练时，模型学习在 `### Response:` 之后生成符合指令要求的回答。该格式能够帮助 base model 学习 instruction-response 形式的交互方式，使其更接近指令遵循模型。

## 8. 训练方法

本项目使用 Qwen2.5-0.5B 作为 base model，并采用 LoRA 进行参数高效微调。LoRA 方法保持原始模型权重冻结，只训练额外插入的低秩适配器参数，从而降低训练成本和显存需求。

本实验的 LoRA target modules 包括：

```text
q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj
```

主要训练超参数如下：

| 超参数                         |           数值 |
| --------------------------- | -----------: |
| Base model                  | Qwen2.5-0.5B |
| 微调方法                        |         LoRA |
| Max sequence length         |          512 |
| Epochs                      |            2 |
| Per-device train batch size |            2 |
| Gradient accumulation steps |            8 |
| Effective batch size        |           16 |
| Learning rate               |         2e-4 |
| LoRA r                      |            8 |
| LoRA alpha                  |           16 |
| LoRA dropout                |         0.05 |

LoRA 可训练参数量如下：

```text
Trainable params: 4,399,104
All params: 498,431,872
Trainable percentage: 0.8826%
```

为了保证 Mixed 1K 和 Mixed 3K 实验具有可比性，两组实验使用相同的 base model、LoRA 配置、batch size、learning rate、max sequence length 和 epoch 数。两组实验的主要区别仅在于训练样本规模不同。

## 9. 实验结果

本项目共完成了 Mixed 1K 和 Mixed 3K 两组 LoRA instruction fine-tuning 实验。主要训练结果如下：

| 实验设置                 |  Mixed 1K |    Mixed 3K |
| -------------------- | --------: | ----------: |
| 训练样本数                |      1000 |        3000 |
| 英文 / 中文训练样本数         | 500 / 500 | 1500 / 1500 |
| 验证样本数                |        50 |         100 |
| Epochs               |         2 |           2 |
| Effective batch size |        16 |          16 |
| Learning rate        |      2e-4 |        2e-4 |
| Final train_loss     |     1.576 |       1.602 |
| Trainer runtime      |   118.7 s |     355.8 s |
| Wall time            |     129 s |       367 s |
| Peak GPU memory      |   5650 MB |     5650 MB |
| Peak GPU utilization |       43% |         44% |

实验结果显示，当训练样本数从 1000 增加到 3000 时，总训练时间明显增加。Mixed 3K 的 wall time 为 367 秒，约为 Mixed 1K 的 2.84 倍，基本符合训练数据量增加带来的时间增长趋势。

两组实验的峰值显存均为 5650 MB。这说明在模型规模、batch size、max sequence length 和 LoRA 配置保持不变的情况下，训练样本总数主要影响训练步数和总耗时，而不会明显增加单步训练的峰值显存占用。

Mixed 3K 的 final train_loss 为 1.602，略高于 Mixed 1K 的 1.576。该结果不能简单理解为 3K 模型效果更差，因为 3K 数据包含更多样化的中英文 instruction 样本，任务分布更复杂。因此，模型效果需要结合推理输出结果进行综合分析，而不能只依赖训练 loss 数值。

重要结果文件如下：

```text
results/loss_curve_mixed_1k.png
results/loss_curve_mixed_3k.png
results/run_summary_mixed_1k.md
results/run_summary_mixed_3k.md
results/training_log_mixed_1k.txt
results/training_log_mixed_3k.txt
results/gpu_summary_mixed_1k.txt
results/gpu_summary_mixed_3k.txt
```

## 10. 推理输出对比

为了评估 instruction fine-tuning 的实际效果，我们设计了 10 条测试指令，覆盖中文问答、英译中、中译英、总结、代码解释、数学推理、逻辑判断、英文问答和日常助手等任务类型。我们分别比较了 base model、Mixed 1K fine-tuned model 和 Mixed 3K fine-tuned model 的输出表现。

完整输出对比结果保存在以下文件中：

```text
results/output_comparison.md
results/output_comparison_3k.md
```

主要观察结果如下：

* Base model 经常将 prompt 当作普通文本续写，而不是执行用户指令。例如在翻译任务中，base model 直接复制输入文本，没有进行翻译。
* Mixed 1K fine-tuned model 在指令遵循能力上有明显提升，尤其是在翻译任务和简单数学任务中，能够更好地按照指令生成回答。
* Mixed 3K fine-tuned model 在日常助手类任务中表现更好，例如邮件写作任务中，回答更加自然、礼貌，结构也更加完整。
* 但是 Mixed 3K 并不是在所有任务上都优于 Mixed 1K。它在部分翻译任务中出现了重复生成、过长解释和截断问题。
* 在数学推理任务中，Mixed 3K 模型将“打八折”错误计算为 `200 * (1 - 0.80) = 40`，而正确答案应为 `200 * 0.8 = 160`。
* 在逻辑判断任务中，base model 和 fine-tuned model 都仍然存在明显不足，说明小规模 instruction fine-tuning 无法显著提升复杂逻辑推理能力。

总体来看，LoRA instruction fine-tuning 能够明显改善模型的指令遵循能力、回答格式和助手风格。但是，这种提升主要体现在“如何回答”上，而不是全面提升模型的数学推理、逻辑判断或代码理解能力。对于 Qwen2.5-0.5B 这样的小模型，模型能力仍然受到 base model 本身能力、训练数据质量和生成策略的限制。



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

