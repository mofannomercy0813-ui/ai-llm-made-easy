# 第 12 课：Pre-norm vs Post-norm，安检放哪的问题

两个公式。

Post-norm（原论文）：y = LayerNorm(x + F(x))
Pre-norm（现代）：y = x + F(LayerNorm(x))

区别：LayerNorm 放在加号前还是加号后。

Post-norm 把残差和子层输出加起来再过 LayerNorm。梯度回传要经过除法，训练初期网络不稳，标准差上蹿下跳，梯度跟着波动。需要 Warmup：前几千步极小学习率等网络稳定。

Pre-norm 把 LayerNorm 挪到 F(x) 前面。残差的平滑通道直接绕过整个 F(LayerNorm(x)) 块，梯度走这条不经过任何运算。dy/dx = I + dF(LN(x))/dx，I 保底。不需要 Warmup，从第一步就能用正常学习率。

---

### 梯度回传路径对比

以一个 Attention 子层为例，输入 x = [0.5, -0.3, 0.8]。

**Post-norm 路径**：

```
x ──→ Attention ──→ + ──→ LayerNorm ──→ y
 ↑                              │
 └────── 残差 ──────────────────┘
                                ↓
                              梯度要过 LayerNorm
                              ÷σ 压缩 / ×σ 放大
```

梯度从 y 回传到 x，必须穿过 LayerNorm 的除法运算。如果训练初期 σ=0.1，梯度被放大 10 倍，参数飞出去。如果 σ=10.0，梯度被压缩到 0.1 倍，参数原地踏步。这就是需要 Warmup 的根源。

**Pre-norm 路径**：

```
x ──→ LayerNorm ──→ Attention ──→ + ──→ y
 ↑                                  │
 └───────── 残差直通 ───────────────┘
                                    梯度从这里回传
                                    直接走残差线，不经运算
```

梯度从 y 回传时，残差线是纯直通。即使 Attention 输出归一化后的 σ 剧烈波动，残差线始终给出 ∂y/∂x = I 的保底梯度。第一步就能正常训。

所有现代模型全用 Pre-norm。代价是对表达能力的微弱损失远小于工程稳定性的收益。Post-norm 已被历史淘汰。

---

> 磨平一些信息差。
