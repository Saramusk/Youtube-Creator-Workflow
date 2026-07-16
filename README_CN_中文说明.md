# SARA YouTube 达人开发工作流 Skill

一个可重复使用的 YouTube 达人开发工作流 Skill，可根据产品关键词完成达人搜索、频道筛选、资格评估、数据导出、批次合并以及飞书多维表格同步。

该仓库将 OpenAI / Codex Skill 定义与一套内置 Python 工作流结合起来，适用于品牌市场团队、海外达人营销团队和 KOL 开发人员，用于建立标准化、可复用、可扩展的 YouTube 达人开发流程。

## 项目功能

- 根据一个或多个产品关键词搜索 YouTube
- 收集相关视频、频道及达人数据
- 按照可配置规则筛选视频和频道
- 支持品牌、频道和竞品排除名单
- 输出结构化 Excel 达人数据表
- 将多个搜索批次合并为标准业务工作簿
- 可选择同步至飞书 / Lark 多维表格
- 提供初始化脚本、配置示例、测试文件和操作文档
- 支持本地运行、批量搜索和自动化达人开发

## 适用场景

本项目适用于：

- YouTube 达人搜索
- 海外 KOL 开发
- 品牌达人资源库搭建
- 根据产品关键词寻找垂类创作者
- 达人频道资格评估与筛选
- 达人外联前的数据准备
- 达人名单批量导出
- 飞书达人数据库同步
- 标准化达人开发工作流搭建

## 仓库结构

```text
.
├── agents/
│   └── openai.yaml
├── assets/
│   └── yt-kol-workflow/
│       ├── config.py
│       ├── main.py
│       ├── requirements.txt
│       ├── channel_taxonomy.json
│       ├── brand_exclusions.example.json
│       ├── keywords.example.txt
│       ├── export/
│       ├── feishu/
│       ├── filter/
│       ├── tests/
│       ├── utils/
│       ├── workflow/
│       └── youtube/
├── references/
│   └── workflow-operations.md
├── scripts/
│   └── bootstrap_workflow.py
├── SKILL.md
├── LICENSE
└── README.md
```

## 快速开始

### 1. 初始化工作流

在仓库根目录运行：

```bash
python scripts/bootstrap_workflow.py \
  --target /path/to/yt-kol-workflow \
  --install-deps
```

初始化脚本会自动完成：

- 复制内置 YouTube 达人开发工作流
- 根据示例文件创建本地配置文件
- 创建 Python 虚拟环境
- 安装项目依赖
- 创建本地关键词文件
- 创建品牌排除配置文件

### 2. 进入项目目录

```bash
cd /path/to/yt-kol-workflow
source .venv/bin/activate
python main.py --help
```

Windows 用户可使用：

```bash
.venv\Scripts\activate
python main.py --help
```

## 配置 YouTube API Key

打开项目目录中的 `.env` 文件，并添加：

```env
YOUTUBE_API_KEY=your_youtube_api_key
```

请将 `your_youtube_api_key` 替换为真实的 YouTube Data API Key。

请勿将以下内容上传至 GitHub：

- `.env`
- YouTube API Key
- 飞书 App Secret
- 飞书 App Token
- Access Token
- Webhook URL
- 任何真实账号凭证

如果 API Key 曾出现在截图、日志或公开仓库中，请立即前往 Google Cloud 控制台撤销并重新生成。

## 配置搜索关键词

编辑本地 `keyword.txt` 文件，每行填写一个关键词。

示例：

```text
baby monitor
baby car monitor
video baby monitor
newborn essentials
parenting products
```

也可以使用中文关键词：

```text
婴儿监视器
车载婴儿监视器
无线婴儿监视器
新生儿用品
母婴产品
```

建议：

- 每行仅填写一个关键词
- 使用明确的产品词或场景词
- 避免一次加入过多宽泛关键词
- 可按国家、产品、使用场景分别建立关键词组

## 本地运行达人搜索

建议先在本地运行，不直接同步飞书：

```bash
python main.py batch \
  --keywords-file keyword.txt \
  --sort-order relevance \
  --yes \
  --no-feishu
```

参数说明：

| 参数 | 说明 |
|---|---|
| `batch` | 批量执行关键词搜索 |
| `--keywords-file` | 指定关键词文件 |
| `--sort-order relevance` | 按相关性排序 |
| `--yes` | 自动确认执行 |
| `--no-feishu` | 本次运行不同步飞书 |

## 预期输出文件

每次批量运行后，系统会在 `output/` 目录生成带时间戳的批次文件夹。

示例：

```text
output/<timestamp>_batch/
```

主要输出文件包括：

```text
output/<timestamp>_batch/search_tasks_all.xlsx
output/<timestamp>_batch/search_videos_all.xlsx
output/<timestamp>_batch/influencers_all.xlsx
output/<timestamp>_batch/influencer_videos_all.xlsx
```

对应四张核心业务表：

| 文件 | 业务用途 |
|---|---|
| `search_tasks_all.xlsx` | 记录关键词、搜索任务及执行状态 |
| `search_videos_all.xlsx` | 保存搜索到的视频数据 |
| `influencers_all.xlsx` | 保存达人及频道详情 |
| `influencer_videos_all.xlsx` | 保存达人与视频之间的关联数据 |

## 合并批次结果

将一个搜索批次合并为标准化工作簿：

```bash
python main.py merge-output \
  output/<timestamp>_batch \
  --output output/summary_<timestamp>/kol_summary_tables.xlsx
```

合并完成后，会生成：

```text
output/summary_<timestamp>/kol_summary_tables.xlsx
```

该工作簿包含四张标准业务数据表，可用于：

- 团队内部复盘
- 达人筛选
- 达人外联
- 达人资源库管理
- 飞书数据同步
- 后续人工补充与跟进

## 同步至飞书 / Lark 多维表格

### 1. 初始化飞书目标

首次使用飞书同步时运行：

```bash
python main.py feishu-setup
```

该命令会：

- 安装或调用 `lark-cli`
- 打开浏览器完成 OAuth 授权
- 创建或复用一个飞书多维表格
- 创建或检查四张标准数据表

默认数据表包括：

- 搜索任务表
- 视频数据表
- 达人详情表
- 达人视频表

### 2. 同步工作簿

```bash
python main.py sync-workbook \
  --workbook output/summary_<timestamp>/kol_summary_tables.xlsx \
  --cleanup-empty-rows
```

`--cleanup-empty-rows` 用于清理同步过程中产生的空白记录。

## 飞书授权说明

如果同步时提示缺少以下权限：

- `bitable:app:readonly`
- `bitable:app`
- `base:record:retrieve`

请重新授权：

```bash
lark-cli --profile kol-workflow auth login \
  --scope 'bitable:app:readonly bitable:app base:record:retrieve'
```

完成授权后，再次运行同步命令。

## 本地配置文件

以下文件属于本地运行配置，不应直接提交真实版本：

```text
.env
keyword.txt
brand_exclusions.json
```

仓库中建议仅保留示例文件：

```text
.env.example
keywords.example.txt
brand_exclusions.example.json
```

### 品牌排除配置

`brand_exclusions.json` 可用于排除：

- 竞品官方频道
- 品牌自营频道
- 不符合开发要求的频道
- 已合作达人
- 黑名单达人
- 重复或无效频道

请勿将包含敏感业务信息的真实排除名单上传到公开仓库。

## 推荐 `.gitignore`

建议在仓库根目录创建 `.gitignore`：

```gitignore
# 环境变量与密钥
.env
.env.*
!.env.example

# Python 虚拟环境
.venv/
venv/
env/

# Python 缓存
__pycache__/
*.py[cod]
*.pyo
*.pyd

# 本地配置
keyword.txt
keywords.txt
brand_exclusions.json

# 输出文件
output/
*.xlsx
*.xls
*.csv
*.log

# 测试与缓存
.pytest_cache/
.mypy_cache/
.coverage
htmlcov/

# 系统文件
.DS_Store
Thumbs.db

# 编辑器文件
.vscode/
.idea/
```

## GitHub 上传前安全检查

在 Skill 根目录运行：

```bash
rg -n 'AI[z]a|YOUTUBE_API_KEY=AI[z]a|FEISHU_APP_SECRET=.{8,}|FEISHU_APP_TOKEN=.{8,}|old-upstream-owner' .
```

检查不应上传的文件：

```bash
find . \
  -name '.env' \
  -o -name '*.xlsx' \
  -o -path '*/output/*' \
  -o -path '*/.venv/*' \
  -o -path '*/.git/*'
```

上传前请确认：

- 不存在真实 YouTube API Key
- 不存在飞书 App Secret
- 不存在飞书 App Token
- 不存在 Access Token
- 不存在真实达人 Excel 数据
- 不存在 `.env`
- 不存在虚拟环境目录
- 不存在旧项目所有者名称
- 示例文件仅保留占位符

## 常见问题

### 缺少 YouTube API Key

报错提示找不到 YouTube Key 时，请检查 `.env`：

```env
YOUTUBE_API_KEY=你的真实API密钥
```

保存后重新激活虚拟环境并运行命令。

### macOS 中看不到 `.env`

`.env` 是隐藏文件。

在 Finder 中按：

```text
Command + Shift + .
```

即可显示隐藏文件。

### 飞书 CLI 安装失败

可手动运行：

```bash
npx --yes @larksuite/cli@latest install
```

然后重新执行：

```bash
python main.py feishu-setup
```

### 飞书只创建了部分数据表

如果第一次飞书初始化被中断，可能只创建部分表。

重新运行：

```bash
python main.py feishu-setup
```

系统会继续创建或复用缺失的数据表。

### 飞书同步提示权限不足

重新授权：

```bash
lark-cli --profile kol-workflow auth login \
  --scope 'bitable:app:readonly bitable:app base:record:retrieve'
```

授权完成后，再次执行 `sync-workbook`。

### 搜索结果过多或不精准

建议：

- 缩小关键词范围
- 使用更明确的产品词
- 加入使用场景
- 增加频道分类规则
- 更新品牌排除名单
- 优先使用 `relevance` 排序
- 分批执行不同关键词组

### 输出文件没有生成

请检查：

- 虚拟环境是否已激活
- `requirements.txt` 是否安装完成
- `.env` 是否配置正确
- 关键词文件路径是否正确
- YouTube API 是否达到配额限制
- `output/` 是否具有写入权限

## 标准工作流程

建议按照以下顺序运行：

```text
1. 配置 YouTube API Key
2. 编辑 keyword.txt
3. 更新品牌排除规则
4. 本地执行批量搜索
5. 检查搜索结果
6. 合并批次工作簿
7. 人工复核达人名单
8. 同步飞书多维表格
9. 进入达人外联与跟进阶段
```

对应命令：

```bash
python main.py batch \
  --keywords-file keyword.txt \
  --sort-order relevance \
  --yes \
  --no-feishu

python main.py merge-output \
  output/<timestamp>_batch \
  --output output/summary_<timestamp>/kol_summary_tables.xlsx

python main.py feishu-setup

python main.py sync-workbook \
  --workbook output/summary_<timestamp>/kol_summary_tables.xlsx \
  --cleanup-empty-rows
```

## 项目文档

- Skill 定义：`SKILL.md`
- 操作说明：`references/workflow-operations.md`
- 内置项目：`assets/yt-kol-workflow`
- 初始化脚本：`scripts/bootstrap_workflow.py`

## 项目定位

该项目不是单纯的 YouTube 数据抓取工具，而是一套用于品牌达人营销团队的标准化达人开发工作流。

它从产品关键词出发，覆盖：

```text
关键词准备
→ YouTube 搜索
→ 视频筛选
→ 频道识别
→ 达人资格评估
→ 品牌排除
→ 数据导出
→ 批次合并
→ 飞书同步
→ 达人外联
```

## 数据与隐私说明

本项目可能处理达人公开频道信息、视频数据、业务关键词和内部筛选规则。

使用时请确保：

- 遵守 YouTube API 服务条款
- 遵守适用的数据保护法规
- 不公开内部达人名单
- 不公开品牌排除规则
- 不上传包含个人隐私的数据
- 不将真实账号密钥提交至公开仓库

## 开源许可

具体许可条款请查看：

```text
LICENSE
```

在公开发布或二次分发前，请确认当前 `LICENSE` 内容符合你的使用和授权要求。

## 项目名称

推荐仓库名称：

```text
youtube-creator-workflow
```

推荐项目描述：

```text
一个用于 YouTube 达人开发的工作流 Skill，支持关键词搜索、频道筛选、品牌排除、达人评估、Excel 导出、批次合并及飞书同步。
```
