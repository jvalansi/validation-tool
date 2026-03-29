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
    <iframe src="{form_url}" width="100%" frameborder="0" marginheight="0" marginwidth="0"
            style="border-radius:8px;min-height:300px;" onload="window.parent.scrollTo(0,0)">
    </iframe>
    <script src="https://tally.so/widgets/embed.js" async></script>"""
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

    # Inline SVG icons keyed by name — safe cross-platform alternative to emoji
    svg_icons = {
        "chart": '<svg viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
        "zap":   '<svg viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
        "shield":'<svg viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
        "cpu":   '<svg viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></svg>',
        "eye":   '<svg viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>',
        "layers":'<svg viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>',
        "dollar":'<svg viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>',
        "code":  '<svg viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>',
        "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>',
    }
    default_icon_keys = ["zap", "layers", "chart"]

    features = features or []
    feature_cards = ""
    if features:
        cards = []
        for i, f in enumerate(features):
            key = f.get("icon_key") or default_icon_keys[i % len(default_icon_keys)]
            svg = svg_icons.get(key, svg_icons["zap"])
            cards.append(
                f'    <div class="card"><span class="icon">{svg}</span>'
                f'<strong>{f["title"]}</strong><p>{f["body"]}</p></div>'
            )
        cards_html = "\n".join(cards)
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
      background: linear-gradient(135deg, #ffffff 30%, #38bdf8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      color: #ffffff;
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
    .card .icon {{ display: block; margin-bottom: 0.75rem; width: 28px; height: 28px; }}
    .card .icon svg {{ width: 28px; height: 28px; }}
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
