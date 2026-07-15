# 第 22 课：AI Agent，让模型会干活

Chatbot 是被动回答，你问一句它答一句，答完就忘。Agent 是主动完成任务，感知环境、做决策、调工具、看结果、调整下一步，循环直到目标达成。

### Function Calling：模型的「遥控器」

Agent 最基础的能力是调用外部工具。机制叫 Function Calling：

1. 提前定义好工具清单（函数名、参数格式、功能描述），写在 system prompt 里
2. 用户输入后，模型决定要不要调工具。要调的话，输出一串 JSON 描述「调哪个函数、传什么参数」
3. 外部框架截获这串 JSON，执行真正的函数调用（查数据库、调 API、读文件）
4. 把返回结果追加到对话历史里，喂回给模型
5. 模型基于工具返回结果继续推理或输出最终回答

模型自己不能上网、不能查数据库、不能发微信。它只会生成 JSON。是外部框架在替它执行。这种设计让模型的能力可以无限外挂，加一个新工具只需要在清单里多写一行描述。

### ReAct：Agent 的决策循环

ReAct = Reasoning + Acting。最主流的 Agent 决策模式。不是「想好了再动手」，而是「想一步、做一步、看结果、再想下一步」。

一个完整的 ReAct 循环：

```
Thought（思考）：我现在知道了什么，下一步该做什么
Action（行动）：调用工具
Observation（观察）：工具返回了什么
→ 回到 Thought，基于新信息继续
```

这套循环让 Agent 具备了两个 Chatbot 没有的能力。多步推理：复杂任务不能一步完成，Agent 自己拆成若干步，每一步基于上一步的结果调整。错误恢复：工具返回错误时，Agent 换参数重试或换工具，不会直接输出一个错的最终答案。

### 一个 Agent 的实际执行过程

任务：「帮我查一下北京明天天气，如果下雨就给我的微信发条提醒」

**Thought 1**：「先查天气。」
**Action 1**：生成 Function Call
```json
{"function": "get_weather", "parameters": {"city": "北京", "date": "2026-07-16"}}
```
**Observation 1**：`{"weather": "中雨", "temp": "26°C"}`

**Thought 2**：「中雨，需要提醒。」
**Action 2**：生成 Function Call
```json
{"function": "send_wechat", "parameters": {"to": "self", "message": "明天北京中雨 26°C，带伞"}}
```
**Observation 2**：`{"status": "sent"}`

**Thought 3**：「搞定了，回复用户。」
**Final Answer**：「明天北京中雨 26°C，微信提醒已发送。」

Chatbot 只能输出「明天北京可能下雨」。Agent 真的调了 API 查天气，并且真的发了微信。

### 单 Agent vs 多 Agent

单 Agent 手里有所有工具，自己决策全过程。简单直接，适合任务边界清晰、工具不超过 10 个的场景。能力受限于单个模型的推理深度。

多 Agent 各司其职。一个检索 Agent 从数据库拉数据，一个分析 Agent 做结论，一个写作 Agent 出报告。Agent 之间通过消息传递信息。复杂度指数增长，通信死锁、等待链、谁来仲裁，需要在架构层面做超时和容错。

Google 的 A2A 协议就是为多 Agent 互操作设计的。第 23 课详讲。

---

> 磨平一些信息差。
