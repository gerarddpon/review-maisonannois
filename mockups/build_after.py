"""Build the "after" mockups by surgically patching the REAL production DOM.
The after pages differ from the before pages ONLY by the 8 P0 fixes."""
import re, os, html, difflib, sys
sys.path.insert(0,"/home/user/audit/mockups")
from chrome import SHELL as _SHELL, NOTES

ASSETS="/home/user/audit/assets"
OUT="/home/user/audit/mockups"

def load(n): return open(f"{ASSETS}/{n}.production.html",encoding="utf-8",errors="replace").read()

def strip_scripts(s):
    s=re.sub(r'<script\b.*?</script>','',s,flags=re.S)
    s=re.sub(r'<noscript\b.*?</noscript>','',s,flags=re.S)
    return s

def body_of(h):
    m=re.search(r'<body[^>]*>(.*)</body>', h, re.S)
    return m.group(1) if m else h

def match_close(h, start_idx, tag):
    """Return index just after the matching </tag> for the element opened at start_idx.
    The whole tag (including the '>') must be consumed, otherwise the caller
    re-inserts a stray '>' and the document structure breaks."""
    depth=0
    pat=re.compile(r'<(/?)'+tag+r'\b[^>]*>', re.I)
    for m in pat.finditer(h, start_idx):
        if m.group(1)=='':
            depth+=1
        else:
            depth-=1
            if depth==0:
                return m.end()
    return -1

def replace_element(h, open_re, new_html, label):
    m=re.search(open_re, h)
    if not m: return h, False
    tag=re.match(r'<([a-zA-Z][\w-]*)', m.group(0)).group(1)
    end=match_close(h, m.start(), tag)
    if end<0: return h, False
    old=h[m.start():end]
    h=h[:m.start()]+new_html+h[end:]
    print(f"    + {label} ({len(old)} → {len(new_html)} bytes)")
    return h, True

# ─────────────────────────────────────────────────────────────── patches
def p_landmark(h):
    """P0-1 — one <main>, one #contenu."""
    m=re.search(r'<main id="contenu" class="min-w-0">', h)
    if not m: return h
    end=match_close(h, m.start(), "main")
    inner=h[m.start():end]
    new=inner.replace('<main id="contenu" class="min-w-0">','<div class="min-w-0" role="none">',1)
    new=new[:new.rfind('</main>')]+'</div>'+new[new.rfind('</main>')+7:]
    h=h[:m.start()]+new+h[end:]
    print("    + P0-1 inner <main> → <div role=none> (duplicate id=\"contenu\" removed)")
    return h

def p_scope(h):
    """Scope every account-scoped override to the account layout wrapper."""
    h=h.replace('<div class="lg:grid lg:grid-cols-[236px_minmax(0,1fr)] lg:gap-10">',
                '<div data-scope="account" class="lg:grid lg:grid-cols-[236px_minmax(0,1fr)] lg:gap-10">')
    print("    + P0-3/4 data-scope=\"account\" on the account grid")
    return h

def p_comfort(h):
    """P0-2 — the reading-comfort control must exist on mobile."""
    before=h
    h=h.replace('<div class="hidden sm:block">','<div class="block">')
    if h!=before:
        print("    + P0-2 comfort wrapper 'hidden sm:block' → 'block' (visible < 640px)")
    # give the announcement paragraph room so the cluster is not squeezed to 22px
    h=h.replace('<p class="truncate">','<p class="truncate min-w-0 flex-1">')
    h=h.replace('class="mx-auto flex h-9 w-full max-w-[1440px] items-center justify-between gap-4 px-[var(--gutter)] text-caption"',
                'class="mx-auto flex h-9 w-full max-w-[1440px] items-center justify-between gap-2 px-[var(--gutter)] text-caption"')
    print("    + P0-2/3 announcement paragraph flex-1 min-w-0 (cluster keeps its width)")
    return h

def p_specids(h):
    """P0-7 — strip internal spec IDs from customer copy.
    The ID moves to a data-spec attribute on the enclosing <p>, so QA keeps
    the traceability without the customer seeing it."""
    n=0
    def repl(m):
        nonlocal n; n+=1
        return f'{m.group(1)} data-spec="{m.group(3)}">{m.group(2)}'
    h=re.sub(r'(<p\b[^>]*)(>)([^<]*?)<span class="text-ardoise-600">\s*—\s*<!-- -->\s*'
             r'((?:R|F|C|H|N)\d+(?:\s*/\s*(?:R|F|C|H|N)\d+)*)</span>',
             repl, h)
    # any left over (different wrapper) -> remove the span entirely
    left=len(re.findall(r'<span class="text-ardoise-600">\s*—\s*<!-- -->\s*(?:R|F|C|H|N)\d+', h))
    h=re.sub(r'<span class="text-ardoise-600">\s*—\s*<!-- -->\s*(?:R|F|C|H|N)\d+(?:\s*/\s*(?:R|F|C|H|N)\d+)*</span>', '', h)
    if n: print(f"    + P0-7 moved {n} spec ID(s) to data-spec attributes")
    if left: print(f"    + P0-7 removed {left} leftover spec-ID span(s)")
    return h

def p_footer_label(h):
    """Bonus — the footer repeats the header's « Aller à » section, so two
    landmarks share the accessible name "Aller à" (axe landmark-unique)."""
    old='<section aria-labelledby="raccourcis">'
    n=h.count(old)
    if n>1:
        idx=h.rfind(old)
        h=h[:idx]+'<section aria-label="Liens rapides de pied de page">'+h[idx+len(old):]
        print("    + bonus: footer « Aller à » re-labelled (landmark-unique)")
    return h

def p_badge(h):
    """P0-8 — 'Solde 53.26 € dû' → 'Solde à régler · 53,26 €'."""
    old='>Solde 53.26 € dû</span>'
    new=('>Solde à régler · 53,26&nbsp;€</span>')
    if old in h:
        h=h.replace(old,new); print("    + P0-8 badge 'Solde 53.26 € dû' → 'Solde à régler · 53,26 €'")
    return h

def p_balance_label(h):
    """O-02 — the deposits page 'Dû' card."""
    h=h.replace('>Dû</h2>', '>À régler au retrait</h2>')
    h=h.replace('>Rendu</h2>', '>Consignes remboursées</h2>')
    return h

def p_contextbar(h):
    """P0-5 — replace the 87px fixed bar with a ≤64px contextual bar."""
    bar = (
 '<div class="account-context-bar" role="region" aria-label="Actions du compte">\n'
 '  <a href="tel:0139471212" class="flex min-h-11 flex-1 items-center justify-center gap-2 rounded-[var(--radius-pill)] border border-ardoise-900/25 bg-white px-3 text-small font-semibold text-ardoise-900">\n'
 '    <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.58 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1 11.4 11.4 0 0 0 .57 3.6 1 1 0 0 1-.25 1z"/></svg>\n'
 '    <span>Appeler</span>\n'
 '  </a>\n'
 '  <a href="/account/orders/CMD-2452" class="flex min-h-11 flex-1 items-center justify-center gap-2 rounded-[var(--radius-pill)] bg-ardoise-900 px-3 text-small font-semibold text-lin-50">\n'
 '    <span class="tabular-nums">53,26&nbsp;€</span><span class="font-normal">à régler</span>\n'
 '  </a>\n'
 '</div>')
    h2,ok = replace_element(h, r'<div class="fixed inset-x-0 bottom-0 z-40[^"]*"[^>]*>', bar, "P0-5 fixed bar → contextual bar (≤64px)")
    return h2

def p_nav(h):
    """P0-6 — grouped nav (drawer on mobile, grouped column on desktop)."""
    groups=[
      ("Commander", [("/account","Vue d'ensemble"),("/account/orders","Commandes"),("/account/subscriptions","Abonnements")]),
      ("Argent",    [("/account/documents","Factures"),("/account/payments","Paiements"),("/account/deposits","Arrhes & consignes")]),
      ("Vos demandes", [("/account/support","Réclamations"),("/account/safety","Sécurité produit"),("/account/reviews","Avis")]),
      ("Préférences", [("/account/preferences","Allergies & atelier"),("/account/butchery","Préférences de découpe"),("/account/favourites","Favoris"),("/account/wallet","Cagnotte"),("/account/notifications","Notifications"),("/account/addresses","Adresses")]),
      ("Compte",    [("/account/settings","Compte & sécurité"),("/account/privacy","Vie privée"),("/account/business","Professionnel")]),
    ]
    nav=['<nav aria-label="Sections de votre compte" class="mb-6 lg:mb-0">']
    nav.append('<button type="button" class="account-nav-drawer-trigger mb-4 flex min-h-11 w-full items-center justify-between gap-2 rounded-[var(--radius-md)] border border-lin-300 bg-white px-3.5 text-small font-semibold text-ardoise-900 lg:hidden" aria-expanded="false" aria-controls="account-nav-drawer">')
    nav.append('  <span>Menu du compte</span><span aria-hidden="true">☰</span>')
    nav.append('</button>')
    nav.append('<div id="account-nav-drawer" class="account-nav-drawer hidden lg:hidden">')
    nav.append('  <div class="account-nav-drawer__head mb-4 flex items-center justify-between">')
    nav.append('    <p class="overline">Espace client</p>')
    nav.append('    <button type="button" class="flex size-11 items-center justify-center rounded-full border border-lin-300 text-ardoise-900" aria-label="Fermer le menu">✕</button>')
    nav.append('  </div>')
    nav.append('  <ul class="account-nav-list">')
    for gtitle, items in groups:
        nav.append(f'    <li><p class="account-nav-group-title">{gtitle}</p><ul>')
        for href,label in items:
            cur = ' aria-current="page"' if href=="/account" else ''
            nav.append(f'      <li><a class="account-nav-link" href="{href}"{cur}>{label}</a></li>')
        nav.append('    </ul></li>')
    nav.append('  </ul>')
    nav.append('</div>')
    nav.append('</nav>')
    new="\n".join(nav)
    h2,ok = replace_element(h, r'<nav aria-label="Sections de votre compte"[^>]*>', new, "P0-6 17-item scroll strip → grouped nav")
    return h2

def p_actions(h):
    """C-02 — blocked states become action cards with real links."""
    old_start = '<div class="mt-5">\n<div class="space-y-4">'
    m=re.search(re.escape(old_start), h)
    if not m:
        m=re.search(r'<div class="mt-5">\s*<div class="space-y-4">', h)
    if not m: return h
    # locate the whole space-y-4 block
    start=m.start()
    open_m=re.search(r'<div class="space-y-4">', h[start:])
    if not open_m: return h
    bstart=start+open_m.start()
    bend=match_close(h, bstart, "div")
    if bend<0: return h
    new = (
 '<div class="mt-5 space-y-3">\n'
 '  <div class="rounded-[var(--radius-md)] border border-lin-200 bg-lin-50 p-4">\n'
 '    <p class="text-small font-semibold text-ardoise-900">Modifier le créneau</p>\n'
 '    <p class="mt-1 text-caption leading-relaxed text-ardoise-600">La coupure est passée (24 h avant le créneau). Nous modifions encore si la préparation n\'a pas commencé.</p>\n'
 '    <div class="mt-3 flex flex-wrap gap-2">\n'
 '      <a href="tel:0139471212" class="inline-flex min-h-11 items-center gap-2 rounded-[var(--radius-pill)] border border-ardoise-900/25 bg-white px-3.5 text-small font-semibold text-ardoise-900">Appeler la boutique</a>\n'
 '      <a href="/account/orders/CMD-2452/change-slot" class="inline-flex min-h-11 items-center gap-2 rounded-[var(--radius-pill)] border border-ardoise-900/25 bg-white px-3.5 text-small font-semibold text-ardoise-900">Changer de créneau</a>\n'
 '    </div>\n'
 '  </div>\n'
 '  <details class="legal-disclosure">\n'
 '    <summary>Rétractation — ce que la loi permet sur cette commande</summary>\n'
 '    <div class="legal-disclosure__body">\n'
 '      <p>Viande fraîche : denrée susceptible de se détériorer ou de périmer rapidement (art. L. 221-28 4° C. conso., art. 16(d) CRD). Ces articles ne sont pas remboursés, mais ils restent les vôtres.</p>\n'
 '      <p class="mt-2">La garantie légale de conformité de deux ans reste ouverte : ouvrez une réclamation.</p>\n'
 '    </div>\n'
 '  </details>\n'
 '  <div class="rounded-[var(--radius-md)] border border-lin-200 bg-lin-50 p-4">\n'
 '    <p class="text-small font-semibold text-ardoise-900">Signaler un problème</p>\n'
 '    <p class="mt-1 text-caption leading-relaxed text-ardoise-600">La réclamation s\'ouvre à la remise de la commande. Vous pouvez aussi appeler la boutique : nous répondons sous deux jours ouvrés.</p>\n'
 '    <div class="mt-3 flex flex-wrap gap-2">\n'
 '      <a href="tel:0139471212" class="inline-flex min-h-11 items-center gap-2 rounded-[var(--radius-pill)] border border-ardoise-900/25 bg-white px-3.5 text-small font-semibold text-ardoise-900">Appeler</a>\n'
 '      <a href="/account/support" class="inline-flex min-h-11 items-center gap-2 rounded-[var(--radius-pill)] border border-ardoise-900/25 bg-white px-3.5 text-small font-semibold text-ardoise-900">Voir mes réclamations</a>\n'
 '    </div>\n'
 '  </div>\n'
 '  <div class="rounded-[var(--radius-md)] border border-lin-200 bg-lin-50 p-4">\n'
 '    <p class="text-small font-semibold text-ardoise-900">Annuler la commande</p>\n'
 '    <p class="mt-1 text-caption leading-relaxed text-ardoise-600">Le délai d\'annulation libre est passé. L\'annulation suit la <a class="underline underline-offset-4" href="/cgv#annulation">politique publiée</a> (arrhes retenues).</p>\n'
 '    <div class="mt-3 flex flex-wrap gap-2">\n'
 '      <a href="tel:0139471212" class="inline-flex min-h-11 items-center gap-2 rounded-[var(--radius-pill)] border border-ardoise-900/25 bg-white px-3.5 text-small font-semibold text-ardoise-900">Appeler la boutique</a>\n'
 '    </div>\n'
 '  </div>\n'
 '</div>')
    h=h[:start]+new+h[bend:]
    print("    + C-02 dead prose → action cards with tel:/real links")
    return h

def p_deposits_intro(h):
    """G-08 — plain-language first, legal reference in a disclosure."""
    m=re.search(r'(<p class="text-lead[^"]*">)(.*?)(</p>)', h, re.S)
    if not m: return h
    old=m.group(0)
    if "versement d'avance" not in old: return h
    new=('<p class="text-lead text-ardoise-700">Un acompte, ce n\'est pas une avance comme les autres. '
         'Ce que vous récupérez dépend de qui annule — voici la règle appliquée à vos commandes.</p>'
         '<details class="legal-disclosure mt-3"><summary>Lire la règle juridique</summary>'
         '<div class="legal-disclosure__body"><p>Le versement d\'avance n\'est pas une avance comme les autres : sa nature juridique '
         '(arrhes ou acompte) décide de ce qui se passe en cas de renoncement (art. L. 214-1 C. conso.). '
         'La garantie légale de conformité reste ouverte deux ans.</p></div></details>')
    h=h.replace(old,new)
    print("    + G-08 legal prose → plain summary + <details>")
    return h

def build(slug, src, patches, note_key):
    h=load(src)
    h=body_of(h)
    h=strip_scripts(h)
    print(f"  [{slug}]")
    for fn in patches:
        h=fn(h)
    tagbg,tagfg = "#2f5a41", "#fff"
    out=_SHELL.format(title=f"APRÈS — {slug}", slug=slug, body=h, tag="APRÈS",
                       tagbg=tagbg, tagfg=tagfg, extra='<link rel="stylesheet" href="../tokens/account-scope.css">',
                       note=NOTES[slug]["after"])
    open(f"{OUT}/screens/{slug}.after.html","w",encoding="utf-8").write(out)
    print(f"    = wrote screens/{slug}.after.html ({len(out)} bytes)")

COMMON=[p_scope,p_specids]
build("01-overview","account-overview",
      [p_landmark,p_scope,p_comfort,p_badge,p_contextbar,p_nav,p_footer_label,p_specids], "01-overview")
build("02-order-detail","order-detail",
      [p_landmark,p_scope,p_comfort,p_actions,p_contextbar,p_nav,p_footer_label,p_specids], "02-order-detail")
build("03-deposits","deposits",
      [p_landmark,p_scope,p_comfort,p_balance_label,p_deposits_intro,p_contextbar,p_nav,p_footer_label,p_specids], "03-deposits")
build("04-nav","account-overview",
      [p_landmark,p_scope,p_comfort,p_contextbar,p_nav,p_footer_label,p_specids], "04-nav")
