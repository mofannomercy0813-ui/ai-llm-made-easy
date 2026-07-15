# 第 12 课：Pre-norm vs Post-norm，安检放哪的问题

两个公式。

Post-norm（原论文）：y = LayerNorm(x + F(x))
Pre-norm（现代）：y = x + F(LayerNorm(x))

区别：LayerNorm 放在加号前还是加号后。

Post-norm 把残差和子层输出加起来再过 LayerNorm。梯度回传要经过除法，训练初期网络不稳，标准差上蹿下跳，梯度跟着波动。需要 Warmup：前几千步极小学习率等网络稳定。

Pre-norm 把 LayerNorm 挪到 F(x) 前面。残差的平滑通道直接绕过整个 F(LayerNorm(x)) 块，梯度走这条不经过任何运算。dy/dx = I + dF(LN(x))/dx，I 保底。不需要 Warmup，从第一步就能用正常学习率。

所有现代模型全用 Pre-norm。代价是对表达能力的微弱损失远小于工程稳定性的收益。Post-norm 已被历史淘汰。

---

## 追问模块

**追问：「Pre-norm 有没有升级版？」** Sandwich-LN 和 DeepNorm 都是 Pre-norm 方向上的变体。

**追问：「Post-norm 配 Warmup 能不能追平 Pre-norm？」** 能追平效果，但多了 Warmup 这个需要调参的超参数。工程不划算。

---

## 思考题

1. 用安检排队解释 Pre-norm 和 Post-norm。

2. 如果时间和算力无限，你会选哪个。为什么 2026 年所有模型都选 Pre-norm。

---

> 磨平一些信息差。
