---
name: saraking-yt-kol-workflow
description: Run SARA/saraking's YouTube KOL discovery workflow for product keywords. Use when Codex needs to install or operate the bundled YouTube influencer search system, configure YouTube Data API credentials, update keyword files, run YouTube video/channel filtering, export Excel workbooks, merge output batches, or sync KOL data into Feishu/Lark Bitable documents.
---

# SARA YouTube KOL Workflow

## Overview

Use this skill to operate the bundled `yt-kol-workflow` project as a repeatable SARA/saraking workflow. It searches YouTube by product keywords, filters videos, identifies creator channels, exports Excel files, and optionally syncs the normalized tables into Feishu/Lark Bitable.

The bundled project lives in `assets/yt-kol-workflow`. Do not commit user secrets, generated outputs, virtual environments, or local keyword files.

## Quick Start

For a fresh install, run the bootstrap helper from the skill root:

```bash
python scripts/bootstrap_workflow.py --target /path/to/yt-kol-workflow --install-deps
```

The helper copies the bundled workflow, creates `.env`, `keyword.txt`, and `brand_exclusions.json` from examples when absent, creates `.venv`, and installs Python requirements when `--install-deps` is used.

If the project is already installed, work directly in that project directory:

```bash
cd /path/to/yt-kol-workflow
source .venv/bin/activate
python main.py --help
```

## Standard Workflow

1. Configure YouTube API credentials.
   - Edit `.env`.
   - Set only `YOUTUBE_API_KEY=<real key>`.
   - Never print or commit `.env`.
   - If a key appears in screenshots or logs, tell the user to rotate it in Google Cloud.

2. Update keywords.
   - For one keyword, replace `keyword.txt` with that keyword plus a trailing newline.
   - For multiple keywords, keep one keyword per line.

3. Run local discovery first.

```bash
python main.py batch --keywords-file keyword.txt --sort-order relevance --yes --no-feishu
```

4. Merge the output batch into the four canonical business tables.

```bash
python main.py merge-output output/<timestamp>_batch --output output/summary_<timestamp>/kol_summary_tables.xlsx
```

5. Sync to Feishu/Lark Bitable when requested.

```bash
python main.py feishu-setup
python main.py sync-workbook --workbook output/summary_<timestamp>/kol_summary_tables.xlsx --cleanup-empty-rows
```

Use `feishu-setup` once per local profile or when a Base target is missing. It uses `lark-cli`, browser OAuth, and creates/reuses a Base target.

## Feishu Auth Notes

If sync fails with missing scopes such as `bitable:app:readonly`, `bitable:app`, or `base:record:retrieve`, explicitly re-authorize:

```bash
lark-cli --profile kol-workflow auth login --scope 'bitable:app:readonly bitable:app base:record:retrieve'
```

Then rerun `sync-workbook`.

## GitHub Hygiene

Before preparing a GitHub upload, verify the package is clean:

```bash
rg -n 'AI[z]a|YOUTUBE_API_KEY=AI[z]a|FEISHU_APP_SECRET=.{8,}|FEISHU_APP_TOKEN=.{8,}|old-upstream-owner' .
find . -name '.env' -o -name '*.xlsx' -o -path '*/output/*' -o -path '*/.venv/*' -o -path '*/.git/*'
```

The SARA/saraking fork should use `saraking` wherever ownership is shown. Do not point examples or remotes at any old upstream owner.

## References

For command details, troubleshooting, and expected outputs, read `references/workflow-operations.md`.
