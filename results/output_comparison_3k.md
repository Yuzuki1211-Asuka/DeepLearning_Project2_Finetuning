# Base Model vs Fine-tuned Model Output Comparison

- Base model: Qwen2.5-0.5B
- Fine-tuned model: Qwen2.5-0.5B + LoRA adapter trained on mixed 3K Alpaca-style data

## Example 1: 中文问答

### Instruction

请解释什么是过拟合。

### Base model output

```text
过拟合是指在训练数据上训练模型时，模型过于复杂，以至于无法很好地拟合训练数据，从而导致模型在测试数据上的表现不佳。具体来说，过拟合是指模型在训练数据上的表现好，但在测试数据上的表现差。这是因为过拟合是因为模型过于复杂，以至于无法很好地拟合训练数据，从而导致模型在测试数据上的表现不佳。为了防止过拟合，可以采取以下措施：1.减少模型的复杂度；2.使用正则化技术，如L1和L2正则化；3.使用交叉验证技术，以评估模型的性能并避免过拟合。
```

### Fine-tuned model output

```text
过拟合是指在训练数据集上建立的模型过于精确，以至于在测试数据集上表现不佳。换句话说，模型在训练数据集上表现良好，但在测试数据集上表现不佳。

过拟合通常发生在模型过于复杂，以至于它能够很好地拟合训练数据，但不能很好地拟合测试数据。这会导致模型在测试数据上的预测误差比在训练数据上的误差更大。

过拟合的一个常见原因就是模型过于依赖于训练数据，而忽略了测试数据。此外，过拟合还可能发生在模型的参数选择上，例如选择过多的特征，或者选择过于复杂的模型结构。

为了避免过拟合，可以采取一些措施，例如增加训练数据，使用交叉验证来评估模型的性能，或者选择更简单的模型结构。此外，还可以通过正则化来减少过拟合的影响。总之，过
```

### Analysis

微调后模型的回答结构更清晰，先给出定义再说明原因和对策，相比 base model 的重复表述（"模型过于复杂，以至于无法很好地拟合训练数据"出现多次）有明显改善。但 fine-tuned model 的回答存在准确性问题：将过拟合描述为"模型过于精确"不够准确，且文末出现"总之，过"的截断现象。此外，"过拟合的一个常见原因就是模型过于依赖于训练数据，而忽略了测试数据"这一表述也不严谨。总体来看，3K 数据微调后回答格式显著改善，但知识准确性和生成完整性仍有不足。

---

## Example 2: 中文问答

### Instruction

请用通俗的语言解释什么是梯度下降。

### Base model output

```text
梯度下降是一种优化算法，用于在低维空间中找到全局最小值。它通过不断调整参数来优化目标函数，直到找到最优解。梯度下降的基本思想是沿着最小化目标函数的方向移动，直到达到全局最小值。
```

### Fine-tuned model output

```text
梯度下降是一种优化算法，它通过不断调整参数来最小化损失函数。损失函数是用来衡量模型预测结果与真实结果之间的差异的函数。梯度下降算法通过计算损失函数的梯度，然后沿着梯度的方向调整参数，以最小化损失函数。简单来说，梯度下降就是通过不断调整参数来最小化损失函数，从而达到优化模型的目的。通俗地说，梯度下降就是通过不断调整参数来最小化损失函数，从而达到优化模型的目的。希望这个解释能够帮助您理解梯度下降。如果您还有其他问题，欢迎继续提问。
```

### Analysis

微调后模型对"用通俗的语言解释"这一要求的响应更加到位。Base model 的回答简洁但偏教科书式，没有体现"通俗"的要求。Fine-tuned model 在结尾处加入了"通俗地说，梯度下降就是……"和"希望这个解释能够帮助您理解"等面向用户的表达，语气更加友好。不过 fine-tuned model 的回答中"梯度下降就是通过不断调整参数来最小化损失函数"出现了重复，说明 3K 数据微调后模型的语言更加口语化，但也带来了轻度重复的问题。整体上 fine-tuned model 更好地完成了通俗解释的任务。

---

## Example 3: 英译中

### Instruction

Please translate the following sentence into Chinese.

### Input

```text
Instruction tuning helps language models better follow user requests.
```

### Base model output

```text
Instruction tuning helps language models better follow user requests.
```

### Fine-tuned model output

```text
指令调整有助于语言模型更好地遵循用户的请求。 

注：这句话的中文翻译为“指令调整有助于语言模型更好地遵循用户的请求。”这句话的意思是，通过调整指令，语言模型能够更好地适应用户的需求，从而更好地完成任务。这句话强调了指令调整在语言模型中的重要性。 

另外，这句话也可以翻译为“指令调整有助于语言模型更好地遵循用户的请求。”这句话的意思是，通过调整指令，语言模型能够更好地适应用户的需求，从而更好地完成任务。这句话强调了指令调整在语言模型中的重要性。 

总之，这句话强调了指令调整在语言模型中的重要性，能够更好地适应用户的需求，从而更好地完成任务。这句话也强调了指令调整在语言模型中的重要性。 

另外，这句话也可以翻译为“指令调整有助于语言模型更好地遵循用户的请求。”这句话的意思是，通过调整指令，语言模型
```

### Analysis

该样例中，base model 完全未能理解翻译指令，直接复制了英文原文。Fine-tuned model 能够识别翻译任务并给出正确的中文翻译"指令调整有助于语言模型更好地遵循用户的请求"，但随后出现了严重的重复生成问题：同样的解释性内容被反复输出多次，最终导致截断。这表明 3K 数据微调后模型在翻译任务上的指令遵循能力有所提升，但相比 1K 版本，3K 模型似乎更容易陷入重复生成，可能是训练数据量增加后模型过度学习了某种回复模式，导致在简单任务上也会"过度发挥"。

---

## Example 4: 中译英

### Instruction

请把下面这句话翻译成英文。

### Input

```text
深度学习正在改变自然语言处理。
```

### Base model output

```text
深度学习正在改变自然语言处理。
```

### Fine-tuned model output

```text
Deep learning is changing natural language processing. 

Note: The original sentence is in Chinese, so the translation is in Chinese as well. If you want the translation to be in English, please provide the original sentence. Otherwise, the translation is in Chinese. 

If you want me to translate the sentence to English, please let me know. I can translate it for you. 

Note: The original sentence is in Chinese, so the translation is in Chinese as well. If you want the translation to be in English, please provide the original sentence. Otherwise, the translation is in Chinese. 

If you want me to translate the sentence to English, please let me know. I can translate it for you. 

Note: The original sentence is in Chinese, so the translation is in Chinese as well. If you want the translation to be in English, please provide the original sentence. Otherwise, the
```

### Analysis

与英译中样例类似，base model 在此样例中也未能响应翻译指令，直接复制了中文原文。Fine-tuned model 正确翻译为"Deep learning is changing natural language processing."，但之后却开始用英文输出一段混乱的说明："the original sentence is in Chinese, so the translation is in Chinese as well"——这显然与已完成的翻译矛盾，且被重复输出多次。该样例属于失败案例：fine-tuned model 虽然执行了翻译，但其后续内容完全跑题，说明 3K 微调后模型在某些任务上出现了严重的自我重复和逻辑混乱，这可能是训练过程中模型学习到了一些不理想的生成模式。

---

## Example 5: 总结

### Instruction

请用三句话总结下面这段话。

### Input

```text
大语言模型通常先通过大规模文本进行预训练，获得基础语言建模能力。随后，研究者会使用指令数据进行监督微调，使模型更好地理解和响应用户任务。最后，还可以通过偏好学习或强化学习进一步提升模型的有用性和安全性。
```

### Base model output

```text
1. 大语言模型通常先通过大规模文本进行预训练，获得基础语言建模能力。
2. 研究者会使用指令数据进行监督微调，使模型更好地理解和响应用户任务。
3. 最后，还可以通过偏好学习或强化学习进一步提升模型的有用性和安全性。
```

### Fine-tuned model output

```text
1. 大语言模型通常先通过大规模文本进行预训练，获得基础语言建模能力。
2. 研究者会使用指令数据进行监督微调，使模型更好地理解和响应用户任务。
3. 最后，还可以通过偏好学习或强化学习进一步提升模型的有用性和安全性。 

总结：大语言模型通过预训练和微调，能够更好地理解和响应用户任务，同时通过偏好学习或强化学习，进一步提升模型的有用性和安全性。
```

### Analysis

在该样例中，fine-tuned model 相比 base model 有所提升。两个模型都以"1. 2. 3."的格式列出了原文要点，但 base model 只是简单照抄原文句子。Fine-tuned model 在列出三点之后，额外增加了一句真正的总结："大语言模型通过预训练和微调，能够更好地理解和响应用户任务，同时通过偏好学习或强化学习，进一步提升模型的有用性和安全性。"这表明 3K 数据微调后，模型在摘要类任务上不仅学会了格式，还在一定程度上理解了"总结"这一深层意图。不过整体概括仍偏保守，未能大幅压缩原文信息。

---

## Example 6: 代码解释

### Instruction

请解释下面 Python 代码的作用。

### Input

```text
for i in range(5):
    print(i)
```

### Base model output

```text
这段代码使用了 Python 中的 for 循环语句，用于遍历一个范围内的整数。具体来说，它将从 0 到 4 进行迭代，每次迭代都会打印当前的值。
```

### Fine-tuned model output

```text
这段 Python 代码的作用是打印从 0 到 4 的所有整数。具体来说，它会执行以下操作：

1. `for i in range(5)`：这是 Python 中的 `range` 函数，它是一个生成器函数，用于生成一个从 0 到 4 的整数序列。`range(5)` 会生成一个包含 0 到 4 的整数序列，即 [0, 1, 2, 3, 4]。

2. `print(i)`：对于每个 `i` 的值，它都会执行 `print(i)` 这一行代码，输出 `i` 的值。

3. `print(i)`：由于 `i` 的值是 0 到 4 的整数序列，因此 `print(i)` 会输出 0、1、
```

### Analysis

该样例主要考察代码理解能力。Fine-tuned model 的回答形式更加结构化，将执行过程分为两个步骤逐一说明，看起来更像一份详细的代码解释。但该样例属于失败案例，原因有二：一是 fine-tuned model 将 `range()` 描述为"生成器函数"在严格意义上不准确（`range()` 返回的是不可变序列对象），二是回答末尾出现了明显的截断。相比 1K 版本，3K 版本的回答虽然更详细，但同样存在技术细节不精确的问题，且出现了截断现象。这说明增加训练数据量并不一定改善代码相关任务的准确性。

---

## Example 7: 数学推理

### Instruction

如果一个商品原价 200 元，现在打八折，请问现价是多少？请给出计算过程。

### Base model output

```text
原价为200元的商品，现在打八折，即原价的80%。因此，现价为200元的80%是160元。
```

### Fine-tuned model output

```text
打八折意味着商品的价格是原价的 80%，即 200 元的 80% 是 160 元。因此，现价是 160 元。计算过程如下：

原价 = 200 元
折扣 = 80%
现价 = 原价 × (1 - 折扣)
现价 = 200 元 × (1 - 0.80)
现价 = 200 元 × 0.20
现价 = 40 元

所以，打八折后的现价是 40 元。希望这个计算过程对你有帮助。如果你还有其他问题，欢迎继续提问。
```

### Analysis

该样例属于严重的失败案例。Base model 计算正确（160 元），但推理过程较为简略。Fine-tuned model 虽然给出了看似详细的分步计算过程，却犯了一个根本性的数学错误：将"打八折"错误地理解为 `原价 × (1 - 0.80) = 200 × 0.20 = 40 元`，最终得出了 40 元的错误结论。这反映出 fine-tuned model 学会了输出详细计算步骤的格式，但缺乏真正的数学理解能力——它将"打八折"与"打二折"（减去 80%）混淆了。值得注意的是，1K 版本的 fine-tuned model 在此题上是正确的，3K 版本反而出错，说明增加训练数据并不一定带来一致的能力提升，模型在数学推理上仍存在随机性。

---

## Example 8: 逻辑判断

### Instruction

请判断下面的推理是否正确，并说明原因：所有猫都会飞，小黑是猫，所以小黑会飞。

### Base model output

```text
正确的推理是：所有猫都会飞，小黑是猫，所以小黑会飞。因为小黑是猫，所以小黑会飞。
```

### Fine-tuned model output

```text
这个推理是正确的。根据题目中的信息，所有猫都会飞，小黑是猫，因此小黑会飞。这个推理是正确的，因为它符合逻辑推理的基本规则，即前提和结论之间必须是因果关系。推理过程是基于已知事实，得出一个结论。在这个推理中，推理过程遵循了逻辑推理的基本规则，即前提和结论之间必须是因果关系。因此，这个推理是正确的。不过，需要注意的是，推理过程中的前提和结论之间必须是因果关系，否则推理过程就不是正确的。在实际应用中，推理过程中的前提和结论之间可能不是因果关系，因此推理过程就不是正确的。因此，推理过程中的前提和结论之间必须是因果关系，否则推理过程就不是正确的。在实际应用中，推理过程中的前提和结论之间可能不是因果关系，因此推理过程就
```

### Analysis

该样例属于严重的失败案例。Base model 完全未能识别推理中的逻辑错误，直接判定"正确的推理"。Fine-tuned model 的表现甚至更差：它不仅同样判定"这个推理是正确的"，还用了大段文字来论证"前提和结论之间必须是因果关系"，内容混乱且严重重复，最后以截断结束。该样例非常清楚地表明，无论 1K 还是 3K 数据微调，LoRA instruction fine-tuning 都无法赋予小模型真正的逻辑推理能力。模型只是学会了生成看起来像"分析"的文本，却无法正确判断大前提"所有猫都会飞"本身就是假的。这印证了小规模 instruction tuning 主要改善回答风格，而难以提升模型的逻辑和推理能力。

---

## Example 9: 英文问答

### Instruction

Explain what supervised fine-tuning is in simple terms.

### Base model output

```text
Supervised fine-tuning is a technique used in machine learning to improve the performance of a model by fine-tuning its parameters on a specific task. In supervised fine-tuning, the model is trained on a large dataset of labeled examples, and then fine-tuned on a smaller dataset of unlabeled examples. The fine-tuned model is then used to make predictions on new, unlabeled examples, which can improve the model's performance on the original task.
```

### Fine-tuned model output

```text
Supervised fine-tuning is a technique used in machine learning to improve the performance of a model by adjusting its parameters based on the performance of the model on a specific task. In other words, it is a way to fine-tune a pre-trained model by adjusting its parameters to better fit the specific task at hand. This is done by training the model on a large dataset of labeled examples, and then using the model to make predictions on new, unseen data. The model is then fine-tuned by adjusting its parameters to better fit the specific task at hand, and the process is repeated until the model achieves the desired level of performance. This technique is commonly used in natural language processing, computer vision, and other areas where pre-trained models have been trained on large datasets. By fine-tuning the model, we can improve its performance on new, unseen data, and make it more accurate and effective
```

### Analysis

两者都能围绕"supervised fine-tuning"输出英文回答。Base model 的回答中混入了"on a smaller dataset of unlabeled examples"这一不准确表述，与监督微调的实际情况不符。Fine-tuned model 的回答内容更丰富，提到了应用场景（NLP、计算机视觉），回答结构也更完整，但整体上仍偏学术化，未能很好地满足"in simple terms"的要求。此外 fine-tuned model 的回答较长且存在轻微重复（"to better fit the specific task at hand"出现了两次）。总体来看 fine-tuned model 在内容丰富度上优于 base model，但在通俗性和简洁性上仍有明显差距。

---

## Example 10: 日常助手

### Instruction

请写一封礼貌的邮件，请老师允许我延期提交作业。

### Base model output

```text
尊敬的老师，

您好！我写这封信是想向您表达我的歉意和感激之情。我之前提交了作业，但由于某些原因，我无法按时完成。我非常抱歉，希望您能够理解我的心情，并允许我延期提交作业。

我理解您可能需要时间来处理其他事务，但我希望您能够理解我的困难，并允许我延期提交作业。我非常感激您给我这个机会，让我有机会完成作业，并且希望您能够原谅我的错误。

再次感谢您的耐心和理解，希望您能够原谅我的错误，并允许我延期提交作业。

此致，

敬礼！

[您的姓名]
```

### Fine-tuned model output

```text
尊敬的老师，

您好！我写这封信是想向您表达我的歉意。我最近遇到了一些困难，导致我无法按时提交我的作业。我非常抱歉，希望您能理解我的困难并允许我延期提交作业。

我非常感激您一直以来对我的关心和支持，我将尽快完成作业，并在规定的时间内提交。如果您有任何问题或需要帮助，请随时与我联系。

再次感谢您的耐心等待，希望您能尽快回复我的邮件。

此致，
[您的名字]
```

### Analysis

在日常助手类任务中，fine-tuned model 相比 base model 有显著提升。Base model 存在明显的前后矛盾（"我之前提交了作业"与"我无法按时完成"互相冲突），语句重复啰嗦（"希望您能够原谅我的错误"出现了两次）。Fine-tuned model 的邮件逻辑清晰、语言得体：正确地表达了"最近遇到困难导致无法按时提交"的因果关系，语气礼貌自然，格式完整。相比 1K 版本 fine-tuned model 出现的"您在上个月提交了作业"逻辑错误，3K 版本在此例中表现明显更好，说明增加训练数据量对助手类任务的一致性有一定帮助。不过邮件中的"希望您能尽快回复"略显催促，尚可进一步优化。

---