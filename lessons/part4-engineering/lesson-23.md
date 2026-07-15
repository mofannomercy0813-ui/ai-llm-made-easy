# 第 23 课：MCP / A2A / Function Call，让模型会叫外援

Function Call：模型输出 JSON 描述调什么函数传什么参。外部框架截获执行后结果喂回。极简，但一次性，没有持久化工具管理。

MCP（Model Context Protocol）：Anthropic 2024 年发布。客户端-服务器架构。AI 宿主是客户端，每个工具封装成 MCP 服务器。服务器暴露统一接口，列出资源、描述参数、处理请求。一次开发，所有支持 MCP 的 AI 应用都能用。社区已有数百个现成服务器，Google Drive、GitHub、PostgreSQL。

A2A（Agent-to-Agent）：Google 2024 年发布。不是模型↔工具，是 Agent↔Agent。跨组织互操作，采购 Agent 跟供应商库存 Agent 确认交货时间。定义了发现、握手、任务分配、结果回传的标准流程。

Skill：预定义的 Prompt + 调用规范。MCP 是通用工具层，Skill 是场景化编排。两者互补。

---

## 追问模块

**追问：「MCP 和传统 API 的区别？」** 传统 API 每个工具一种格式。MCP 统一协议，所有工具同一种方式暴露和调用。

**追问：「A2A 和 MCP 冲突吗？」** 不冲突。MCP 是模型↔工具，A2A 是 Agent↔Agent。同一系统里共存。

---

## 思考题

1. 你有邮件、日历、Jira 三个工具，用 MCP 怎么封装它们的接口。

2. 两个公司 Agent 跨 A2A 协同，通信协议最少要哪些字段。

---

> 磨平一些信息差。
