# 第 25 课：大厂真题精讲（上）

五道真题，每题覆盖一个核心面试方向。

**字节：PEFT 方案怎么选。** 通用 LoRA（r=8-16）。显存紧 QLoRA。精度控 Adapter。简单分类 Prompt Tuning。r 值看任务复杂度，简单情感 r=4，复杂推理 r=32。LoRA 训在 Q、V 上效果最好。QLoRA 实测显存比理论高 10%-20%。

**腾讯：RAG 系统怎么设计。** 切分 200-500 Token→BGE/text-embedding-3 建索引→向量+BM25 混合召→Cross-Encoder 重排→拼 Prompt 喂 LLM。Chunk size 从 300 开始试，看检索召回率。ChromaDB 做原型，Milvus 上生产。RAGAS 做评估。

**阿里：偏差和方差。** 训练&验证 Loss 都高→偏差高（欠拟合）→加数据加参数加步数。训练低验证高→方差高（过拟合）→正则化。PEFT 天然低方差。全参微调数据少时方差极高。Debug 看两 Loss 的 gap。

**美团：Agent 怎么拆。** 感知层（用户输入+工具返回+上下文）、决策层（ReAct：思考-行动-观察）、执行层（Function Calling）、记忆层（短期+长期）。单 Agent vs 多 Agent 看任务边界。工具调错→三层防御：参数校验、异常重试（N 次换参换工具）、回退兜底。

**小红书：MoE 怎么玩更稳。** 负载均衡加辅助 loss。All-to-All 优化通信。保守学习率配频繁负载检查。

---

### 模拟面试：完整回答一道 RAG 题

面试官：「给你一个包含 500 篇技术文档的内网知识库，设计一个 RAG 问答系统。」

**你的回答**：

「我分五步来。

**切分**，先试 300 Token 的 chunk，overlap 设 50 Token。然后看实际文档类型调，如果大部分是 API 文档，结构性强，可以切得更短（200 Token）。如果是综述类长文，拉到 500。

**Embedding**，用 BGE-large-zh 或 text-embedding-3-large，1536 维。如果文档涉及大量代码，考虑训练 domain-specific 的 embedding 模型。

**检索**，向量检索做语义召回，BM25 做关键词精确匹配。Top-20 召回来之后，用 Cross-Encoder 做重排序，取 Top-5 送入 LLM。这个两步检索能兼顾语义和精确。

**生成 Prompt**，给每个 chunk 标上来源、相似度分数，要求模型「如资料中没有相关信息，请直接说明不知道，不要编造」。这一句能把幻觉率降一截。

**评估闭环**，上线后用 RAGAS 框架定期抽检，看检索召回率和答案准确率。用户反馈里搜集 badcase，回到切分策略上迭代 chunk size。」

面试官大概率会在 chunk size 怎么调、混合检索的实现细节、Cross-Encoder 的性能开销上追着问。提前准备好这三个点的具体回答。

---

> 磨平一些信息差。
