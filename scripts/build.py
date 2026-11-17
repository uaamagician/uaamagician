import os, json, urllib.request, html

USER, TOKEN = "uaamagician", os.environ.get("GH_TOKEN", "")
BG, LINE, TXT, MUTED, ACC = "#14110F", "#2A241F", "#EDE6DA", "#8C8175", "#C8A97E"
MONO = "SF Mono,Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,'Helvetica Neue',Inter,'Segoe UI',Arial,sans-serif"

def api(u):
    h = {"Accept": "application/vnd.github+json"}
    if TOKEN: h["Authorization"] = f"Bearer {TOKEN}"
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=h)))

# 含私有倉庫（需要有 repo 權限的 token）；只統計語言比例，不會顯示倉庫名稱
url = "https://api.github.com/user/repos?per_page=100&affiliation=owner" if TOKEN else f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner"
repos = [r for r in api(url) if not r["fork"] and r["name"] != USER]
tot = {}
for r in repos:
    for k, v in api(r["languages_url"]).items(): tot[k] = tot.get(k, 0) + v
top = sorted(tot.items(), key=lambda x: -x[1])[:6]
S = sum(tot.values()) or 1
names = [k for k, _ in top[:4]]

# ---------- header ----------
W, H = 900, 240
header = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<pattern id="g" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="{LINE}" stroke-width="1" opacity=".55"/></pattern>
<radialGradient id="glow" cx="85%" cy="0%" r="70%"><stop offset="0" stop-color="{ACC}" stop-opacity=".16"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/></radialGradient>
<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{ACC}"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/></linearGradient>
</defs>
<style>
.a{{opacity:0;animation:in .9s cubic-bezier(.2,.7,.2,1) forwards}}
.d1{{animation-delay:.15s}}.d2{{animation-delay:.4s}}.d3{{animation-delay:.65s}}
@keyframes in{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
.ln{{transform-origin:0 0;transform:scaleX(0);animation:ln 1.4s cubic-bezier(.2,.7,.2,1) .3s forwards}}
@keyframes ln{{to{{transform:scaleX(1)}}}}
.cur{{animation:b 1.1s steps(1) infinite}}@keyframes b{{50%{{opacity:0}}}}
</style>
<rect width="{W}" height="{H}" rx="14" fill="{BG}"/>
<rect width="{W}" height="{H}" rx="14" fill="url(#g)"/>
<rect width="{W}" height="{H}" rx="14" fill="url(#glow)"/>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{LINE}"/>
<text class="a" x="64" y="70" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{ACC}">~ / PROFILE</text>
<text class="a d1" x="62" y="134" font-family="{SANS}" font-size="52" font-weight="200" letter-spacing="1" fill="{TXT}">{USER}<tspan class="cur" fill="{ACC}">_</tspan></text>
<g class="a d2"><rect class="ln" x="64" y="158" width="260" height="1.5" fill="url(#fade)"/></g>
<text class="a d3" x="64" y="190" font-family="{MONO}" font-size="13" letter-spacing="1" fill="{MUTED}">{"  /  ".join(html.escape(n) for n in names)}</text>
</svg>'''
open("assets/header.svg", "w", encoding="utf-8").write(header)

# ---------- languages ----------
W2, H2 = 900, 215
shades = ["#C8A97E", "#A98B63", "#8A6F4E", "#6E5841", "#574636", "#463829"]
L = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W2}" height="{H2}" viewBox="0 0 {W2} {H2}">
<style>
.a{{opacity:0;animation:in .8s cubic-bezier(.2,.7,.2,1) forwards}}
@keyframes in{{from{{opacity:0;transform:translateY(6px)}}to{{opacity:1;transform:none}}}}
.s{{transform-box:fill-box;transform-origin:left center;transform:scaleX(0);animation:g 1.1s cubic-bezier(.2,.7,.2,1) forwards}}
@keyframes g{{to{{transform:scaleX(1)}}}}
</style>
<rect width="{W2}" height="{H2}" rx="14" fill="{BG}"/>
<rect x=".5" y=".5" width="{W2-1}" height="{H2-1}" rx="14" fill="none" stroke="{LINE}"/>
<text x="64" y="58" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{ACC}">LANGUAGES</text>
<text x="{W2-64}" y="58" text-anchor="end" font-family="{MONO}" font-size="12" fill="{MUTED}">by code volume</text>
<clipPath id="c"><rect x="64" y="80" width="{W2-128}" height="8" rx="4"/></clipPath><g clip-path="url(#c)"><rect x="64" y="80" width="{W2-128}" height="8" fill="{LINE}"/>''']
bw, x = W2 - 128, 64
for i, (k, v) in enumerate(top):
    w = bw * v / S
    L.append(f'<rect class="s" style="animation-delay:{i*.12:.2f}s" x="{x:.1f}" y="80" width="{max(w-2,2):.1f}" height="8" fill="{shades[i]}"/>')
    x += w
L.append('</g>')
for i, (k, v) in enumerate(top):
    col, row = i % 3, i // 3
    cx, cy = 64 + col * 260, 130 + row * 36
    L.append(f'<g class="a" style="animation-delay:{.5+i*.08:.2f}s"><circle cx="{cx+4}" cy="{cy-4}" r="4" fill="{shades[i]}"/>'
             f'<text x="{cx+18}" y="{cy}" font-family="{SANS}" font-size="15" fill="{TXT}">{html.escape(k)}</text>'
             f'<text x="{cx+200}" y="{cy}" text-anchor="end" font-family="{MONO}" font-size="13" fill="{MUTED}">{v/S*100:.1f}%</text></g>')
L.append('</svg>')
open("assets/languages.svg", "w", encoding="utf-8").write("\n".join(L))
print(top)
