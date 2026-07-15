# 第 24 课：前沿架构，MoE、GQA、DeepSeek 怎么玩的

MoE（Mixture of Experts）：把密集的 FFN 拆成多个「专家」小矩阵。每个 Token 经由路由网络只激活 Top-2 专家。参数量暴增但激活量不暴增。DeepSeek-V3 总参数 1.6T，每次推理只激活 49B。负载均衡通过辅助损失保证各专家使用率均等。

GQA（Grouped Query Attention）：K 和 V 分成 G 组，Q 保持全头，组内共享 KV。MHA（全头）精度最高但 KV Cache 大。MQA（K/V=1 头）最省但信息瓶颈。GQA 取折中。Llama 2、Qwen 用 GQA。

DeepSeek-V3 整合了 MoE + GQA + MLA（Multi-head Latent Attention，KV 投影到极小的潜在空间，128K 长序列 KV Cache 压至传统方案 1/10）。开源模型顶尖。

---

## 追问模块

**追问：「MoE 路由网络怎么训？」** 和主模型一起训。路由是一个小线性层加 softmax，辅助负载均衡损失防网红专家。

**追问：「GQA 精度损失？」** 多数任务感知不到，1%-2% benchmark 差异。KV Cache 节省倍数为 G 值。

**追问：「MLA 是怎么压缩 KV Cache 的？」** KV 投影到比 d_head 更小的潜在维度，推理时从潜在空间恢复完整 KV。有监督有损压缩，长上下文推理成本核心原因。

---

## 思考题

1. MoE 专家调度像不像公司部门分派，有些常年满负荷有些闲置。

2. GQA 的 G 值你会怎么定。

---

> 磨平一些信息差。
