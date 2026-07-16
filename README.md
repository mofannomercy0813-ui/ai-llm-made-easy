# 《AI 大模型不难》

> 扫盲书，看完你就会懂怎么说黑话。28 课 + 2 附录，不讲代码，只把原理拆到你能在面试里讲清楚。

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

---

## 为什么有这本书

大模型面试八股背到第三天就崩溃了。不是因为记不住。是因为面试官每个词都能追着问——LoRA 原理？跟 QLoRA 的区别？为什么不直接用 Adapter？

市面上的资源有三种：付费课程太贵且不知道值不值，开源教程代码太重需要 PyTorch 基础，面试题库给你标准答案但不讲「为什么是这个答案」。

这本书做一件事：**每个概念从零开始讲，讲到你能用自己的话在面试里说清楚为止。** 不用 GPU，不用 Jupyter，一部手机就能读完。

---

## 读完你能做什么

- 面试被问到 Attention、LoRA、RLHF、RAG 时，给出有层次、有原理、有数值的完整回答
- 用自己的话给完全不懂技术的朋友讲清楚 Transformer 是怎么工作的
- 看懂 DeepSeek-V3、Llama 4 的技术报告，不再被公式挡在门外
- 设计一个 RAG 系统、选一个 PEFT 方案、拆一个 Agent 任务——有明确的决策逻辑

---

## 目录（28 课 + 2 附录）

**第 0 课：开篇 + 大模型五分钟全景图**

### 第一部分：世界观

1. Token、预训练、微调
2. 涌现和幻觉
3. Prompt + CoT + ICL
4. 解码策略
5. RLHF 五分钟速览
6. 量化、蒸馏、分布式

### 第二部分：引擎

7. Transformer 到底是什么
8. Attention 公式
9. 多头注意力
10. 位置编码（RoPE）
11. 残差连接
12. LayerNorm / RMSNorm
13. Pre-norm vs Post-norm
14. Padding Mask + Sequence Mask

### 第三部分：炼金

15. 参数 vs 数据 + Chinchilla
16. MLM vs CLM
17. RLHF 全流程
18. DPO 和 GRPO
19. LoRA / QLoRA
20. 过拟合、梯度、Warmup、ZeRO

### 第四部分：落地

21. RAG 全链路
22. 推理优化全家桶
23. AI Agent + ReAct
24. MCP / A2A / Function Call
25. MoE、GQA、MLA
26. 多模态/VLM 入门

### 第五部分：实战

27. 大厂真题精讲（上）
28. 大厂真题精讲（下）+ 系统设计 + 项目讲述

### 附录

- **A**：NLP 基础速查
- **B**：理论速查表（公式、显存、默认值、模型对比）

---

## 与其他资源的区别

| | 本书 | 图解大模型 | Happy-LLM | LLMs-from-scratch |
|---|---|---|---|---|
| 形式 | 原理精讲 + 手算走通 + 面试演练 | 300 幅全彩插图 | PyTorch 代码实现 | 从零写 GPT |
| 时长 | 周末读完 | 需系统学习 | 需编程基础 | 需编程+数学 |
| 适合 | 面试准备 + 零基础扫盲 | 深入理解 + 实操 | 代码实战 | 底层原理 |
| 价格 | 免费开源 | ¥159.80 | 免费 | 免费 |

---

## 本地阅读

```bash
pip install markdown
python scripts/build_html.py         # 生成 HTML
python scripts/build_html.py --pdf   # 生成 HTML + PDF
```

或直接打开仓库里的 `index.html` 或下载 `ai-llm-made-easy.pdf`。

---

## 反馈

发现错误、有更好的讲法、或者用这本书面过了面试——提 Issue 或 PR。

---

> 磨平一些信息差。
