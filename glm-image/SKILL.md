---
name: glm-image
description: Generate images using GLM-Image API. Use when the user wants to generate, create, or draw an image from a text prompt. Triggers on requests like "generate an image of...", "create a picture of...", "draw...", or any image generation request.
---

# GLM-Image Generator

Generate images from text prompts using the GLM-Image API.

## Usage

When user provides an image generation prompt:

1. Run the generation script with the prompt
2. Default size: 1088x1920 (portrait HD)
3. Images save to `output/` folder automatically
4. No watermark by default
5. Return the image URL in markdown format

## Generate Image

```bash
python3 ~/.claude/skills/glm-image/scripts/generate.py "<prompt>"
```

### Options

- `--size`: Image dimensions (default: 1088x1920). Valid range: 512-2048px, must be multiples of 32
- `--output`: Custom output path (default: output/)
- `--quality`: Image quality, "hd" or "standard" (default: hd)
- `--watermark`: Enable watermark (disabled by default)

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

## Requirements

- GLM_API_KEY environment variable or config.json with api_key
