import re, json
SRC="/home/user/audit/assets"

def load(n): return open(f"{SRC}/{n}.production.html",encoding="utf-8",errors="replace").read()

def find(h, pattern, label, span=1400, flags=re.S):
    m=re.search(pattern,h,flags)
    print(f"\n########## {label} ##########")
    if not m: print("  NOT FOUND"); return None
    a=max(0,m.start()-200); b=min(len(h),m.start()+span)
    print(h[a:b].replace("><",">\n<")[:span])
    return m

h=load("account-overview")
find(h, r'<main', "FIRST <main>", 900)
find(h, r'<main[^>]*>\s*<div class="shell', "SECOND <main>", 900)
find(h, r'SOLDE', "SOLDE badge", 700)
find(h, r'fixed inset-x-0 bottom-0', "FIXED BAR", 900)
find(h, r'no-scrollbar flex items-center gap-1\.5 overflow-x-auto', "CATEGORY CHIPS UL", 500)
find(h, r'-mx-\[var\(--gutter\)\] flex gap-1 overflow-x-auto', "ACCOUNT NAV UL", 1600)
find(h, r'truncate', "ANNOUNCEMENT BAR", 700)
find(h, r'Confort de lecture', "COMFORT TOGGLE", 700)

o=load("order-detail")
find(o, r'Agir sur cette commande', "ACTIONS BLOCK", 2600)
find(o, r'— R20', "SPEC ID R20", 700)
find(o, r'— R6 / R7 / R8 / R9', "SPEC IDS R6-R9", 700)

d=load("deposits")
find(d, r"versement d'avance", "DEPOSITS INTRO", 1400)
find(d, r'— R20', "DEPOSITS SPEC ID", 700)
find(d, r'\bDû\b', "DEPOSITS DÛ CARD", 1200)
