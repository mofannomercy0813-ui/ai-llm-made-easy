# 第 22 课：AI Agent，让模型会干活

Chatbot 是被动回答。Agent 是主动完成任务，感知环境、做决策、调工具、看结果、调整下一步。

四个环节。感知，知道现在什么情况。决策，基于感知决定下一步。执行，调用工具。学习，从结果中更新策略。PDEO 循环持续转。

Function Calling：模型生成 JSON 描述要调什么函数传什么参，外部框架执行后结果喂回。像遥控器，模型按按钮，外面的人操作。

单 Agent vs 多 Agent。单 Agent 简单但能力窄。多 Agent 各司其职，一个检索一个分析一个写报告，信息在之间流转。

---

### 一个 Agent 的实际执行过程

任务：「帮我查一下北京明天天气，如果下雨就给我的微信发条提醒」

**Step 1 — 模型分解任务**：
1. 调用天气 API 查北京明天天气
2. 判断是否下雨
3. 如果下雨，调用微信 API 发送消息

**Step 2 — Function Call（查天气）**：

```json
{
  "function": "get_weather",
  "parameters": {"city": "北京", "date": "2026-07-16"}
}
```

框架执行 → 返回 `{"weather": "中雨", "temp": "26°C"}`

**Step 3 — 模型判断**：weather = "中雨" → 触发提醒逻辑。

**Step 4 — Function Call（发微信）**：

```json
{
  "function": "send_wechat",
  "parameters": {"to": "self", "message": "明天北京有中雨，26°C，记得带伞"}
}
```

**Step 5 — 结束**：模型输出「已查完。明天北京中雨 26°C，微信提醒已发送。」

Agent 跟 Chatbot 的核心区别：Chatbot 只能输出文字告诉你「可能会下雨」。Agent 真的去调 API 查了天气，并且真的发了微信。行动闭环。

---

> 磨平一些信息差。
