---
name: glm-image
description: Generate images using GLM-Image API. Use when the user wants to generate, create, or draw an image from a text prompt. Triggers on requests like "generate an image of...", "create a picture of...", "draw...", or any image generation request.
---

# GLM-Image Generator

Generate images from text prompts using the GLM-Image API.

> **Attribution:** Based on [glm-image](https://github.com/ViffyGwaanl/glm-image) by ViffyGwaanl (MIT License).

## Usage

When a user requests image generation:

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

## Configuration

Set GLM_API_KEY in TOOLS.md or as environment variable. Never hardcode in skill files.

Required entries in TOOLS.md:
- **GLM_API_KEY**: Your BigModel API key (https://open.bigmodel.cn)

The script also reads from `config.json` or `.env` file as fallback.

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

- GLM_API_KEY environment variable or config.json with api_key
