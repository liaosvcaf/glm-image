# GLM Image Generator

Generate images from text prompts using the [GLM-Image API](https://open.bigmodel.cn) by Zhipu AI (BigModel).

**Attribution:** Based on [glm-image](https://github.com/ViffyGwaanl/glm-image) by ViffyGwaanl (MIT License).

## Setup

1. Get your API key from https://open.bigmodel.cn
2. Set `GLM_API_KEY` in your environment or TOOLS.md

## Usage

Ask the agent to generate an image:
- "Generate an image of a sunset over mountains"
- "Create a picture of a robot playing chess"
- "Draw a futuristic city at night"

## Output

Images are saved to `output/` with a timestamped filename and displayed as markdown image links.

## Sizes

| Size | Orientation |
|------|------------|
| 1088x1920 | Portrait HD (default) |
| 1920x1088 | Landscape HD |
| 1280x1280 | Square |

## Requirements
- Python 3
- `requests` library: `pip install requests`
- `GLM_API_KEY` environment variable
