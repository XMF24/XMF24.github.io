# AI 资讯文字版

> 更新时间：2026-10-12 10:42 CST  
> 收录范围：2026-09-29 至 2026-10-09  
> 核验原则：官方原文优先，社交平台只用于发现线索。

## 本期结论

1. 模型竞争继续向“默认入口 + 交互界面”转移，OpenAI 将 GPT-6 与 Intelligent UI 面向所有 ChatGPT 用户推进。
2. AI 安全从内容审核延伸到关键基础设施、开源供应链和影响力行动处置。
3. 企业与政府合作进入多年期投入阶段，Anthropic 向 Genesis Mission 承诺三年 1.5 亿美元。
4. 产品创新从文本扩展至游戏生成；Google Playground 支持用文字提示创建、游玩和分享自定义游戏。
5. 平台生命周期变化同样重要：百度智能云将下线 5 项图像接口，开发者需要提前迁移。

## 8 条精选资讯

### 1. 百度智能云将下线 5 项图像接口，并停止 AI 修图新用户接入

- 时间：2026-10-09
- 来源：百度智能云 · 官方公告
- 核验：A · 官方原文核验
- 背景：大模型视觉能力正在取代部分单点传统图像 API。平台需要整合资源、降低维护面，同时给存量开发者留出迁移窗口。
- 内容：官方公告明确列出了 5 项下线接口和停止服务日期，并建议图像识别类业务评估使用“看图识万物”等替代能力。AI 修图接口停止更新，不再支持新用户接入。
- 影响：企业调用单点视觉模型时，需要把服务生命周期和迁移计划纳入 AI 技术债管理。
- 原文：https://cloud.baidu.com/support/news?action=detail&id=3287

### 2. Anthropic 三年投入 1.5 亿美元支持 Genesis Mission 科研计划

- 时间：2026-10-08
- 来源：Anthropic · 官方新闻室
- 核验：A · 官方原文核验
- 背景：政府科研机构希望利用 AI 加速聚变能、量子计算等长期难题，但模型、工程支持与科研工作流之间仍存在落地门槛。
- 内容：资金覆盖 NASA、NIH、NSF 等参与机构；Anthropic 将提供模型与 API 信用额度、科研培训、上手支持，并优先配合聚变能源和量子计算等项目。
- 影响：AI 实验室与公共科研体系的合作正在从试点访问升级为多年、跨机构的算力与工具投入。
- 原文：https://www.anthropic.com/news/genesis-mission-commitment

### 3. Anthropic 启动 Cyber Mission，重点保护关键基础设施与开源软件

- 时间：2026-10-08
- 来源：Anthropic · 官方新闻室
- 核验：A · 官方原文核验
- 背景：电网、水务、交通等行业依赖难以停机的运营技术。发现漏洞的速度正在提升，但漏洞验证、优先级排序和修复能力仍然不足。
- 内容：CIDP 将前沿 Claude 模型、现场工程师和威胁研究带给关键基础设施防御方；OSS Scanner 则提供定期开源安全扫描。创始合作方包括 Accenture、CrowdStrike、Deloitte、Palo Alto Networks、PwC 和 Rockwell Automation 等。
- 影响：前沿模型厂商正把安全能力从模型风控扩展到基础设施、开源供应链和防守方赋能。
- 原文：https://www.anthropic.com/news/anthropic-cyber-mission

### 4. OpenAI 阻断两起 AI 驱动的“虚假前线”舆论行动

- 时间：2026-10-08
- 来源：OpenAI · 官方 RSS
- 核验：A- · 官方原文核验 · 外部复核有限
- 背景：生成式 AI 降低了批量内容生产和身份伪装成本，平台需要同时识别账号网络、自动化行为和跨平台叙事协同。
- 内容：官方摘要确认行动涉及两起利用 AI 的影响操作，并使用了“false-front journalists”和智库等伪装形式。公开摘要没有披露全部账号规模、归因证据与跨平台影响范围。
- 影响：模型安全治理正在从有害内容审核延伸到影响力行动识别和组织化滥用处置。
- 原文：https://openai.com/index/disrupting-ai-enabled-false-front-operations

### 5. Google 推出实验性游戏平台 Playground，用文字提示生成可玩内容

- 时间：2026-10-07
- 来源：Google · 官方博客
- 核验：A · 官方原文核验
- 背景：生成式 AI 正从生成文本和图片转向生成可交互体验。把创作门槛降到自然语言，有助于测试用户生成内容与游戏分发的结合方式。
- 内容：Google 官方将其描述为实验性游戏平台，核心流程是文字提示生成自定义游戏，并支持创建、游玩与分享。当前定位强调实验性和低门槛，不等于成熟商业游戏引擎。
- 影响：交互式生成有望成为继图像、视频和代码之后，生成式 AI 的下一类高频消费场景。
- 原文：https://blog.google/innovation-and-ai/technology/ai/playground-experimental-gaming-platform/

### 6. OpenAI 面向所有 ChatGPT 用户推出 GPT-6 与 Intelligent UI

- 时间：2026-10-07
- 来源：OpenAI · 官方 RSS
- 核验：A · 官方 RSS 核验
- 背景：模型竞争正从纯文本生成转向多模态结果、工具调用与界面交互。OpenAI 需要把前沿能力下沉到大众产品，而不只是提供给 API 开发者。
- 内容：官方 RSS 确认的核心变化包括 GPT-6 全球逐步上线、Intelligent UI、更快响应、视觉内容以及交互式体验。具体地区、套餐和完整能力范围仍以 OpenAI 产品页面为准。
- 影响：AI 产品的差异化开始更多体现在界面如何组织模型能力，以及用户能否直接完成任务。
- 原文：https://openai.com/index/gpt-6-for-everyone

### 7. Google 复盘 9 月 AI 更新：Gemini 4 Argon 与 3.8 系列集中推进

- 时间：2026-10-02
- 来源：Google · 官方博客
- 核验：A · 官方原文核验
- 背景：Google 正把模型矩阵扩展到推理、Agent、语音、网络安全、科学和企业工作流，减少对单一聊天模型的依赖。
- 内容：官方汇总提到 Gemini 4 Argon 支持最高 100 万 token 输出，Gemini 3.8 系列面向推理、软件开发、网络安全和语音交互。科学与基础设施方向还包括 AlphaGenome Atlas、全球甲烷追踪和 Project Suncatcher。
- 影响：模型竞争开始按能力分层与应用场景组合推进，单次发布会更像产品矩阵更新。
- 原文：https://blog.google/innovation-and-ai/technology/ai/google-ai-updates-september-2026/

### 8. Microsoft 推出 Fabric IQ，把受治理业务语义接入 Copilot

- 时间：2026-09-29
- 来源：Microsoft · 官方博客
- 核验：A · 官方原文核验
- 背景：企业 AI 的主要风险之一不是模型不会回答，而是答案没有建立在统一、受治理的业务数据与指标口径上。
- 内容：Fabric IQ 让 Copilot 的回答基于组织已有的 Power BI 语义模型，并保留现有访问控制和治理。官方同时公布 Fabric Apps、跨工作区可观测性和 Agentic Data Engineering 等数据平台更新。
- 影响：企业 AI 的竞争重点正在从模型接入转向数据语义层、权限治理和可审计的执行环境。
- 原文：https://blogs.microsoft.com/blog/2026/09/28/new-microsoft-data-innovations-unlock-what-only-your-business-knows/

## 核验说明

- 7 条为 `A` 级：官方原文能够确认核心事实。
- 1 条为 `A-` 级：OpenAI 对影响力行动的处置由官方披露，但规模、归因和跨平台影响仍缺少独立复核。
- OpenAI 两条页面因站点风控对自动访问返回 403，标题、摘要、日期和链接已通过官方 RSS 核验。
- Google Playground 页面通过直接访问确认 HTTP 200；自动检查脚本因网络波动返回超时，已人工复核。
