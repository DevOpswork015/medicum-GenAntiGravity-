import json
import os
import re

def main():
    if not os.path.exists("post.json"):
        print("post.json not found.")
        return
        
    with open("post.json", "r", encoding="utf-8") as f:
        post_data = json.load(f)
        
    title = post_data.get("title", "Untitled")
    subtitle = post_data.get("subtitle", "")
    body_html = post_data.get("body_html", "")
    mid_heading = post_data.get("mid_image_insert_after_heading", "")
    tags = post_data.get("tags", [])
    
    mid_image_html = '<figure><img src="images/mid.png" alt="Mid Image" /></figure>'
    
    if mid_heading:
        # Regex to find the heading and insert after it
        heading_pattern = re.compile(rf"(<h2>\s*{re.escape(mid_heading)}\s*</h2>)", re.IGNORECASE)
        if heading_pattern.search(body_html):
            body_html = heading_pattern.sub(r"\1\n" + mid_image_html, body_html, count=1)
        else:
            body_html += "\n" + mid_image_html
    else:
        body_html += "\n" + mid_image_html
        
    tags_html = " ".join([f'<span class="tag">#{tag}</span>' for tag in tags])
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; color: #333; }}
        img {{ max-width: 100%; height: auto; border-radius: 8px; margin: 20px 0; }}
        pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        code {{ font-family: monospace; }}
        .tag {{ display: inline-block; background: #eee; padding: 5px 10px; border-radius: 15px; margin-right: 5px; font-size: 0.9em; }}
        .meta {{ color: #666; margin-bottom: 30px; font-style: italic; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="meta">{subtitle}</div>
    <figure>
        <img src="images/hero.png" alt="Hero Image" />
    </figure>
    <article>
        {body_html}
    </article>
    <div class="tags">
        {tags_html}
    </div>
</body>
</html>"""

    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print("Rendered docs/index.html")

if __name__ == "__main__":
    main()
