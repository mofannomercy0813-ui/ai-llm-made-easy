# 第 24 课：前沿架构，MoE、GQA、DeepSeek 怎么玩的

MoE（Mixture of Experts）：把密集的 FFN 拆成多个「专家」小矩阵。每个 Token 经由路由网络只激活 Top-2 专家。参数量暴增但激活量不暴增。DeepSeek-V3 总参数 1.6T，每次推理只激活 49B。负载均衡通过辅助损失保证各专家使用率均等。

GQA（Grouped Query Attention）：K 和 V 分成 G 组，Q 保持全头，组内共享 KV。MHA（全头）精度最高但 KV Cache 大。MQA（K/V=1 头）最省但信息瓶颈。GQA 取折中。Llama 2、Qwen 用 GQA。

DeepSeek-V3 整合了 MoE + GQA + MLA（Multi-head Latent Attention，KV 投影到极小的潜在空间，128K 长序列 KV Cache 压至传统方案 1/10）。开源模型顶尖。

---

### MoE 怎么做到「参数巨大但推理不贵」

传统密集模型：一个 7B 模型，每个 Token 都要经过全部 7B 参数。计算量 = 7B。

DeepSeek-V3：256 个专家（每个约 6.4B），每次只激活 Top-8。

**一个 Token 穿过 MoE 层的计算**：

```
Token 「猫」→ 路由网络打分 →
  专家 17: 0.83（激活）
  专家 89: 0.72（激活）
  专家 3: 0.15（忽略）
  ...
  专家 201: 0.08（忽略）

输出 = 0.83 × Expert17(Token) + 0.72 × Expert89(Token)
```

256 个专家，只跑了 8 个。参数量 1.6T，每次推理的计算量只相当于激活参数 49B。这就是 MoE 的精髓：大模型的容量，小模型的速度。

**负载均衡怎么保证**：如果所有 Token 都选专家 17 和 89，其他 254 个专家白训了。辅助损失函数惩罚专家使用不均：

```
L_balance = α × Σ(每个专家的平均选择概率 - 1/N_experts)²
```

所有专家使用率强制均匀分布。训练几亿 Token 后，256 个专家自然分化出各自的领域。

---

> 磨平一些信息差。
