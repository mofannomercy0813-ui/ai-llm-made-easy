# 第 17 课：DPO 和 GRPO，更聪明的对齐方式

PPO 太贵。四个模型，两倍计算量，大量偏好标注，一堆超参。

DPO（Direct Preference Optimization）：直接干掉 RM 和 PPO。从偏好数据推一个跟 RLHF 等价的损失函数，一次梯度更新。只用一个模型，计算量等于 SFT。代价是对偏好数据质量高度敏感，没有 RM 的平滑缓冲。

GRPO（Group Relative Policy Optimization）：DeepSeek 的方案。也砍掉价值模型，改用一组回答的相对分数。同 prompt 生成 8 个回答，RM 打分，用均值和标准差算「相对优势」。优势不依赖绝对分数，只需要知道在 8 个里排第几。KL 约束从 reward 里挪到 loss 里，执法更硬，更防策略跑偏。

选型矩阵：预算足上 PPO。预算紧用 DPO。想稳妥选 GRPO。

---

## 追问模块

**追问：「DPO 能在所有任务追平 RLHF 吗？」** 大部分 benchmark 可以。安全对齐等需要精确奖励建模的任务上 RLHF 更稳。

**追问：「HHH 原则是什么？」** Helpful（有用）、Honest（诚实）、Harmless（无害）。RLHF 对齐的三大目标。

**追问：「GRPO 的 8 个回答全都很差怎么办？」** RM 评出来的相对最好不代表真的好，RM 本身可能出问题。多层防御必不可少。

---

## 思考题

1. 你更适合 PPO（被打分再改进）还是 DPO（看到对比直接学更好的）。

2. 如果 GRPO 的 RM 本身不可靠，你能设计什么兜底机制。

---

> 磨平一些信息差。
