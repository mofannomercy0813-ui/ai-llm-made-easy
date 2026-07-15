# 第 6 课：Transformer 到底是什么

2017 年 Google 发了篇论文，《Attention Is All You Need》。没吹牛。GPT、Claude、Llama、DeepSeek 全是它的直系后代。

RNN 像只有一个收费窗口，车必须排队过。Transformer 像几十个窗口同时开，所有车一起处理，每辆车能同时看到路上所有其他车。

原版 Transformer 有 Encoder 和 Decoder。Encoder 双向理解输入，Decoder 单向生成输出。Enc-Dec 之间有 Cross-Attention 传信息。

后来大家发现可以只用一半。扔掉 Encoder，只用 Decoder，这就是 GPT。扔掉 Decoder，只用 Encoder，这就是 BERT。两边都留着，这就是 T5。

共享的砖块只有四种。注意力机制，每个词跟所有其他词对话。残差连接，梯度高速公路。层归一化，统一数值范围。位置编码，注入词序信息。

![Transformer 架构图解](../../assets/transformer-architecture.svg)

---

### 走一遍：一句话穿过 GPT 的完整路径

输入：「猫坐在垫子上」

**Step 1 — Tokenize + Embedding**：切成 5 个 Token，每个映射成 768 维向量。

**Step 2 — 位置编码**：位置 0 的「猫」旋转一个角度，位置 1 的「坐」转更大角度。现在每个向量知道自己排第几。

**Step 3 — Attention 层（第 1 层）**：「垫子」通过 Attention 发现自己跟「猫」「坐」关系最紧，跟「上」的关系没那么紧。所有 Token 互相看，加权融合信息。

**Step 4 — 残差 + LayerNorm**：加回原始输入，归一化。

**Step 5 — FFN 层**：每个 Token 独立过两层全连接，做一次非线性变换。

**Step 6 — 重复 32 层**：每层都在上一步基础上提取更高级的语义关系。第 1 层可能学到「垫子」跟「猫」相关，第 20 层可能学到整句话的动作逻辑。

**Step 7 — 输出**：最后一个 Token 的向量过 Linear + Softmax，从 10 万 Token 词表里挑概率最高的那个，输出下一个词。

Transformer 不是模型，是一套建筑图纸。用这套图纸你可以盖 BERT、GPT 或 T5。GPT-4 堆了几百层，但砖还是这四种。

---

> 磨平一些信息差。
