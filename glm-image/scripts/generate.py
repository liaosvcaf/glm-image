#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GLM-Image generation script for Claude Code skill.
Generates an image from a text prompt and outputs markdown-formatted result.
"""

import os
import sys
import json
import datetime
import re
import argparse
import requests


def load_api_key() -> str:
    """Load API key from environment or config file."""
    api_key = os.environ.get("GLM_API_KEY")
    if api_key:
        return api_key

    # Try config.json in current directory
    config_paths = ["config.json", os.path.expanduser("~/.openclaw/config.json"), os.path.expanduser("~/.claude/config.json")]
    for path in config_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    config = json.load(f)
                    if "api_key" in config:
                        return config["api_key"]
            except:
                pass

    # Try .env file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)
    env_paths = [
        os.path.join(skill_dir, ".env"),  # skill 目录下的 .env
        ".env",                            # 当前工作目录
        os.path.expanduser("~/.env")       # 用户主目录
    ]
    for path in env_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("GLM_API_KEY="):
                            value = line.split("=", 1)[1].strip()
                            if value.startswith('"') and value.endswith('"'):
                                value = value[1:-1]
                            return value
            except:
                pass

    raise ValueError("API key not found. Set GLM_API_KEY environment variable or add to config.json")


def generate_image(
    prompt: str,
    size: str = "1088x1920",
    quality: str = "hd",
    watermark: bool = False,
    output_dir: str = "output"
) -> dict:
    """Generate an image using GLM-Image API."""
    api_key = load_api_key()

    # API endpoint
    url = "https://open.bigmodel.cn/api/paas/v4/images/generations"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    body = {
        "model": "glm-image",
        "prompt": prompt,
        "size": size,
        "quality": quality,
        "watermark_enabled": str(watermark).lower()
    }

    response = requests.post(url, headers=headers, json=body, timeout=120)
    response.raise_for_status()

    data = response.json()

    if "data" not in data or not data["data"]:
        raise RuntimeError("No image returned from API")

    image_url = data["data"][0]["url"]

    # Download and save image
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_prompt = re.sub(r'[\\/:*?"<>|]', '', prompt).replace(' ', '_')[:30]
    filename = f"{timestamp}_{safe_prompt}.png"
    filepath = os.path.join(output_dir, filename)

    img_response = requests.get(image_url, timeout=60)
    img_response.raise_for_status()

    with open(filepath, "wb") as f:
        f.write(img_response.content)

    return {
        "url": image_url,
        "local_path": filepath,
        "prompt": prompt
    }


def main():
    parser = argparse.ArgumentParser(description="Generate image from prompt")
    parser.add_argument("prompt", help="Image description")
    parser.add_argument("--size", default="1088x1920", help="Image size (default: 1088x1920)")
    parser.add_argument("--quality", default="hd", help="Image quality (default: hd)")
    parser.add_argument("--output", default="output", help="Output directory (default: output)")
    parser.add_argument("--watermark", action="store_true", help="Enable watermark (disabled by default)")

    args = parser.parse_args()

    try:
        result = generate_image(
            prompt=args.prompt,
            size=args.size,
            quality=args.quality,
            watermark=args.watermark,
            output_dir=args.output
        )

        print(f"Image saved: {result['local_path']}")
        print(f"\nMarkdown URL:\n![{result['prompt']}]({result['url']})")
        print(f"\nLocal path: {result['local_path']}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
