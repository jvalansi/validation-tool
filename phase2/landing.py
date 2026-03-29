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


def build_html(project_name, description, pain_desire, price_per_year, form_url, features=None):
    def _saas_price(annual):
        raw = annual / 12
        anchors = [9, 19, 29, 49, 79, 99, 149, 199, 299, 499, 799, 999]
        return min(anchors, key=lambda x: abs(x - raw))

    price_per_mo = _saas_price(price_per_year) if price_per_year else None

    if form_url:
        cta_block = f"""
    <form class="signup-form" action="{form_url}" method="POST" target="_blank">
      <input type="email" name="email" placeholder="your@email.com" required />
      <button type="submit">Join the waitlist &rarr;</button>
    </form>"""
    else:
        cta_block = """
    <form class="signup-form" onsubmit="handleSubmit(event)">
      <input type="email" name="email" placeholder="your@email.com" required />
      <button type="submit">Join the waitlist &rarr;</button>
    </form>
    <p id="submitted" style="display:none;color:#4ade80;margin-top:1rem;text-align:center;">
      &#10003; You're on the list — we'll be in touch!
    </p>
    <script>
      function handleSubmit(e) {{
        e.preventDefault();
        document.querySelector('.signup-form').style.display = 'none';
        document.getElementById('submitted').style.display = 'block';
      }}
    </script>"""

    features = features or []
    feature_cards = ""
    if features:
        cards_html = "\n".join(
            f'    <div class="card"><span class="icon">{f["icon"]}</span><strong>{f["title"]}</strong><p>{f["body"]}</p></div>'
            for f in features
        )
        feature_cards = f"""
  <section class="features">
{cards_html}
  </section>"""

    price_note = ""
    if price_per_mo:
        price_note = f'<p class="price-note">Early access from <strong>${price_per_mo}/mo</strong> &mdash; lock in founder pricing</p>'

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
      padding: 2rem 1rem 4rem;
    }}
    .container {{ max-width: 640px; width: 100%; margin: 0 auto; }}

    /* Hero */
    .hero {{ text-align: center; padding: 5rem 0 2.5rem; }}
    .badge {{
      display: inline-block;
      background: #1e3a5f;
      color: #7dd3fc;
      font-size: 0.78rem;
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      padding: 0.3rem 0.9rem;
      border-radius: 9999px;
      margin-bottom: 1.5rem;
    }}
    .hero h1 {{
      font-size: clamp(2rem, 5vw, 3.2rem);
      font-weight: 800;
      line-height: 1.15;
      margin-bottom: 1.25rem;
      background: linear-gradient(135deg, #f8fafc 0%, #7dd3fc 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }}
    .hero .subtitle {{
      font-size: 1.15rem;
      color: #94a3b8;
      line-height: 1.65;
      max-width: 520px;
      margin: 0 auto 2.5rem;
    }}

    /* Signup form */
    .signup-form {{
      display: flex;
      gap: 0.5rem;
      max-width: 480px;
      margin: 0 auto 1rem;
    }}
    .signup-form input {{
      flex: 1;
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 0.75rem 1rem;
      color: #f1f5f9;
      font-size: 1rem;
      outline: none;
    }}
    .signup-form input:focus {{ border-color: #38bdf8; }}
    .signup-form button {{
      background: #0ea5e9;
      color: #fff;
      border: none;
      border-radius: 8px;
      padding: 0.75rem 1.25rem;
      font-size: 0.95rem;
      font-weight: 600;
      cursor: pointer;
      white-space: nowrap;
      transition: background 0.15s;
    }}
    .signup-form button:hover {{ background: #38bdf8; }}
    .signup-hint {{
      text-align: center;
      font-size: 0.82rem;
      color: #475569;
      margin-bottom: 2.5rem;
    }}

    /* Price note */
    .price-note {{
      text-align: center;
      font-size: 0.9rem;
      color: #64748b;
      margin-bottom: 3rem;
    }}
    .price-note strong {{ color: #7dd3fc; }}

    /* Feature cards */
    .features {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
      gap: 1rem;
      margin-bottom: 3rem;
    }}
    .card {{
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 12px;
      padding: 1.25rem;
    }}
    .card .icon {{ font-size: 1.6rem; display: block; margin-bottom: 0.6rem; }}
    .card strong {{ display: block; font-size: 0.95rem; margin-bottom: 0.35rem; color: #f1f5f9; }}
    .card p {{ font-size: 0.85rem; color: #94a3b8; line-height: 1.5; }}

    /* Footer */
    footer {{ text-align: center; color: #334155; font-size: 0.8rem; padding-top: 1rem; }}

    @media (max-width: 480px) {{
      .signup-form {{ flex-direction: column; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <section class="hero">
      <span class="badge">Early access</span>
      <h1>{pain_desire}</h1>
      <p class="subtitle">{description}</p>
      {cta_block}
      <p class="signup-hint">No spam &middot; Unsubscribe anytime</p>
      {price_note}
    </section>
    {feature_cards}
  </div>
  <footer>Built by independent makers</footer>
</body>
</html>
"""


def deploy_landing_page(project_name, description, pain_desire, price_per_year, form_url=None, features=None, dry_run=False):
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
    html_content = build_html(project_name, description, pain_desire, price_per_year, form_url, features)

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
    elif pages_status in (409, 422):
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
