---
name: glm-image
description: Generate images using GLM-Image API. Use when the user wants to generate, create, or draw an image from a text prompt. Triggers on requests like "generate an image of...", "create a picture of...", "draw...", or any image generation request.
---

# GLM-Image Generator

Generate images from text prompts using the GLM-Image API.

> **Attribution:** Based on [glm-image](https://github.com/ViffyGwaanl/glm-image) by ViffyGwaanl (MIT License).

## Setup

This skill requires a GLM API key from [BigModel / Zhipu AI](https://open.bigmodel.cn).

The script looks for the key in this order:

1. `GLM_API_KEY` environment variable
2. `~/.openclaw/config.json` → `"api_key"` field
3. `~/.claude/config.json` → `"api_key"` field
4. `.env` file in the skill directory or working directory → `GLM_API_KEY=<value>`

**Recommended:** set it as an environment variable or add to `~/.openclaw/config.json`:

```json
{
  "api_key": "your-glm-api-key-here"
}
```

Get your key at: https://open.bigmodel.cn → Console → API Keys

## Usage

When a user requests image generation:

**Step 0 — Verify API key is configured**

Run a quick check to confirm the key is present before doing anything else:

```bash
python3 -c "
import os, json
found = bool(os.environ.get('GLM_API_KEY'))
if not found:
    import pathlib
    for p in ['~/.openclaw/config.json', '~/.claude/config.json']:
        try:
            d = json.loads(pathlib.Path(p).expanduser().read_text())
            if d.get('api_key'):
                found = True; break
        except: pass
print('KEY_FOUND' if found else 'KEY_MISSING')
"
```

If output is `KEY_MISSING`, tell the user:

> "GLM_API_KEY is not configured. To use this skill, get your API key from https://open.bigmodel.cn (Console → API Keys), then set it one of these ways:
>
> **Option A — environment variable (recommended):**
> ```
> export GLM_API_KEY=your-key-here
> ```
>
> **Option B — config file:**
> Create or edit `~/.openclaw/config.json` and add:
> ```json
> { "api_key": "your-key-here" }
> ```
>
> **Option C — .env file:**
> Create a `.env` file in the skill directory with:
> ```
> GLM_API_KEY=your-key-here
> ```"

Do not proceed until the user confirms the key is set.

**Step 1 — Ask for language (MANDATORY, no exceptions)**

Before running anything, ask:

> "What language is your prompt in? Please choose: zh (Chinese), en (English), ja (Japanese), ko (Korean), fr (French), de (German), es (Spanish)."

Do NOT infer language from the user's message language or any other signal. Do NOT default to any language. Do NOT proceed until the user explicitly states a language code.

**Step 2 — Run the generation script**

```bash
python3 scripts/generate.py "<prompt>" --language <code>
```

`--language` is required. The script will error if omitted.

Other defaults:

- Size: 1088x1920 (portrait HD)
- Output: `output/` folder
- No watermark

**Step 3 — Return the result**

Display the markdown image link and local file path.

## Generate Image

```bash
python3 scripts/generate.py "<prompt>" --language <zh|en|ja|ko|fr|de|es>
```

### Options

- `--language`: **(Required)** Prompt language. Must be explicitly provided by the user. Supported: `zh` (Chinese), `en` (English), `ja` (Japanese), `ko` (Korean), `fr` (French), `de` (German), `es` (Spanish)
- `--size`: Image dimensions (default: 1088x1920). Valid range: 512-2048px, must be multiples of 32
- `--output`: Custom output path (default: output/)
- `--quality`: Image quality, "hd" or "standard" (default: hd)
- `--watermark`: Enable watermark (disabled by default)

### Language Selection Rules

- **Always ask explicitly.** Never guess from the user's message language.
- **Never default.** If the user does not specify, ask again.
- **Record as-typed.** Pass exactly what the user said (e.g., `zh`, `en`) — do not normalize.
- Reason: GLM is a Chinese-native model; prompt language significantly affects output quality and style.

### Available Sizes

- 1088x1920 (default, portrait HD)
- 1920x1088 (landscape HD)
- 1280x1280 (square)
- 1568x1056, 1056x1568
- 1472x1088, 1088x1472
- 1728x960, 960x1728

## Output Format

After successful generation, display:

1. Local file path: `output/<timestamp>_<prompt>.png`
2. Markdown image link: `![<prompt>](<url>)`

## Agent Owner

This skill is executed by the main OpenClaw agent session. The `generate.py` script
runs as a shell command via the exec tool. No sub-agents are spawned.

## Success Criteria

Image generation succeeds when:
1. Script exits with code 0
2. Image file saved to output/ directory
3. Markdown image link displayed to user

Failure conditions: invalid API key, unsupported size, network timeout (120s), API quota exceeded.

## Edge Cases

- Invalid size: must be 512-2048px in multiples of 32 — script will fail with API error
- Long prompts: prompt truncated to 30 chars in filename (full prompt used for generation)
- Network timeout: 120s API timeout, 60s download timeout — retry once if timeout
- Missing API key: script exits with clear error message listing search locations
- Chinese characters in prompt: supported, filename sanitized automatically

## Requirements

- GLM API key configured (see Setup section above)
- Python 3 with `requests` package (`pip install requests`)
