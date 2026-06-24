# Base Model vs Fine-tuned Model Output Comparison

- Base model: Qwen2.5-0.5B
- Fine-tuned model: Qwen2.5-0.5B + LoRA adapter trained on mixed 1K Alpaca-style data

## Example 1: 中文问答

### Instruction

请解释什么是过拟合。

### Base model output

```text
过拟合是指在训练数据上训练模型时，模型过于复杂，以至于无法很好地拟合训练数据，从而导致模型在测试数据上的表现不佳。具体来说，过拟合是指模型在训练数据上的表现好，但在测试数据上的表现差。这是因为过拟合是因为模型过于复杂，以至于无法很好地拟合训练数据，从而导致模型在测试数据上的表现不佳。为了防止过拟合，可以采取以下措施：1.减少模型的复杂度；2.使用正则化技术，如L1和L2正则化；3.使用交叉验证技术，以评估模型的性能并避免过拟合。
```

### Fine-tuned model output

```text
过拟合是指在训练数据集上训练模型时，模型过于拟合训练数据，而忽略了训练数据集之外的噪声和异常值。这意味着模型在训练过程中学习了训练数据的模式，而忽略了训练数据集之外的模式，从而导致模型在测试数据集上的表现不佳。

过拟合通常可以通过降低模型的复杂度来解决，例如通过减少模型的层数、减少模型的参数数量等。然而，过拟合也会带来其他问题，例如模型的泛化能力差，容易在测试数据集上表现不佳。因此，需要在训练和测试数据集上进行交叉验证，选择一个合适的模型复杂度，以及使用正则化技术来防止过拟合。
```

### Analysis

微调后模型对中文指令的响应更加自然，能够直接解释问题中的核心概念。Base model 的输出存在明显的重复问题（"模型过于复杂，以至于无法很好地拟合训练数据"重复了两次），而且没有对"过拟合"给出清晰的解释。Fine-tuned model 的回答结构更清晰，先给出了过拟合的定义，再说明了解决方案，语言更接近面向用户的解释风格。但在准确性上，fine-tuned model 将过拟合归因于"忽略了训练数据集之外的噪声和异常值"，这一表述不够准确，说明 LoRA instruction fine-tuning 主要改善了回答格式和指令遵循能力，对模型本身的知识纠偏作用有限。

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
梯度下降是一种优化算法，它通过不断调整参数来最小化损失函数。损失函数是用来衡量模型预测结果与真实结果之间的差异。梯度下降算法通过计算损失函数的梯度，然后沿着梯度的方向调整参数，以最小化损失函数。这个过程称为反向传播，它通过计算损失函数的梯度来更新参数。梯度下降算法通常用于机器学习和深度学习中，用于优化模型的参数，以提高模型的性能。
```

### Analysis

微调后模型对中文指令的响应更加完整，能够围绕"通俗的语言"这一要求展开解释。Base model 的回答虽然基本正确，但"在低维空间中找到全局最小值"的表述比较抽象，没有体现"通俗"的要求，更像是一段教科书式的定义。Fine-tuned model 引入了损失函数、反向传播等概念，回答内容更充实，语气也更倾向于向用户解释说明。不过 fine-tuned model 也没有做到真正的通俗易懂，仍包含较多专业术语，说明 instruction tuning 提升了回答的完整性和格式，但在满足"通俗解释"这类细粒度要求上仍有不足。

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
翻译：训练语言模型以更好地响应用户的请求。
```

### Analysis

该样例中两个模型的差异非常明显。Base model 完全没有理解翻译指令，直接复制了英文原文而没有进行任何翻译操作，说明其 instruction-following 能力较弱，更像是把 prompt 当作待续写的文本。Fine-tuned model 能够正确识别翻译任务，并给出了准确的中文翻译结果，以"翻译："作为前缀的格式也符合指令回答的风格。这说明 LoRA instruction fine-tuning 显著改善了模型对翻译类指令的遵循能力。

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
```

### Analysis

与 Example 3 类似，Base model 在此样例中也未能理解翻译指令，只是直接复制了中文原文，说明 base model 的 instruction-following 能力较弱，无法将翻译类 prompt 识别为任务指令。Fine-tuned model 准确地完成了中译英任务，翻译结果"Deep learning is changing natural language processing."语义准确、表达自然。这再次表明 LoRA instruction fine-tuning 对翻译类指令的遵循能力有显著提升。

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
1. 大语言模型先通过大规模文本进行预训练，获得基础语言建模能力。
2. 研究者会使用指令数据进行监督微调，使模型更好地理解和响应用户任务。
3. 最后，还可以通过偏好学习或强化学习进一步提升模型的有用性和安全性。
```

### Analysis

在该样例中，base model 和 fine-tuned model 的输出差异不明显。两个模型都只是将原文的三句话标上序号输出，并没有真正进行"用自己的话概括"这一核心要求，本质上都是在复述原文而非摘要。可能原因是该任务本身对语言生成能力要求不高，base model 已经能够给出格式合理的回答；同时本实验只使用了 1000 条训练样本，微调规模较小，因此在需要理解"总结"这一深层意图的任务上能力提升有限。该样例可作为失败案例之一。

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
这段 Python 代码的作用是打印从 0 到 4 的所有整数。它使用了 Python 的 `range()` 函数，该函数返回一个生成器对象，它每次迭代都会返回一个整数。在本例中，`range(5)` 返回一个包含 0 到 4 的整数的序列，然后使用 `for` 循环遍历这个序列，打印每个值。
```

### Analysis

该样例主要考察代码理解能力。Fine-tuned model 的回答形式更符合解释类任务，提供了更多细节：它明确指出代码打印 0 到 4，并额外解释了 `range()` 函数的生成器行为，说明微调后模型在代码解释任务上倾向于给出更详尽的回答。但需要指出的是，fine-tuned model 将 `range()` 描述为"返回一个生成器对象"在严格意义上不够精确（`range()` 返回的是一个不可变的序列对象，不是生成器），说明本次 instruction tuning 对代码能力的提升主要体现在回答风格上，对技术细节的准确性改善有限。该样例属于失败案例。

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
打八折意味着商品售价为原价的 80%，即 200 元的 80% = 200 * 0.8 = 160 元。因此，现价为 160 元。
```

### Analysis

两个模型在计算结果上都是正确的（160 元），但 fine-tuned model 的回答更符合"给出计算过程"的指令要求，明确写出了 `200 * 0.8 = 160` 的计算步骤，而 base model 直接跳到结论"200元的80%是160元"，中间推理过程更简略。在本样例中，fine-tuned model 能够更好地遵循指令格式，提供更清晰的分步推理。但由于该数学问题本身较简单，两个模型都能正确作答，总体差异不大。

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
这个推理是不正确的。原因如下：

1. 原理：推理是根据已知的事实或前提，得出一个结论的过程。在这个推理中，推理者根据“所有猫都会飞”这一前提，得出结论“小黑会飞”。

2. 事实：推理者没有提供关于小黑是否真的会飞的任何事实或证据。他们只是根据已知的事实“所有猫都会飞”来得出结论。

3. 结论：这个推理得出的结论是错误的。因为推理者没有提供关于小黑是否真的会飞的任何事实或证据，所以不能得出小黑会飞的结论。

因此，这个推理是不正确的。推理者应该根据已知的事实或前提，得出一个结论，而不是根据已知的事实或前提得出一个结论。
```

### Analysis

该样例明显属于失败案例。Base model 完全未能识别推理中的逻辑错误，直接判定"正确的推理"，说明其不具备基本的逻辑分析能力。Fine-tuned model 在形式上有所改善，能够判断该推理"是不正确的"，但其论证过程存在严重问题：它关注的是"没有关于小黑是否会飞的证据"，而真正的错误在于大前提"所有猫都会飞"本身就是假的。这说明即使经过 LoRA 微调，模型也只是学会了输出"这个推理不正确"这样的回答格式，却无法进行真正的逻辑分析。这也印证了小规模 instruction tuning 更容易改善回答风格，而难以显著提升模型的逻辑推理能力。

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
Supervised fine-tuning is a technique used in machine learning to improve the performance of a model by fine-tuning its parameters on a new dataset. It involves training the model on a large dataset, and then fine-tuning its parameters on a smaller dataset that is similar to the original dataset but with fewer features. This process helps the model to learn the specific patterns and relationships in the new data, resulting in better performance on the new data. Supervised fine-tuning is often used in natural language processing, computer vision, and other machine learning tasks. It is a common technique used to improve the performance of models on new data.
```

### Analysis

两者都能围绕"supervised fine-tuning"这一主题输出英文回答。但 Base model 的解释中混入了不准确的信息，例如将微调描述为"在大量有标签数据上训练后在少量无标签数据上微调"，这与监督微调的实际情况不符（微调数据通常也是有标签的）。Fine-tuned model 的回答更加完整，提到了 NLP 和计算机视觉等应用场景，但同样存在一些模糊表述，如 in simple terms 的要求并未被充分满足，回答仍偏学术化。整体来看 fine-tuned model 略好，但两者在准确性和通俗性上都有提升空间。

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

您好！我写这封邮件是为了向您表达我的歉意。我注意到您在上个月提交了作业，但因为某种原因，我无法按时完成作业。我非常抱歉，希望您能理解我的歉意，并允许我延期提交作业。

如果您需要帮助，我将很乐意为您提供帮助。请随时与我联系。

此致，
[您的名字]
```

### Analysis

在日常助手类任务中，fine-tuned model 的整体表现更好。Base model 存在明显的前后矛盾："我之前提交了作业"与"我无法按时完成"互相冲突，让邮件内容逻辑不通。Fine-tuned model 的回答格式更像一封正式的请求邮件，语气礼貌，结构完整。不过 fine-tuned model 也出现了"您在上个月提交了作业"这样的逻辑错误（提交作业的应该是学生而不是老师，且与"延期提交"矛盾）。这说明 instruction fine-tuning 对助手风格和邮件格式的生成有明显帮助，但在内容的一致性和逻辑自洽性上仍存在问题，小规模微调对此类问题的改善有限。

---