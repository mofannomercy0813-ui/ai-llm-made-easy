# 第 23 课：MCP / A2A / Function Call，让模型会叫外援

Function Call：模型输出 JSON 描述调什么函数传什么参。外部框架截获执行后结果喂回。极简，但一次性，没有持久化工具管理。

MCP（Model Context Protocol）：Anthropic 2024 年发布。客户端-服务器架构。AI 宿主是客户端，每个工具封装成 MCP 服务器。服务器暴露统一接口，列出资源、描述参数、处理请求。一次开发，所有支持 MCP 的 AI 应用都能用。社区已有数百个现成服务器，Google Drive、GitHub、PostgreSQL。

A2A（Agent-to-Agent）：Google 2024 年发布。不是模型↔工具，是 Agent↔Agent。跨组织互操作，采购 Agent 跟供应商库存 Agent 确认交货时间。定义了发现、握手、任务分配、结果回传的标准流程。

Skill：预定义的 Prompt + 调用规范。MCP 是通用工具层，Skill 是场景化编排。两者互补。

---

### MCP 连接数据库的实际过程

假设 Claude 要通过 MCP 查 PostgreSQL 里的订单表。

**1. 启动时**：MCP 客户端（Claude 宿主）连接 PostgreSQL MCP 服务器。服务器暴露能力清单：

```json
{
  "tools": [
    {"name": "query", "description": "执行 SQL 查询", "parameters": {"sql": "string"}},
    {"name": "list_tables", "description": "列出所有表"}
  ]
}
```

**2. 用户提问**：「查一下 user_id=1088 昨天的订单总金额」

**3. 模型生成 Function Call**：

```json
{
  "tool": "query",
  "parameters": {
    "sql": "SELECT SUM(amount) FROM orders WHERE user_id = 1088 AND date = '2026-07-14'"
  }
}
```

**4. MCP 服务器执行**：连接数据库，跑 SQL，返回 `[{"sum": 456.80}]`

**5. 模型回答**：「用户 1088 昨天的订单总金额为 456.80 元。」

整个过程，模型不需要知道数据库地址、账号密码、表结构。MCP 服务器做了封装。换一个 MySQL 服务器，只要它实现了相同的 MCP 接口，模型代码零改动。

---

> 磨平一些信息差。
