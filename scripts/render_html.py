import json
import os
import re
import html


def main():
    if not os.path.exists("post.json"):
        print("post.json not found.")
        return

    with open("post.json", "r", encoding="utf-8") as f:
        post_data = json.load(f)

    title = post_data.get("title", "Untitled")
    subtitle = post_data.get("subtitle", "")
    body_html = post_data.get("body_html", "")
    
    seo = post_data.get("seo", {})
    meta_title = seo.get("meta_title") or title
    meta_desc = seo.get("meta_description") or subtitle
    focus_keyword = seo.get("focus_keyword", "")
    
    # Sanitize LLM HTML: remove empty pre/code blocks and excess spacing
    body_html = re.sub(r'<pre><code>\s*</code></pre>', '', body_html)
    body_html = re.sub(r'<p>\s*</p>', '', body_html)
    body_html = re.sub(r'\n{3,}', '\n\n', body_html)
    
    images = post_data.get("images", [])
    tags = post_data.get("tags", [])
    read_minutes = post_data.get("estimated_read_minutes")
    slug = post_data.get("canonical_slug", "")

    # Insert mid-article images after their target headings
    for idx, img_data in enumerate(images):
        heading = img_data.get("insert_after_heading", "")
        caption = img_data.get("caption", "")
        caption_html = f"<figcaption>{html.escape(caption)}</figcaption>" if caption else ""
        img_html = (
            f'<figure class="mid-figure">'
            f'<img src="images/mid_{idx}.png" alt="{html.escape(heading or f"Illustration {idx+1}")}" loading="lazy" />'
            f'{caption_html}'
            f'</figure>'
        )

        inserted = False
        if heading:
            heading_pattern = re.compile(rf"(<h2>\s*{re.escape(heading)}\s*</h2>)", re.IGNORECASE)
            if heading_pattern.search(body_html):
                body_html = heading_pattern.sub(r"\1\n" + img_html, body_html, count=1)
                inserted = True

        if not inserted:
            body_html += "\n" + img_html

    tags_html = "".join(f'<span class="tag">#{html.escape(tag)}</span>' for tag in tags)
    meta_bits = []
    if read_minutes:
        meta_bits.append(f"{read_minutes} min read")
    meta_line = " · ".join(meta_bits)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(meta_title)}</title>
<meta name="description" content="{html.escape(meta_desc)}">
<meta name="keywords" content="{html.escape(focus_keyword)}">
<style>
  :root {{
    --text: #1a1a1a;
    --muted: #6b6b6b;
    --accent: #0d6efd;
    --border: #ececec;
    --code-bg: #0d1117;
    --code-text: #e6edf3;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    font-family: "Georgia", "Iowan Old Style", serif;
    line-height: 1.75;
    max-width: 720px;
    margin: 0 auto;
    padding: 48px 24px 96px;
    color: var(--text);
    background: #fff;
  }}
  h1 {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    line-height: 1.2;
    margin: 0 0 12px;
    letter-spacing: -0.02em;
  }}
  .meta {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    color: var(--muted);
    font-size: 1.05rem;
    margin-bottom: 8px;
  }}
  .read-time {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    color: var(--muted);
    font-size: 0.9rem;
    margin-bottom: 32px;
    padding-bottom: 24px;
    border-bottom: 1px solid var(--border);
  }}
  figure {{ margin: 32px 0; }}
  img {{
    max-width: 100%;
    height: auto;
    display: block;
    border-radius: 10px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  }}
  figcaption {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 0.85rem;
    color: var(--muted);
    text-align: center;
    margin-top: 10px;
  }}
  article h2 {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 1.55rem;
    font-weight: 700;
    margin: 44px 0 18px;
    letter-spacing: -0.01em;
  }}
  article p {{ font-size: 1.15rem; margin: 0 0 20px; }}
  article ul, article ol {{ font-size: 1.1rem; margin: 0 0 20px; padding-left: 28px; }}
  article li {{ margin-bottom: 8px; }}
  article strong {{ font-weight: 700; }}
  pre {{
    background: var(--code-bg);
    color: var(--code-text);
    padding: 20px;
    border-radius: 10px;
    overflow-x: auto;
    font-size: 0.9rem;
    margin: 0 0 24px;
  }}
  code {{
    font-family: "SF Mono", Menlo, Consolas, monospace;
  }}
  :not(pre) > code {{
    background: #f1f1f1;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.9em;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 0 0 28px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 0.95rem;
  }}
  th, td {{
    border: 1px solid var(--border);
    padding: 10px 12px;
    text-align: left;
  }}
  th {{ background: #fafafa; font-weight: 700; }}
  .tags {{
    margin-top: 48px;
    padding-top: 24px;
    border-top: 1px solid var(--border);
  }}
  .tag {{
    display: inline-block;
    background: #eef4ff;
    color: var(--accent);
    padding: 6px 14px;
    border-radius: 20px;
    margin: 0 8px 8px 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
  }}
  @media (max-width: 600px) {{
    body {{ padding: 32px 18px 72px; }}
    h1 {{ font-size: 1.9rem; }}
    article p, article ul, article ol {{ font-size: 1.05rem; }}
  }}
</style>
</head>
<body>
<h1>{html.escape(title)}</h1>
<div class="meta">{html.escape(subtitle)}</div>
<div class="read-time">{meta_line}</div>
<figure>
  <img src="images/hero.png" alt="{html.escape(title)}" />
</figure>
<article>
{body_html}
</article>
<div class="tags">
{tags_html}
</div>
</body>
</html>"""

    os.makedirs("docs", exist_ok=True)
    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Rendered docs/index.html ({slug or 'no-slug'})")


if __name__ == "__main__":
    main()
