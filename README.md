# Medium Auto Publish

Zero-cost automation pipeline that generates a technical blog post using AI, hosts it on GitHub Pages, and publishes it via Medium's native Import Story tool.

## Setup

1. **Install requirements:**
   ```
   pip install -r requirements.txt
   playwright install --with-deps chromium
   ```

2. **Set environment variables:**
   - `GROQ_API_KEY`: Your Groq API key for LLM generation.

3. **Get Medium Session:**
   Run `python scripts/get_medium_session.py` to log in to Medium and save your session locally to `auth/medium_state.json`.

## GitHub Actions Deploy

To run this pipeline daily via GitHub Actions:
1. Push to GitHub.
2. Go to Settings -> Pages, enable it from the `main` branch, `/docs` folder.
3. Set GitHub Secrets:
   ```bash
   gh secret set GROQ_API_KEY -b"your_key"
   gh secret set MEDIUM_STATE < auth/medium_state.json
   ```

## Pages URL
The Pages URL used to import the story is constructed as: `https://<username>.github.io/<repo>/`

## Daily workflow
1. Daily cron triggers Action
2. Groq generates post content (JSON)
3. Pollinations generates images (hero and mid)
4. HTML is rendered and pushed to `docs/`
5. GitHub Pages deploys the updated HTML
6. Playwright triggers Medium's "Import a story" with the Pages URL and publishes the post.
