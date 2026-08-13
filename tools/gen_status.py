#!/usr/bin/env python3
"""Regenerate assets/status.svg from the live GitHub API.

Deliberately not a follower or star counter. Those read as vanity metrics and
say nothing at this size. This shows whether the work is actually maintained:
current release, whether the suite is green, how many commits exist and when
it was last touched.

Runs from .github/workflows/status.yml with the default GITHUB_TOKEN, which can
read public repository data without any secret being configured.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

REPO = os.environ.get("STATUS_REPO", "hamim-liberate-labs/standup-sync")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
API = "https://api.github.com"

BG0, BG1 = "#070B16", "#161E3A"
CYAN, VIOLET, EMERALD, AMBER, RED = "#22D3EE", "#A78BFA", "#34D399", "#FBBF24", "#F87171"
TEXT, MUTED = "#E8EEF7", "#94A3B8"
SANS = "'Segoe UI',Ubuntu,'Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,'SF Mono','Cascadia Code','Fira Code',Menlo,Consolas,monospace"


def get(path, raw=False):
    req = urllib.request.Request(f"{API}{path}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "profile-status-generator")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r if raw else json.load(r)
    except urllib.error.HTTPError as e:
        print(f"warn: {path} -> HTTP {e.code}", file=sys.stderr)
        return None
    except Exception as e:  # network flake should not fail the workflow
        print(f"warn: {path} -> {e}", file=sys.stderr)
        return None


def commit_count():
    """Total commits on the default branch, read from the Link header."""
    req = urllib.request.Request(f"{API}/repos/{REPO}/commits?per_page=1")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "profile-status-generator")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            link = r.headers.get("Link", "")
    except Exception as e:
        print(f"warn: commit count -> {e}", file=sys.stderr)
        return None
    m = re.search(r'[?&]page=(\d+)>; rel="last"', link)
    return int(m.group(1)) if m else None


def humanise(iso):
    if not iso:
        return None
    d = datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    days = (datetime.now(timezone.utc) - d).days
    if days <= 0:
        return "today"
    if days == 1:
        return "yesterday"
    if days < 30:
        return f"{days} days ago"
    if days < 365:
        return f"{days // 30} months ago"
    return f"{days // 365} years ago"


def collect():
    repo = get(f"/repos/{REPO}") or {}
    rel = get(f"/repos/{REPO}/releases/latest") or {}
    runs = get(f"/repos/{REPO}/actions/workflows/tests.yml/runs?branch=main&per_page=1") or {}
    run = (runs.get("workflow_runs") or [{}])[0]

    conclusion = run.get("conclusion")
    if conclusion == "success":
        ci_label, ci_col = "suite green", EMERALD
    elif conclusion in (None, ""):
        ci_label, ci_col = "suite unknown", MUTED
    else:
        ci_label, ci_col = f"suite {conclusion}", RED

    n = commit_count()
    return [
        (repo.get("name") or REPO.split("/")[-1], CYAN, True),
        (rel.get("tag_name") or "unreleased", VIOLET, False),
        (ci_label, ci_col, False),
        (f"{n} commits" if n else "", AMBER, False),
        (f"updated {humanise(repo.get('pushed_at'))}" if repo.get("pushed_at") else "", MUTED, False),
    ]


def render(items):
    items = [(t, c, b) for t, c, b in items if t]
    W, H = 900, 88
    CH, PAD, GAP = 7.4, 16, 10
    p = []
    a = p.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
      f'role="img" aria-label="Project status: {", ".join(t for t, _, _ in items)}">')
    a("<defs>")
    a(f'<linearGradient id="sb" x1="0" y1="0" x2="1" y2="1">'
      f'<stop offset="0%" stop-color="{BG0}"/><stop offset="100%" stop-color="{BG1}"/></linearGradient>')
    a(f'<clipPath id="sbc"><rect width="{W}" height="{H}" rx="16"/></clipPath>')
    a("</defs>")
    a("<style>")
    a(f".n{{font-family:{SANS};}} .m{{font-family:{MONO};}}")
    a("@keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}")
    a(".live{animation:pulse 2.4s ease-in-out infinite;}")
    a("</style>")
    a('<g clip-path="url(#sbc)">')
    a(f'<rect width="{W}" height="{H}" fill="url(#sb)"/>')
    for x in range(0, W, 30):
        a(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{CYAN}" stroke-opacity="0.04"/>')
    a(f'<text class="m" x="26" y="26" font-size="10" fill="{MUTED}" letter-spacing="2.4">'
      f'FEATURED PROJECT</text>')

    x, cy = 26, 58
    for label, col, bold in items:
        w = round(len(label) * CH + PAD * 2 + 14)
        a(f'<rect x="{x}" y="{cy-15}" width="{w}" height="30" rx="15" fill="{col}" '
          f'fill-opacity="0.10" stroke="{col}" stroke-opacity="0.42"/>')
        a(f'<circle class="live" cx="{x+PAD}" cy="{cy}" r="3.2" fill="{col}"/>')
        weight = ' font-weight="700"' if bold else ''
        a(f'<text class="m" x="{x+PAD+11}" y="{cy+4}" font-size="12" fill="{TEXT}"'
          f'{weight}>{label}</text>')
        x += w + GAP
    a("</g>")
    a(f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{CYAN}" '
      f'stroke-opacity="0.20"/>')
    a("</svg>")
    return "".join(p)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "assets", "status.svg")
    svg = render(collect())
    with open(out, "w") as f:
        f.write(svg)
    print(f"wrote {out} ({len(svg)} bytes)")
