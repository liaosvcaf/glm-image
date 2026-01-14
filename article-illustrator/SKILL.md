---
name: article-illustrator
description: Generate illustrations for articles using scrapbook style. Use when the user wants to add images to an article, create illustrated content, or requests "illustrate this article", "add images to this article", "generate pictures for this post".
---

# Article Illustrator

Transform articles into illustrated markdown with hand-crafted scrapbook style images.

## Workflow

1. **Analyze article**: Read the article content and identify key sections
2. **Generate image prompts**: Use the scrapbook prompt template to create image descriptions in JSON format
3. **Generate images**: Call glm-image skill for each image
4. **Compose output**: Insert images at appropriate positions and output final markdown

## Step 1: Generate Image Prompts

Read the system prompt from [references/scrapbook-prompt.md](references/scrapbook-prompt.md).

Using that system prompt, analyze the article and generate a JSON output with image descriptions:

```json
{
  "project_title": "项目标题 - 手工剪贴簿风格系列图",
  "style": "实体手工剪贴簿（Physical Mixed-Media Scrapbook）",
  "total_images": 3,
  "images": [
    {
      "image_id": 1,
      "title": "图片标题",
      "description": "300-500字的连续画面描述...",
      "insert_after": "文章中应该插入此图的段落标识"
    }
  ]
}
```

## Step 2: Generate Images

For each image in the JSON, run:

```bash
python3 ~/.claude/skills/glm-image/scripts/generate.py "<description>"
```

Collect the generated image URLs and local paths.

## Step 3: Compose Final Markdown

Insert images into the article at appropriate positions using markdown format:

```markdown
![图片标题](image_url)
```

## Output Format

Return the complete markdown article with:
1. Original article text
2. Generated images inserted at logical break points
3. Image captions using the title from JSON

## Tips

- Generate 2-5 images depending on article length
- Insert images after major topic transitions
- Keep image descriptions faithful to the scrapbook style
- Use portrait orientation (1088x1920) for all images
