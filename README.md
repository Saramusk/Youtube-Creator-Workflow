[README.md](https://github.com/user-attachments/files/30077093/README.md)# YouTube KOL Workflow Skill

A reusable workflow skill for discovering, filtering, qualifying, exporting, and managing YouTube creators based on product keywords.

The repository combines a Codex/OpenAI skill definition with a bundled Python workflow that searches YouTube, evaluates creator channels, exports structured Excel workbooks, and optionally syncs normalized creator data to Feishu/Lark Bitable.

## What It Does

- Searches YouTube using one or more product keywords
- Collects matching video and channel data
- Filters videos and creator channels using configurable rules
- Supports brand and channel exclusion lists
- Produces structured Excel workbooks for creator development
- Merges batch results into four standardized business tables
- Optionally syncs creator data to Feishu/Lark Bitable
- Includes setup scripts, tests, configuration examples, and operating documentation

## Repository Structure

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
└── README.md
```

## Quick Start

### 1. Bootstrap the workflow

Run the helper from the repository root:

```bash
python scripts/bootstrap_workflow.py \
  --target /path/to/yt-kol-workflow \
  --install-deps
```

The bootstrap script copies the bundled workflow, creates local configuration files from examples when needed, creates a virtual environment, and installs dependencies.

### 2. Configure the YouTube API key

Open the generated `.env` file and add:

```env
YOUTUBE_API_KEY=your_youtube_api_key
```

Never commit `.env` or expose real credentials in screenshots, logs, examples, or public repositories.

### 3. Add search keywords

Edit `keyword.txt` and place one keyword on each line:

```text
baby monitor
baby car monitor
video baby monitor
```

### 4. Run creator discovery

```bash
cd /path/to/yt-kol-workflow
source .venv/bin/activate
python main.py batch \
  --keywords-file keyword.txt \
  --sort-order relevance \
  --yes \
  --no-feishu
```

## Expected Outputs

A batch run creates timestamped files such as:

```text
output/<timestamp>_batch/search_tasks_all.xlsx
output/<timestamp>_batch/search_videos_all.xlsx
output/<timestamp>_batch/influencers_all.xlsx
output/<timestamp>_batch/influencer_videos_all.xlsx
```

These files represent four core business tables:

1. Search tasks
2. Video data
3. Creator details
4. Creator videos

## Merge Batch Results

Merge a completed batch into one standardized workbook:

```bash
python main.py merge-output \
  output/<timestamp>_batch \
  --output output/summary_<timestamp>/kol_summary_tables.xlsx
```

## Sync to Feishu / Lark Bitable

Set up or reuse a Feishu Base:

```bash
python main.py feishu-setup
```

Then sync the merged workbook:

```bash
python main.py sync-workbook \
  --workbook output/summary_<timestamp>/kol_summary_tables.xlsx \
  --cleanup-empty-rows
```

The setup process creates or reuses four tables:

- 搜索任务表
- 视频数据表
- 网红详情表
- 网红视频表

## Feishu Authorization

If Feishu synchronization reports missing permissions, re-authorize with the required scopes:

```bash
lark-cli --profile kol-workflow auth login \
  --scope 'bitable:app:readonly bitable:app base:record:retrieve'
```

Then rerun the sync command.

## Local Files That Must Not Be Committed

Keep the following files and directories out of Git:

```text
.env
keyword.txt
brand_exclusions.json
output/
.venv/
*.xlsx
__pycache__/
*.pyc
```

Recommended `.gitignore`:

```gitignore
.env
.venv/
venv/
output/
keyword.txt
brand_exclusions.json
*.xlsx
__pycache__/
*.py[cod]
.DS_Store
```

## GitHub Safety Check

Before pushing the repository, run:

```bash
rg -n 'AI[z]a|YOUTUBE_API_KEY=AI[z]a|FEISHU_APP_SECRET=.{8,}|FEISHU_APP_TOKEN=.{8,}|old-upstream-owner' .
find . -name '.env' \
  -o -name '*.xlsx' \
  -o -path '*/output/*' \
  -o -path '*/.venv/*' \
  -o -path '*/.git/*'
```

Only placeholder credentials in example files are acceptable.

## Common Issues

### Missing YouTube API key

Add `YOUTUBE_API_KEY` to `.env`.

### Hidden `.env` file on macOS

In Finder, press:

```text
Command + Shift + .
```

### Feishu CLI installation fails

Run:

```bash
npx --yes @larksuite/cli@latest install
```

### Feishu tables are incomplete

If the first setup was interrupted, run again:

```bash
python main.py feishu-setup
```

## Documentation

- Skill instructions: `SKILL.md`
- Operating guide: `references/workflow-operations.md`
- Bundled workflow: `assets/yt-kol-workflow`

## Use Cases

This workflow is suitable for:

- YouTube creator discovery
- KOL and influencer prospecting
- Product-keyword creator research
- Channel qualification and filtering
- Creator lead list building
- Influencer outreach preparation
- Feishu-based creator pipeline management

## License

See `LICENSE` for license terms.
