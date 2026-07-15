# 附录 B：理论速查表

面试前 10 分钟翻一遍。全是数字、公式、默认值。

### 显存速算

| 精度 | 每参数大小 | 7B 模型显存 | 70B 模型显存 | 备注 |
|------|-----------|-----------|------------|------|
| FP32 | 4 字节 | ~28 GB | ~280 GB | 全参训练 |
| FP16 | 2 字节 | ~14 GB | ~140 GB | 推理标配 |
| INT8 | 1 字节 | ~7 GB | ~70 GB | 推理加速 |
| INT4 | 0.5 字节 | ~3.5 GB | ~35 GB | QLoRA |
| FP16 训练 | 2 字节 ×4 | ~56 GB | ~560 GB | 参数+梯度+优化器×2 |
| LoRA (r=8) | 额外 ~0.06 GB | ~14 GB | ~140 GB | 基座 FP16 + LoRA 参数 |

### 公式速查

| 名称 | 公式 |
|------|------|
| Attention | softmax(QK^T / sqrt(d_k)) V |
| RoPE | Q_m = R_m·q, K_n = R_n·k, R_m^T R_n = R_{n-m} |
| PPO Clip | min(r_t A_t, clip(r_t, 1-ε, 1+ε) A_t) |
| DPO Loss | -log σ(β(log π_θ(y_w)/π_ref(y_w) - log π_θ(y_l)/π_ref(y_l))) |
| Chinchilla | N_opt ∝ C^0.5, D_opt ∝ C^0.5, D ≈ 20N |
| LoRA | W' = W + B·A, B∈R^(d×r), A∈R^(r×d) |
| Cross-Entropy | L = -log(p_correct) |

### 常用默认值

| 参数 | 默认值 | 说明 |
|------|--------|------|
| LoRA r | 8 | 简单任务 4，复杂推理 32 |
| LoRA α | 16 | 通常 = 2×r |
| PPO ε | 0.2 | Clip 范围 |
| KL β | 0.01-0.1 | RLHF 约束强度 |
| Temperature | 0.7-1.0 | 对话领域 |
| Top-P | 0.9 | GPT 默认 |
| Learning Rate | 1e-4 ~ 5e-5 | LLM 预训练/微调 |
| Batch Size | 128-512 | LLM 微调（样本数） |
| Gradient Clip | 1.0 | 梯度裁剪阈值 |

### 开源模型速查

| 模型 | 参数量 | 架构 | 上下文 | 特点 |
|------|--------|------|--------|------|
| Qwen2.5 | 0.5B-72B | Dense + GQA | 128K | 中文最强，Apache 2.0 |
| DeepSeek-V3 | 1.6T/49B | MoE + MLA | 128K | 开源顶配，激活参数 49B |
| Llama 3.3 | 8B-70B | Dense + GQA | 128K | 英文标杆 |
| Qwen-VL | 2B-72B | VLM | 128K | 多模态中文 |
| Llama 4 | Scout/Maverick | MoE | 10M | 千万级上下文 |

### 面试常用数字

| 问题 | 答案 |
|------|------|
| Attention 复杂度 | O(n²) |
| LoRA 参数量 (7B, r=8) | ~17M (约 0.2%) |
| KV Cache 大小 (7B, n=4096) | ~2 GB |
| Chinchilla 最优比 | 每 1 参数喂 ~20 Token |
| GPT-3 训练数据量 | ~300B Token |
| GPT-4 训练成本 | ~1 亿美元 |
| LLaMA 7B 全参微调显存 | ~56 GB (FP16) |
| LLaMA 7B LoRA 显存 | ~16 GB (FP16) |
| BPE 词表大小 (GPT-4) | ~100K Token |
| Warmup 步数 | 500-3000 |

---

> 磨平一些信息差。
