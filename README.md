# AI Signal · 可核验 AI 资讯站

一个可直接打开的高级蓝白调静态网站原型，聚合并人工提炼 OpenAI、Google、Microsoft、Anthropic、百度智能云、腾讯混元等公开渠道信息。当前版本收录 8 条资讯，每条都包含时间、背景、内容、来源、核验等级与原始链接。

## 直接预览

在目录内启动一个静态服务器：

```bash
python3 -m http.server 4173
```

然后访问 <http://localhost:4173>。也可以直接打开 `index.html`；本站使用 `data/news.js` 保证 `file://` 预览可用。

## 目录

- `index.html`：页面结构
- `assets/styles.css`：高级蓝白视觉、响应式布局与动效
- `assets/app.js`：搜索、分类筛选、精选卡片和时间线渲染
- `data/news.json`：人工精编后的唯一内容源
- `data/news.js`：供纯静态页面直接读取的同源数据
- `scripts/collect_news.py`：从官方 RSS、Newsroom、Sitemap 和公告页抓取候选元数据
- `scripts/verify_sources.py`：批量检查原文链接可达性
- `scripts/sync_news_js.py`：从 JSON 重新生成 `news.js`

## 更新流程

```bash
python3 scripts/collect_news.py
python3 scripts/verify_sources.py
```

`collect_news.py` 只生成 `data/collected.json` 候选池，不会自动发布。编辑者需要逐条回到原始页面核验，再修改 `data/news.json`，最后执行：

```bash
python3 scripts/sync_news_js.py
```

## 核验原则

1. 机构公告优先使用官网、官方博客、Newsroom、官方 RSS、Sitemap 或开源仓库。
2. 日期、数字、功能边界和身份称谓必须有原始来源；无法确认的内容明确标注“待核验”或直接不发布。
3. 知乎、微博、微信公众号用于发现讨论线索，不直接作为事实层来源。
4. 厂商内部评测标注为待第三方复测；科研成果标注“早期结果 / 待同行评审”。
5. 社交平台链接只进入选题池，通过一级来源确认后才可进入首页精选。

## 接入生产环境时的建议

当前是静态预览。生产版建议增加定时任务、原文快照、变更记录、事实核验队列、人工审核后台和发布记录。页面数据结构已经按这些字段拆分，可直接迁移到数据库或 Headless CMS。
