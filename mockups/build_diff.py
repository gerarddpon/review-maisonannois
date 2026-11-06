"""Generate a human-reviewable patch document per screen.

The production DOM is minified onto a single line, so a classic unified diff
is unreadable AND cannot be applied with `patch`. Instead we record each
correction as an explicit AVANT → APRÈS block: the exact production fragment
replaced by the exact corrected fragment. The pair
screens/<slug>.before.html ↔ screens/<slug>.after.html remains the
machine-comparable artefact.
"""
import re, os, sys, difflib
sys.path.insert(0, "/home/user/audit/mockups")
import build_after as B

OUT="/home/user/audit/mockups/diff"
os.makedirs(OUT, exist_ok=True)

def pretty(html, maxlen=1400):
    h=re.sub(r'>\s*<','>\n<',html)
    h=re.sub(r'\n\s*\n','\n',h)
    lines=[l.strip() for l in h.split("\n") if l.strip()]
    out="\n".join(lines)
    if len(out)>maxlen:
        out=out[:maxlen].rstrip()+"\n      … (tronqué)"
    return out

def changed_blocks(old, new):
    """Return the list of (removed, added) blocks between two strings."""
    a=re.sub(r'>\s*<','>\n<',old).split("\n")
    b=re.sub(r'>\s*<','>\n<',new).split("\n")
    blocks=[]
    for tag,i1,i2,j1,j2 in difflib.SequenceMatcher(None,a,b).get_opcodes():
        if tag=='equal': continue
        blocks.append(("\n".join(a[i1:i2]).strip(), "\n".join(b[j1:j2]).strip()))
    return blocks

LABEL={
 "p_landmark":  ("S-01", "Un seul <main>, un seul #contenu"),
 "p_comfort":   ("S-04", "Le contrôle « Confort de lecture » existe sur mobile"),
 "p_badge":     ("O-01", "Le solde est une action, pas une dette"),
 "p_contextbar":("S-02", "Barre de bas de page : 87 px → 61 px, contenu contextuel"),
 "p_nav":       ("S-05", "Navigation groupée en 5 sections"),
 "p_actions":   ("C-02", "Les blocages deviennent des actions"),
 "p_deposits_intro":("C-03", "Langage clair d'abord, la référence ensuite"),
 "p_balance_label":("C-03", "« Dû » devient « À régler au retrait »"),
 "p_specids":   ("C-01", "Les identifiants de spécification quittent l'affichage"),
 "p_footer_label":("G-09", "Le pied de page ne répète plus le nom accessible de l'en-tête"),
 "p_scope":     ("—", "Périmètre d'application du correctif CSS"),
}

def build(slug, src, patches):
    h=B.load(src); h=B.body_of(h); h=B.strip_scripts(h)
    sections=[]
    for fn in patches:
        before=h
        after=fn(h)
        if after==before: continue
        ref,title=LABEL.get(fn.__name__,("—",fn.__name__))
        blocks=changed_blocks(before, after)
        if not blocks: continue
        sections.append((ref,title,blocks))
        h=after
    out=[]
    out.append(f"PATCH DOCUMENT — {slug}")
    out.append("="*78)
    out.append("")
    out.append("Maquette : screens/%s.before.html  →  screens/%s.after.html" % (slug, slug))
    out.append("Chaque bloc ci-dessous est le fragment RÉEL de production remplacé par son")
    out.append("fragment corrigé. Rien d'autre n'est touché : le reste du DOM est identique.")
    out.append("")
    n=0
    for ref,title,blocks in sections:
        n+=1
        out.append("")
        out.append(f"── {n}. [{ref}] {title} " + "─"*max(0, 62-len(title)))
        for k,(rem,add) in enumerate(blocks,1):
            out.append("")
            out.append(f"   AVANT")
            out.append("   " + pretty(rem).replace("\n","\n   "))
            out.append("")
            out.append(f"   APRÈS")
            out.append("   " + pretty(add).replace("\n","\n   "))
    txt="\n".join(out)+"\n"
    open(f"{OUT}/{slug}.diff","w",encoding="utf-8").write(txt)
    print(f"  {slug}.diff : {n} corrections, {len(txt)} bytes")

build("01-overview","account-overview",
      [B.p_landmark,B.p_scope,B.p_comfort,B.p_badge,B.p_contextbar,B.p_nav,B.p_footer_label,B.p_specids])
build("02-order-detail","order-detail",
      [B.p_landmark,B.p_scope,B.p_comfort,B.p_actions,B.p_contextbar,B.p_nav,B.p_footer_label,B.p_specids])
build("03-deposits","deposits",
      [B.p_landmark,B.p_scope,B.p_comfort,B.p_balance_label,B.p_deposits_intro,B.p_contextbar,B.p_nav,B.p_footer_label,B.p_specids])
build("04-nav","account-overview",
      [B.p_landmark,B.p_scope,B.p_comfort,B.p_contextbar,B.p_nav,B.p_footer_label,B.p_specids])
print("done")
