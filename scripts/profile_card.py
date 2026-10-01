import os, urllib.request, xml.etree.ElementTree as ET, html
from pathlib import Path
URL = "https://github-stats-extended.vercel.app/api?username=Xuzijun57&show_icons=false&hide_rank=true&hide_title=true&commits_year=2026&role=OWNER,ORGANIZATION_MEMBER,COLLABORATOR&show=contributions"
request = urllib.request.Request(URL, headers={"User-Agent": "Xuzijun57-profile-card"})
with urllib.request.urlopen(request, timeout=90) as response:
    root = ET.fromstring(response.read())
texts = ["".join(e.itertext()).strip() for e in root.iter() if e.tag.endswith("}text")]
def value(prefix):
    for i, text in enumerate(texts):
        if text.startswith(prefix) and i + 1 < len(texts):
            candidate = texts[i + 1]
            if candidate and candidate[0].isdigit():
                return candidate
    raise ValueError("Missing statistic " + prefix)
rows = [("Total Stars", value("Total Stars")), ("Total Commits", value("Total Commits")), ("Total PRs", value("Total PRs")), ("Total Issues", value("Total Issues")), ("Contributed to", value("Contributed to"))]
icons = [
'<path d="m12 2 3 6 7 1-5 5 1 7-6-3-6 3 1-7-5-5 7-1z"/>',
'<path d="M4 5v5h5M4 10a9 9 0 1 1-1 5M12 6v6l4 2"/>',
'<circle cx="6" cy="4" r="2"/><circle cx="6" cy="20" r="2"/><circle cx="18" cy="20" r="2"/><path d="M6 6v12M18 18V9a5 5 0 0 0-5-5h-1m3-3-3 3 3 3"/>',
'<circle cx="12" cy="12" r="10"/><path d="M12 6v7m0 4v1"/>',
'<path d="M3 3h18v15H3zM7 18v4m10-4v4M3 14h18"/>'
]
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="336" height="213" viewBox="0 0 336 213" role="img" aria-label="Public GitHub statistics"><rect width="336" height="213" fill="#20252c"/>']
for i, ((label, count), icon) in enumerate(zip(rows, icons)):
    y = 26 + 41 * i
    svg.append(f'<g transform="translate(24 {y-12})" fill="none" stroke="#539bf5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{icon}</g>')
    svg.append(f'<g fill="#adbac7" font-family="Georgia, Times New Roman, serif" font-size="24" font-weight="bold"><text x="61" y="{y+8}">{html.escape(label)}:</text><text x="264" y="{y+8}">{html.escape(count)}</text></g>')
svg.append("</svg>")
Path("profile").mkdir(exist_ok=True)
Path("profile/stats.svg").write_text("".join(svg), encoding="utf-8")
try:
    total = value("Total Contributions")
except ValueError:
    total = None
if total:
    readme = Path("README.md")
    text = readme.read_text(encoding="utf-8")
    import re
    text = re.sub(r"<!-- aggregate:start -->.*?<!-- aggregate:end -->", f"<!-- aggregate:start -->\nTotal Contributions across all years: **{total}**. Anonymous private activity is included when enabled in GitHub profile settings.\n<!-- aggregate:end -->", text, flags=re.S)
    readme.write_text(text, encoding="utf-8")
