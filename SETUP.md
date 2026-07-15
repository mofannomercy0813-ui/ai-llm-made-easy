# 仓库配置指南

## 1. 启用 DeepSeek Code Review

### 步骤 1：获取 DeepSeek API Key

前往 [platform.deepseek.com](https://platform.deepseek.com) 注册并获取 API Key。

### 步骤 2：添加 GitHub Secret

1. 打开仓库 Settings → Secrets and variables → Actions
2. 点击 "New repository secret"
3. Name 填 `CHAT_TOKEN`
4. Value 填你的 DeepSeek API Key（格式：`sk-xxxxxxxx`）
5. 点击 Add secret

### 步骤 3：验证

给仓库提一个 PR，DeepSeek 会自动在 PR 下评论 Code Review 结果。

## 2. 工作流说明

### 自动触发（已配置）

- 每当 PR 被创建、重新打开、或推送新 commit 时，自动运行
- 审查文件类型：`.md`, `.py`, `.html`, `.yml`, `.yaml`
- 单次最多审查 30000 字符

### 标签触发（可选）

如需改为手动触发（只审查打了 `ai review` 标签的 PR），将 workflow 文件的 `on` 部分替换为：

```yaml
on:
  pull_request_target:
    types:
      - labeled
```

并在 `jobs` 中添加条件：

```yaml
if: contains(github.event.pull_request.labels.*.name, 'ai review')
```

## 3. 成本预估

DeepSeek V3 单价：input ~$0.27/M tokens, output ~$1.10/M tokens
每次 PR 审查约 5000 input + 1000 output tokens → 约 $0.002
每天 10 个 PR → 约 $0.6/月

## 4. 本地手动 Review

```bash
# 安装 nushell（deepseek-review 依赖）
# macOS: brew install nushell
# Linux: 参考 https://www.nushell.sh/book/installation.html

# 设置环境变量
export CHAT_TOKEN=sk-xxxxxxxx

# Review 当前分支相对于 main 的改动
nu cr
```
