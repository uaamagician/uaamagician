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

# ================= extra sections =================
import datetime, urllib.parse

def gql(q):
    req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps({"query": q}).encode(),
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))["data"]

cc = gql('{user(login:"%s"){contributionsCollection{totalCommitContributions contributionCalendar{totalContributions weeks{contributionDays{contributionCount date weekday}}}}}}' % USER)["user"]["contributionsCollection"]
cal = cc["contributionCalendar"]
days = [d for w in cal["weeks"] for d in w["contributionDays"]]
# current streak (today may still be 0)
streak = 0
for d in reversed(days):
    if d["contributionCount"] > 0: streak += 1
    elif d is days[-1]: continue
    else: break
pub = [r for r in api(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner") if not r["fork"]]

BASE = f'<rect width="{{w}}" height="{{h}}" rx="14" fill="{BG}"/><rect x=".5" y=".5" width="{{iw}}" height="{{ih}}" rx="14" fill="none" stroke="{LINE}"/>'
STY = '''<style>.a{opacity:0;animation:in .8s cubic-bezier(.2,.7,.2,1) forwards}@keyframes in{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}</style>'''
def wrap(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{STY}'
            + BASE.format(w=w, h=h, iw=w-1, ih=h-1) + body + '</svg>')
def label(x, y, t, anchor="start", fill=ACC):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{MONO}" font-size="12" letter-spacing="3" fill="{fill}">{t}</text>'

# ---- stats row ----
items = [(f'{cal["totalContributions"]}', "CONTRIBUTIONS · 1Y"), (f'{cc["totalCommitContributions"]}', "COMMITS · 1Y"),
         (f'{len(pub)}', "PUBLIC REPOS"), (f'{streak}', "DAY STREAK")]
cw = (900 - 128) / 4
b = ""
for i, (n, l) in enumerate(items):
    x = 64 + i * cw
    if i: b += f'<line x1="{x-24:.0f}" y1="30" x2="{x-24:.0f}" y2="90" stroke="{LINE}"/>'
    b += (f'<g class="a" style="animation-delay:{i*.1:.1f}s"><text x="{x:.0f}" y="66" font-family="{SANS}" font-size="38" font-weight="200" fill="{TXT}">{n}</text>'
          f'<text x="{x:.0f}" y="88" font-family="{MONO}" font-size="10" letter-spacing="2" fill="{MUTED}">{l}</text></g>')
open("assets/stats.svg", "w", encoding="utf-8").write(wrap(900, 120, b))

# ---- heatmap ----
HW, HH, cell, gap = 900, 230, 11, 3
lv = ["#1E1915", "#4A3A2B", "#7A5F43", "#A98B63", "#D9BC8E"]
mx = max(d["contributionCount"] for d in days) or 1
def level(c):
    if c == 0: return 0
    return 1 + min(3, int((c - 1) / max(mx / 4, 1)))
b = label(64, 58, "ACTIVITY") + label(HW - 64, 58, f'{cal["totalContributions"]} contributions in the last year', "end", MUTED).replace('letter-spacing="3"', 'letter-spacing="0"')
x0, y0 = 64, 90
prev_m = None
for wi, w in enumerate(cal["weeks"]):
    m = datetime.date.fromisoformat(w["contributionDays"][0]["date"]).strftime("%b")
    if m != prev_m and wi < 50:
        b += f'<text x="{x0+wi*(cell+gap)}" y="82" font-family="{MONO}" font-size="10" fill="{MUTED}">{m.upper()}</text>'
    prev_m = m
    for d in w["contributionDays"]:
        y = y0 + d["weekday"] * (cell + gap)
        b += f'<rect class="a" style="animation-delay:{wi*.018:.2f}s" x="{x0+wi*(cell+gap)}" y="{y}" width="{cell}" height="{cell}" rx="2.5" fill="{lv[level(d["contributionCount"])]}"/>'
ly = y0 + 7 * (cell + gap) + 14
mx0 = HW - 64 - 34 - 10 - 5 * 16 + 5
b += f'<text x="{mx0-8}" y="{ly+9}" text-anchor="end" font-family="{MONO}" font-size="10" fill="{MUTED}">LESS</text>'
for i, c in enumerate(lv):
    b += f'<rect x="{mx0+i*16}" y="{ly}" width="{cell}" height="{cell}" rx="2.5" fill="{c}"/>'
b += f'<text x="{HW-64}" y="{ly+9}" text-anchor="end" font-family="{MONO}" font-size="10" fill="{MUTED}">MORE</text>'
open("assets/activity.svg", "w", encoding="utf-8").write(wrap(HW, HH, b))

# ---- projects ----
FEATURED = ["esp32-hardware-experiments", "cpp-exam-archive", "datastructure-notes", "ocean-guardian"]
byname = {r["name"]: r for r in pub}
def lines(t, maxu=40):
    out, cur, u = [], "", 0
    for ch in t:
        w = 2 if ord(ch) > 0x2E80 else 1
        if u + w > maxu:
            out.append(cur); cur, u = "", 0
            if len(out) == 2: break
        cur += ch; u += w
    if cur and len(out) < 2: out.append(cur)
    elif len(out) == 2 and cur: out[1] = out[1][:-1] + "…"
    return out
PW, PH = 900, 340
b = label(64, 58, "SELECTED WORK")
cw2, ch2 = 378, 120
for i, n in enumerate(FEATURED):
    r = byname.get(n)
    if not r: continue
    x, y = 64 + (i % 2) * (cw2 + 16), 84 + (i // 2) * (ch2 + 16)
    lang = r["language"] or "Notes"
    upd = datetime.date.fromisoformat(r["pushed_at"][:10]).strftime("%b %Y").upper()
    desc = r["description"] or f"{lang} project"
    d = "".join(f'<text x="{x+22}" y="{y+62+j*20}" font-family="{SANS}" font-size="13" fill="{MUTED}">{html.escape(t)}</text>' for j, t in enumerate(lines(desc)))
    b += (f'<g class="a" style="animation-delay:{i*.12:.2f}s"><rect x="{x}" y="{y}" width="{cw2}" height="{ch2}" rx="10" fill="#1A1613" stroke="{LINE}"/>'
          f'<text x="{x+22}" y="{y+34}" font-family="{MONO}" font-size="14" fill="{ACC}">{html.escape(n)}</text>{d}'
          f'<circle cx="{x+26}" cy="{y+ch2-20}" r="4" fill="{shades[i]}"/>'
          f'<text x="{x+38}" y="{y+ch2-16}" font-family="{SANS}" font-size="12" fill="{TXT}">{html.escape(lang)}</text>'
          f'<text x="{x+cw2-22}" y="{y+ch2-16}" text-anchor="end" font-family="{MONO}" font-size="10" letter-spacing="1" fill="{MUTED}">{upd}</text></g>')
open("assets/projects.svg", "w", encoding="utf-8").write(wrap(PW, PH, b))

# ---- footer ----
today = datetime.date.today().strftime("%Y.%m.%d")
open("assets/footer.svg", "w", encoding="utf-8").write(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="56" viewBox="0 0 900 56"><line x1="64" y1="18" x2="836" y2="18" stroke="{LINE}"/>'
    f'<text x="64" y="42" font-family="{MONO}" font-size="11" letter-spacing="2" fill="{MUTED}">{USER.upper()}</text>'
    f'<text x="836" y="42" text-anchor="end" font-family="{MONO}" font-size="11" letter-spacing="1" fill="{MUTED}">UPDATED {today}</text></svg>')
print("extra ok", streak)
