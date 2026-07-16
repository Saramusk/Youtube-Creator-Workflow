# Workflow Operations

## Files

- `.env`: local secrets and runtime config. Never commit.
- `keyword.txt`: one search keyword per line. Never commit generated/local keyword files.
- `brand_exclusions.json`: local brand/channel exclusions.
- `output/`: generated Excel, logs, state, and summary workbooks.

## Local Run

```bash
cd /path/to/yt-kol-workflow
source .venv/bin/activate
python main.py batch --keywords-file keyword.txt --sort-order relevance --yes --no-feishu
```

Expected outputs:

- `output/<timestamp>_batch/search_tasks_all.xlsx`
- `output/<timestamp>_batch/search_videos_all.xlsx`
- `output/<timestamp>_batch/influencers_all.xlsx`
- `output/<timestamp>_batch/influencer_videos_all.xlsx`

## Merge and Sync

```bash
python main.py merge-output output/<timestamp>_batch --output output/summary_<timestamp>/kol_summary_tables.xlsx
python main.py sync-workbook --workbook output/summary_<timestamp>/kol_summary_tables.xlsx --cleanup-empty-rows
```

If no Feishu target exists, run:

```bash
python main.py feishu-setup
```

This installs/uses `lark-cli`, opens browser authorization, creates or reuses a Base, and ensures four tables:

- `搜索任务表`
- `视频数据表`
- `网红详情表`
- `网红视频表`

## Common Issues

- Missing YouTube key: set `YOUTUBE_API_KEY` in `.env`.
- Hidden `.env` in Finder: press `Command + Shift + .`.
- Feishu CLI install fails silently: run `npx --yes @larksuite/cli@latest install` directly.
- Feishu missing scopes: run `lark-cli --profile kol-workflow auth login --scope 'bitable:app:readonly bitable:app base:record:retrieve'`.
- Interrupted first Feishu setup may create only some tables: rerun `python main.py feishu-setup` before syncing.

## GitHub Safety Check

Run from the skill root before upload:

```bash
rg -n 'AI[z]a|YOUTUBE_API_KEY=AI[z]a|FEISHU_APP_SECRET=.{8,}|FEISHU_APP_TOKEN=.{8,}|old-upstream-owner' .
find . -name '.env' -o -name '*.xlsx' -o -path '*/output/*' -o -path '*/.venv/*' -o -path '*/.git/*'
```

Only placeholder credentials in example files are acceptable.
