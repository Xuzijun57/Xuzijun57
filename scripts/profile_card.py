import os, urllib.request, xml.etree.ElementTree as ET, html
from pathlib import Path
URL = "https://github-stats-extended.vercel.app/api?username=Xuzijun57&show_icons=false&hide_rank=true&hide_title=true&include_all_commits=true&role=OWNER,ORGANIZATION_MEMBER,COLLABORATOR&show=contributions"
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
rows = [("Total Stars", value("Total Stars")), ("Total Commits", value("Total Commits")), ("Total PRs", value("Total PRs")), ("Total Issues", value("Total Issues")), ("Contributed to", value("Contributed to")), ("Contributions", value("Total Contributions"))]
icons = [
'<path d="m12 2 3 6 7 1-5 5 1 7-6-3-6 3 1-7-5-5 7-1z"/>',
'<path d="M4 5v5h5M4 10a9 9 0 1 1-1 5M12 6v6l4 2"/>',
'<circle cx="6" cy="4" r="2"/><circle cx="6" cy="20" r="2"/><circle cx="18" cy="20" r="2"/><path d="M6 6v12M18 18V9a5 5 0 0 0-5-5h-1m3-3-3 3 3 3"/>',
'<circle cx="12" cy="12" r="10"/><path d="M12 6v7m0 4v1"/>',
'<path d="M3 3h18v15H3zM7 18v4m10-4v4M3 14h18"/>',
'<path d="M4 19V9m8 10V4m8 15v-7"/>'
]
svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="670" height="341" viewBox="0 0 670 341" role="img" aria-label="Xuzijun57 public GitHub statistics"><rect x="1" y="1" width="668" height="339" rx="6" fill="#1e2329" stroke="#30363d" stroke-width="1.5"/><text x="36" y="53" fill="#539bf5" font-family="Georgia, Times New Roman, serif" font-size="46" font-weight="bold">Xuzijun57</text>']
for i, ((label, count), icon) in enumerate(zip(rows, icons)):
    y = 96 + 41 * i
    svg.append(f'<g transform="translate(36 {y-12})" fill="none" stroke="#539bf5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{icon}</g>')
    svg.append(f'<g fill="#adbac7" font-family="Georgia, Times New Roman, serif" font-size="24" font-weight="bold"><text x="75" y="{y+8}">{html.escape(label)}:</text><text x="278" y="{y+8}">{html.escape(count)}</text></g>')
svg.append('<g transform="translate(420 83) scale(11.5)" fill="#8b949e"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82a7.65 7.65 0 0 1 2-.27c.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></g>')
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
    text = re.sub(r"<!-- aggregate:start -->.*?<!-- aggregate:end -->", f"<!-- aggregate:start -->\n<sub>Visible contributions across all years **{total}**, including commits and other contribution types. Private activity is included only when GitHub exposes anonymous private contributions.</sub>\n<!-- aggregate:end -->", text, flags=re.S)
    readme.write_text(text, encoding="utf-8")
