"""
Generate and deploy a GitHub Pages landing page for a validation campaign.
"""

import base64
import json
import os
import re
import time
import urllib.request
import urllib.error


GH_TOKEN = os.environ.get("GH_TOKEN")
GH_API = "https://api.github.com"


def slugify(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = text.strip("-")
    return text


def gh_request(method, path, data=None):
    url = f"{GH_API}{path}"
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {GH_TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read()), resp.status
    except urllib.error.HTTPError as e:
        body = e.read()
        try:
            payload = json.loads(body)
        except Exception:
            payload = {"message": body.decode(errors="replace")}
        return payload, e.code


def build_html(project_name, description, pain_desire, price_per_year, form_url):
    price_line = ""
    if price_per_year is not None:
        price_per_mo = round(price_per_year / 12)
        price_line = f'<p class="price">Coming soon &mdash; early access from ${price_per_mo}/mo</p>'

    if form_url:
        cta_section = f'<iframe src="{form_url}" width="100%" height="500" frameborder="0" marginheight="0" marginwidth="0">Loading form...</iframe>'
    else:
        cta_section = '<p class="placeholder">Signup form coming soon</p>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{project_name}</title>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: #0f172a;
      color: #f1f5f9;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 2rem 1rem;
    }}
    .container {{
      max-width: 640px;
      width: 100%;
      margin: 0 auto;
    }}
    .hero {{
      text-align: center;
      padding: 4rem 0 2rem;
    }}
    .hero h1 {{
      font-size: clamp(1.8rem, 5vw, 3rem);
      font-weight: 800;
      line-height: 1.2;
      margin-bottom: 1rem;
      color: #f8fafc;
    }}
    .hero .subtitle {{
      font-size: 1.1rem;
      color: #94a3b8;
      line-height: 1.6;
      margin-bottom: 1.5rem;
    }}
    .price {{
      display: inline-block;
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 9999px;
      padding: 0.4rem 1.2rem;
      font-size: 0.95rem;
      color: #7dd3fc;
      margin-bottom: 2.5rem;
    }}
    .cta {{
      margin: 2rem 0;
    }}
    .placeholder {{
      text-align: center;
      color: #64748b;
      font-style: italic;
      padding: 3rem 0;
      border: 1px dashed #334155;
      border-radius: 8px;
    }}
    footer {{
      margin-top: auto;
      padding-top: 3rem;
      text-align: center;
      color: #475569;
      font-size: 0.85rem;
    }}
    iframe {{
      border-radius: 8px;
      display: block;
    }}
  </style>
</head>
<body>
  <div class="container">
    <section class="hero">
      <h1>{pain_desire}</h1>
      <p class="subtitle">{description}</p>
      {price_line}
    </section>
    <div class="cta">
      {cta_section}
    </div>
  </div>
  <footer>Powered by independent makers</footer>
</body>
</html>
"""


def deploy_landing_page(project_name, description, pain_desire, price_per_year, form_url=None, dry_run=False):
    """
    Deploy a landing page to GitHub Pages.

    Args:
        project_name: str — e.g. "AutoDraft"
        description: str — one-line description of the product
        pain_desire: str — the pain point or desire this solves (used as hero headline)
        price_per_year: float or None — price in USD/year
        form_url: str or None — Google Form URL to embed (placeholder shown if None)
        dry_run: bool — if True, print HTML without deploying

    Returns:
        dict with keys: repo_name, repo_url, pages_url, status
    """
    html_content = build_html(project_name, description, pain_desire, price_per_year, form_url)

    if dry_run:
        print(html_content)
        return {"status": "dry_run", "html": html_content}

    if not GH_TOKEN:
        raise RuntimeError("GH_TOKEN environment variable is not set")

    repo_name = f"validate-{slugify(project_name)}"

    # Get authenticated user
    user_data, status = gh_request("GET", "/user")
    if status != 200:
        raise RuntimeError(f"Failed to get GitHub user: {user_data}")
    owner = user_data["login"]

    # Check if repo exists
    repo_data, status = gh_request("GET", f"/repos/{owner}/{repo_name}")
    if status == 404:
        # Create repo
        create_data = {
            "name": repo_name,
            "auto_init": False,
            "private": False,
            "description": f"Validation landing page for {project_name}",
        }
        repo_data, status = gh_request("POST", "/user/repos", create_data)
        if status not in (200, 201):
            raise RuntimeError(f"Failed to create repo: {repo_data}")
        print(f"Created repo: {repo_name}")

        # Wait for repo to be available
        for _ in range(15):
            time.sleep(1)
            check, check_status = gh_request("GET", f"/repos/{owner}/{repo_name}")
            if check_status == 200:
                break
        else:
            raise RuntimeError("Repo not available after 15s")
    elif status != 200:
        raise RuntimeError(f"Error checking repo: {repo_data}")
    else:
        print(f"Repo already exists: {repo_name}")

    # Push index.html
    encoded_content = base64.b64encode(html_content.encode()).decode()
    file_path = f"/repos/{owner}/{repo_name}/contents/index.html"

    # Check if file exists (to get sha for update)
    existing_file, existing_status = gh_request("GET", file_path)
    put_data = {
        "message": "Add landing page",
        "content": encoded_content,
        "branch": "main",
    }
    if existing_status == 200 and "sha" in existing_file:
        put_data["sha"] = existing_file["sha"]

    file_result, file_status = gh_request("PUT", file_path, put_data)
    if file_status not in (200, 201):
        raise RuntimeError(f"Failed to push index.html: {file_result}")
    print("Pushed index.html")

    # Enable GitHub Pages
    pages_data, pages_status = gh_request(
        "POST",
        f"/repos/{owner}/{repo_name}/pages",
        {"source": {"branch": "main", "path": "/"}},
    )
    if pages_status in (200, 201):
        pages_url = pages_data.get("html_url", f"https://{owner}.github.io/{repo_name}")
        print(f"Enabled GitHub Pages: {pages_url}")
    elif pages_status == 422:
        # Already enabled — fetch existing URL
        existing_pages, ep_status = gh_request("GET", f"/repos/{owner}/{repo_name}/pages")
        if ep_status == 200:
            pages_url = existing_pages.get("html_url", f"https://{owner}.github.io/{repo_name}")
        else:
            pages_url = f"https://{owner}.github.io/{repo_name}"
        print(f"GitHub Pages already enabled: {pages_url}")
    else:
        pages_url = f"https://{owner}.github.io/{repo_name}"
        print(f"Warning: unexpected pages status {pages_status}: {pages_data}")

    return {
        "repo_name": repo_name,
        "repo_url": f"https://github.com/{owner}/{repo_name}",
        "pages_url": pages_url,
        "status": "deployed",
    }
