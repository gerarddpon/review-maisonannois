import re, os, sys
sys.path.insert(0, "/home/user/audit/mockups")
from chrome import SHELL, NOTES

BASE_OUT="/home/user/audit/mockups"
SRC="/home/user/audit/assets"

def body_of(path):
    s=open(path,encoding="utf-8",errors="replace").read()
    m=re.search(r'<body[^>]*>(.*)</body>', s, re.S)
    body=m.group(1) if m else s
    body=re.sub(r'<script\b.*?</script>','',body,flags=re.S)
    body=re.sub(r'<noscript\b.*?</noscript>','',body,flags=re.S)
    return body

def strip_links(body):
    body=re.sub(r'<link[^>]*rel="stylesheet"[^>]*>','',body,flags=re.S)
    body=re.sub(r'<link[^>]*rel="preload"[^>]*>','',body,flags=re.S)
    return body

PAGES=[
 ("01-overview",  "account-overview",  "AVANT — état actuel", "Production", "#9b2226", "#fff"),
 ("02-order-detail","order-detail",    "AVANT — état actuel", "Production", "#9b2226", "#fff"),
 ("03-deposits",  "deposits",         "AVANT — état actuel", "Production", "#9b2226", "#fff"),
 ("04-nav",       "account-overview", "AVANT — navigation",  "Production", "#9b2226", "#fff"),
]

for slug, src, label, tag, tagbg, tagfg in PAGES:
    body = strip_links(body_of(f"{SRC}/{src}.production.html"))
    out = SHELL.format(title=f"{label} — {slug}", slug=slug, body=body, tag=tag,
                        tagbg=tagbg, tagfg=tagfg, extra="", note=NOTES[slug]["before"])
    open(f"{BASE_OUT}/screens/{slug}.before.html","w",encoding="utf-8").write(out)
    print(f"  wrote screens/{slug}.before.html  ({len(out)} bytes)")
print("done")
