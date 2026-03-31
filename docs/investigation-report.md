# ARIS 项目深度调研报告

> **调研目标**：验证 ARIS (Auto-claude-code-research-in-sleep) 声称"全自动生成 CCF B 级别论文，无需人工干预"的真实性
>
> **调研时间**：2026-03-30
> **调研方法**：多维度并行分析（技术架构、效果验证、局限性、社区反馈）

---

## 执行摘要

| 评估维度 | 结论 | 置信度 |
|---------|------|--------|
| **技术架构** | 设计精巧的跨模型协作框架，但非真正"自主" | 高 |
| **CCF-B 论文声称** | **证据薄弱，无法验证** | 高 |
| **全自动声称** | **营销夸大，需大量人工干预** | 高 |
| **社区认可度** | 中文社区活跃，但项目仅3周历史 | 中 |
| **整体可信度** | 有价值的工具，但营销过度 | 高 |

**核心结论**：ARIS 是一个设计精良的研究辅助工具，但"全自动生成 CCF-B 论文"的声称属于**营销夸大**。实际使用中需要大量人工干预、昂贵的 API 费用，且目前缺乏可验证的顶级会议接受记录。

---

## 1. 项目概述

### 1.1 什么是 ARIS

ARIS 是一个基于 Claude Code 的科研自动化框架，通过 Markdown 格式的 "Skills" 来编排多模型协作的研究工作流。

**核心机制**：
- **执行者**：Claude Code（快速执行）
- **审稿者**：GPT-5.4 via Codex MCP（慢速严谨审稿）
- **理念**：跨模型对抗式审稿，避免单模型自我博弈的盲区

### 1.2 声称的能力

根据 README：
> "🌙 **让 Claude Code 在你睡觉时做科研。** 醒来发现论文已被打分、弱点已被定位、实验已跑完、叙事已重写——全自动。"

**四个工作流**：
1. **Workflow 1** (`/idea-discovery`): 文献调研 → 想法生成 → 新颖性检查
2. **Workflow 1.5** (`/experiment-bridge`): 代码实现 → GPU 部署 → 实验执行
3. **Workflow 2** (`/auto-review-loop`): 自动审稿 → 修复 → 再审（4轮迭代）
4. **Workflow 3** (`/paper-writing`): 叙事 → 大纲 → 图表 → LaTeX → PDF

### 1.3 声称的成果

| 论文 | 评分 | 会议 | 技术栈 |
|------|------|------|--------|
| CS Paper | **8/10** "clear accept" | CS Conference | Claude + GPT-5.4 |
| AAAI 2026 | **7/10** "good paper, accept" | AAAI 2026 Main | Pure Codex CLI |

---

## 2. 技术架构分析

### 2.1 Skills 系统设计

**优点**：
- **极度轻量**：纯 Markdown，零依赖，零锁定
- **高度可移植**：可在 Claude Code、Codex CLI、Cursor、Trae 等多平台运行
- **声明式**：Skill 是描述性指令，非编译代码

**缺点**：
- **无状态机**：工作流程依赖 LLM 理解并执行，无强制执行机制
- **易受 LLM 幻觉影响**：如果 LLM 误解指令，无纠正机制
- **上下文窗口限制**：长工作流会触发 "compact 模式" 进行状态压缩

### 2.2 跨模型协作架构

```
┌─────────────────┐     MCP      ┌──────────────────┐
│  Claude Code    │ ◄──────────► │  Review Server   │
│  (执行者)        │  JSON-RPC    │  (外部 LLM)      │
└─────────────────┘              └──────────────────┘
```

**MCP 服务器类型**：
- `claude-review`: Claude 作为审稿人
- `gemini-review`: Gemini 作为审稿人
- `llm-chat`: 通用 OpenAI 兼容 API
- `minimax-chat`: MiniMax M2.7 模型

**技术评价**：跨模型协作架构设计合理，确实能避免单模型自我审稿的盲区。

### 2.3 真正自动化的程度

| 任务 | 自动化程度 | 需人工干预？ |
|------|-----------|------------|
| 文献检索 | ✅ 完全自动 | 否 |
| 想法生成 | ✅ 完全自动 | 可选（`AUTO_PROCEED`） |
| 代码实现 | ⚠️ 半自动 | 复杂架构需人工 |
| GPU 实验部署 | ✅ 自动（配置后） | 初始配置需人工 |
| 实验监控 | ✅ 自动 | 否 |
| LaTeX 生成 | ✅ 自动 | 否 |
| **最终投稿** | ❌ 不支持 | **必须人工** |
| **Rebuttal 提交** | ❌ 不支持 | **必须人工** |

**关键发现**：
> "Currently the orchestration layer requires an active CLI session... relaunch is manual."
>
> —— 项目文档

这意味着**无法真正做到"睡觉时运行"**，需要保持活跃会话。

---

## 3. 论文接受声称验证

### 3.1 声称的论文

#### 声称 1：CS Paper (8/10)
- **会议**：仅写 "CS Conference"，无具体名称
- **证据**：一张模糊的截图，无法辨认内容
- **CCF 等级**：无法验证（不知道是哪会议）

#### 声称 2：AAAI 2026 (7/10)
- **会议**：AAAI 2026 Main Technical
- **证据**：截图显示 "Mar 21, 2026" 和 "Gemini-33-Pro" 水印
- **问题**：
  - **日期在未来**：2026年3月，截图显示的是未来日期
  - **AAAI 时间线异常**：AAAI 2026 的审稿应在2025年底完成
  - **非官方界面**：显示的是 Gemini 模型界面，非会议审稿系统

### 3.2 评分数据的本质

**重要区分**：
- README 中的评分（5.0 → 7.5）是 **GPT-5.4 自我评分**，非真实审稿人评分
- "真实测试" 明确标注是 **ICLR 2026 theory paper 测试**，非真实接受的论文

| 评分来源 | 实际含义 | 可信度 |
|---------|---------|--------|
| GPT-5.4 自我评分 | 模型对自己生成内容的评估 | 低 |
| 截图中的评分 | 来源不明，日期异常 | 可疑 |
| 真实审稿人评分 | 未提供任何链接或证据 | 无 |

### 3.3 CCF-B 声称的问题

1. **AAAI 是 CCF-A，非 CCF-B**
   - 在 CCF 推荐列表中，AAAI 属于 A 类会议
   - 项目声称 "CCF B 级别"，但例子是 CCF-A

2. **"CS Conference" 无法验证**
   - 未提供会议全称
   - 无法查询 CCF 等级

### 3.4 验证结论

| 声称 | 验证结果 | 说明 |
|------|---------|------|
| 8/10 CS Paper | ❌ 无法验证 | 无论文链接、无会议名称 |
| 7/10 AAAI 2026 | ❌ 高度可疑 | 日期在未来，界面非官方 |
| CCF-B 级别 | ❌ 不成立 | 例子是 CCF-A，或无会议名 |
| "已接受" | ❌ 无证据 | 无 citation、无 DOI、无 arXiv |

---

## 4. 局限性与风险分析

### 4.1 技术局限

#### 上下文窗口限制
```markdown
# 项目文档中明确承认：
"Compact mode — generate lean summary files for short-context models
 and session recovery"
```

长工作流会触发 "compact recovery"，信息可能丢失。

#### 无守护进程模式
无法真正做到后台运行，需要保持 CLI 会话活跃。

#### GPU 小时限制
超过 4 GPU 小时的实验会被标记为需人工跟进，非全自动。

### 4.2 幻觉风险

**反幻觉措施**：
| 措施 | 实现 | 局限 |
|------|------|------|
| DBLP/CrossRef 引用 | 自动获取真实 BibTeX | 仅验证引用，不验证实验结果 |
| Cross-model 审稿 | GPT-5.4 审 Claude 输出 | 同源数据，可能有共同盲区 |
| Safety gates | 3道安全门 | 事后检查，非事前预防 |

**关键风险**：
> "Step 4: Validate the Claim... is the step people most often skip
> and the step that matters the most."
>
> —— citation-discipline.md

实验结果可能被错误解析，但系统无法自动发现。

### 4.3 实际成本

| 成本项 | 估算费用 |
|--------|---------|
| Claude Code Pro | $20/月 |
| GPT-5.4 (Codex) | $5-20/轮审稿 |
| 完整 4 轮审稿 | $20-80 |
| 全流程 pipeline | $50-200+/篇 |
| Vast.ai GPU | $0.28-0.95/小时 |

**关键发现**：
项目承认 "⭐ We strongly recommend Claude + GPT-5.4 (default setup)...
Alternative setups work but may require prompt tuning."

"免费替代方案"（ModelScope）效果可能不佳。

### 4.4 学术伦理问题

**披露要求**：
- 项目提到 ICLR 的 LLM 披露政策
- **但**：不自动生成披露声明
- **但**：不追踪 AI 生成 vs 人工撰写内容

**关键问题**：
1. 谁应该是 AI 生成论文的"作者"？
2. 投稿时是否披露 AI 使用？如何披露？
3. 生成的论文能通过严格的同行评议吗？

---

## 5. 社区与外部验证

### 5.1 项目历史

| 指标 | 数据 |
|------|------|
| 创建时间 | ~2026-03-10（约3周历史） |
| Commits | 400+ |
| 合并 PR | 30+ |
| Contributors | 20+ |

**关键发现**：项目非常年轻（3周），但声称已有论文被接受。

### 5.2 外部认可验证

| 声称认可 | 验证结果 |
|---------|---------|
| PaperWeekly 收录 | ✅ **已验证** - 中国知名 AI 媒体 |
| awesome-agent-skills | ❌ **未验证** - 未在 VoltAgent 仓库中找到 |
| AI Digital Crew | ❌ **无法验证** - 网站显示 "0 projects" |
| Sohu Tech 报道 | ✅ **已验证** - 搜狐科技报道 |

### 5.3 社区贡献

**已验证的社区 Skills**：
- `research-refine` (@zjYao36)
- `paper-poster` (@dengzhe-hou)
- `formula-derivation` (@Falling-Flower)
- `paper-slides` (社区贡献)

**外部项目**：
- `open-source-hardening-skills` (@zeyuzhangzyz) - 明确提及与 ARIS 配合使用

### 5.4 社区活跃度

- **GitHub**: 高度活跃，日更
- **WeChat**: 主要社区，但封闭（中文为主）
- **文档**: 非常详尽（中英双语）

---

## 6. 关键发现总结

### 6.1 项目实际能力

| 能力 | 实际水平 | 与声称对比 |
|------|---------|-----------|
| 文献调研 | ⭐⭐⭐⭐ 良好 | 符合声称 |
| 想法生成 | ⭐⭐⭐ 中等 | 需人工筛选 |
| 代码实现 | ⭐⭐⭐ 中等 | 标准模式可用，新颖架构困难 |
| 实验执行 | ⭐⭐⭐⭐ 良好 | 需预配置 |
| 论文写作 | ⭐⭐⭐⭐ 良好 | LaTeX 生成能力强 |
| **全自动** | ⭐⭐ 有限 | **远低于声称** |
| **CCF-B 论文** | ❓ 无法验证 | **无可靠证据** |

### 6.2 营销 vs 现实

| 营销声称 | 现实 |
|---------|------|
| "睡觉时做科研，醒来收论文" | 需保持 CLI 会话活跃，无法真正后台运行 |
| "全自动，无需人工干预" | 多处需人工检查点，最终投稿必须人工 |
| "生成 CCF-B 级别论文" | 无验证的论文链接，声称的例子是 CCF-A |
| "8/10 clear accept" | 自我评分，非真实审稿人评分 |

### 6.3 真实的价值

ARIS **确实有价值**的地方：
1. ✅ 结构化的科研工作流程
2. ✅ 跨模型审稿减少盲区
3. ✅ 反幻觉引用机制（DBLP/CrossRef）
4. ✅ 丰富的社区贡献
5. ✅ 详尽的文档

ARIS **被夸大**的地方：
1. ❌ "全自动" - 需要大量人工干预
2. ❌ "CCF-B 论文" - 缺乏可验证证据
3. ❌ "睡觉时运行" - 技术上不可行
4. ❌ "无需人工干预" - 多处检查点

---

## 7. 结论与建议

### 7.1 总体评价

| 维度 | 评分 | 说明 |
|------|------|------|
| 技术设计 | 8/10 | 跨模型协作架构合理 |
| 实现质量 | 7/10 | 功能丰富但依赖 LLM 稳定性 |
| 文档质量 | 9/10 | 非常详尽 |
| 声称可信度 | 4/10 | 过度营销 |
| 社区活跃度 | 8/10 | 年轻但活跃 |

### 7.2 回答原始问题

> **"作者说可以全自动生成 CCF B 级别的论文，无需人工干预，真的吗？"**

**答案：不是真的。**

具体而言：

1. **"全自动"**：❌ 假
   - 需要人工配置、检查点确认、最终投稿
   - 无法真正"睡觉时运行"

2. **"CCF B 级别"**：❌ 无法验证
   - 声称的例子是 CCF-A（AAAI）
   - 无论文链接、无 DOI、无 citation
   - 截图证据有日期异常问题

3. **"无需人工干预"**：❌ 假
   - 多处 `HUMAN_CHECKPOINT` 可配置
   - 复杂实验需人工介入
   - 图表需人工绘制（约 40%）

4. **"生成论文"**：⚠️ 部分真
   - 能生成结构良好的 LaTeX 论文
   - 质量取决于输入和迭代轮数
   - 不保证接受率

### 7.3 使用建议

**适合使用 ARIS 的情况**：
- ✅ 已有研究方向，需要加速实验和写作
- ✅ 熟悉 LLM 工具，能判断输出质量
- ✅ 有预算支付 API 费用
- ✅ 将 ARIS 视为"助手"而非"替代品"

**不适合使用 ARIS 的情况**：
- ❌ 期望完全自动化，无需人工干预
- ❌ 期望保证 CCF-B/AAAI 等顶会接受
- ❌ 无法接受 API 费用
- ❌ 缺乏领域知识判断输出质量

### 7.4 伦理建议

如使用 ARIS 辅助论文写作：
1. **披露 AI 使用**：遵循目标会议/期刊的 LLM 披露政策
2. **人工审核**：不提交未经仔细审核的生成内容
3. **负责任使用**：将 ARIS 视为工具，非论文作者

---

## 附录 A：调研方法

本次调研采用多 Agent 并行分析：

1. **技术架构分析 Agent**：分析 Skills 系统、MCP 架构、工作流实现
2. **效果验证 Agent**：验证论文接受声称、评分数据来源
3. **局限性分析 Agent**：识别技术局限、风险、伦理问题
4. **社区调研 Agent**：分析 GitHub 活动、外部认可、社区反馈

所有 Agent 独立运行，结果交叉验证。

## 附录 B：关键文档引用

- 项目 README（中英双语）
- Skills 文档（`SKILL.md` 文件）
- MCP 服务器实现代码
- 社区贡献指南

## 附录 C：术语表

| 术语 | 解释 |
|------|------|
| ARIS | Auto-claude-code-research-in-sleep |
| CCF | 中国计算机学会（China Computer Federation） |
| MCP | Model Context Protocol |
| Skill | ARIS 的基本功能单元，Markdown 格式 |
| Workflow | 多个 Skill 组成的流水线 |

---

## 8. OpenAI Codex Plugin for Claude Code (2026-03-31 新发布)

### 8.1 发现概述

**重大发现**：OpenAI 于 **2026-03-30** 发布了 `codex-plugin-cc` 插件，允许 Claude Code 用户直接调用 OpenAI Codex 进行代码审查和任务委托。

| 指标 | 数据 |
|------|------|
| 仓库 | `openai/codex-plugin-cc` |
| 创建时间 | 2026-03-30T15:29:52Z |
| Stars | **4301** (一天内暴涨) |
| Forks | 166 |
| Language | JavaScript |
| License | Apache-2.0 |
| 描述 | "Use Codex from Claude Code to review code or delegate tasks." |

### 8.2 核心功能

该插件提供以下 slash commands：

| 命令 | 功能 | 说明 |
|------|------|------|
| `/codex:review` | 正常代码审查 | 只读审查，与 Codex 直接运行 `/review` 同质量 |
| `/codex:adversarial-review` | 挑战式审查 | 可操控的审查，质疑设计决策、假设、风险 |
| `/codex:rescue` | 任务委托 | 将任务交给 Codex 子代理处理 |
| `/codex:status` | 任务状态 | 查看运行中的 Codex 任务 |
| `/codex:result` | 任务结果 | 获取完成的任务输出 |
| `/codex:cancel` | 取消任务 | 取消正在运行的后台任务 |
| `/codex:setup` | 安装配置 | 检查 Codex 安装和认证状态 |

### 8.3 安装步骤

```bash
# 添加 marketplace
/plugin marketplace add openai/codex-plugin-cc

# 安装插件
/plugin install codex@openai-codex

# 重载插件
/reload-plugins

# 配置
/codex:setup
```

**前置要求**：
- ChatGPT 订阅（含免费版）或 OpenAI API key
- Node.js 18.18+
- Codex CLI (`npm install -g @openai/codex`)
- 运行 `!codex login` 进行认证

### 8.4 使用场景

#### Review Before Shipping
```bash
/codex:review                # 审查当前未提交改动
/codex:review --base main    # 与 main 分支对比审查
/codex:review --background   # 后台运行
```

#### 委托任务给 Codex
```bash
/codex:rescue investigate why the tests started failing
/codex:rescue fix the failing test with the smallest safe patch
/codex:rescue --resume apply the top fix from the last run
/codex:rescue --model gpt-5.4-mini --effort medium investigate the flaky test
/codex:rescue --background investigate the regression
```

#### 挑战式审查
```bash
/codex:adversarial-review --base main challenge whether this was the right caching design
/codex:adversarial-review --background look for race conditions
```

### 8.5 Review Gate 功能

**警告功能**：可以启用 review gate，在 Claude 响应后自动运行 Codex 审查，发现问题会阻止提交。

```bash
/codex:setup --enable-review-gate
```

> ⚠️ **警告**：Review gate 可能创建长时间 Claude/Codex 循环，快速消耗用量限制。

### 8.6 与 ARIS 的关系

**关键洞察**：这个插件与 ARIS 项目有重要关联：

| 对比项 | ARIS | Codex Plugin |
|--------|------|--------------|
| 审稿模型 | GPT-5.4 via Codex MCP | Codex (OpenAI) |
| 代码审查 | `/auto-review-loop` | `/codex:review` |
| 任务委托 | 手动配置 MCP | `/codex:rescue` |
| 官方支持 | ❌ 社区项目 | ✅ OpenAI 官方 |
| 安装复杂度 | 高（需配置 MCP） | 低（plugin install） |

**意义**：
- OpenAI 官方认可 Claude Code 作为 Codex 的调用入口
- ARIS 的跨模型审稿理念被官方采纳
- 大大简化了在 Claude Code 中使用 Codex 的流程

### 8.7 模型配置

可以通过 Codex config 改变默认模型和推理强度：

```toml
# ~/.codex/config.toml 或 .codex/config.toml
model = "gpt-5.4-mini"
model_reasoning_effort = "xhigh"
```

支持的模型别名：
- `spark` → `gpt-5.3-codex-spark`（快速便宜）

### 8.8 技术架构

```
┌─────────────────┐     Plugin     ┌──────────────────┐     CLI      ┌─────────────┐
│  Claude Code    │ ◄───────────► │  Codex Plugin    │ ◄──────────► │  Codex CLI  │
│  (宿主)         │   JSON-RPC    │  (bridge)        │   子进程      │  (OpenAI)   │
└─────────────────┘              └──────────────────┘              └─────────────┘
```

**特点**：
- 使用本地 Codex CLI，共享认证状态
- 共享 Codex config 配置
- 任务可在 Codex CLI 中直接 resume

### 8.9 验证结论

| 声称 | 验证结果 |
|------|---------|
| 官方 OpenAI 发布 | ✅ **已验证** - 在 `openai` 组织下 |
| 与 Claude Code 集成 | ✅ **已验证** - README 清晰说明 |
| 4300+ Stars | ✅ **已验证** - GitHub API 确认 |
| 代码审查功能 | ✅ **已验证** - 功能完整 |
| 后台任务支持 | ✅ **已验证** - `/codex:rescue --background` |

---

*报告更新时间：2026-03-31*
*调研团队：aris-investigation + codex-plugin-research*
