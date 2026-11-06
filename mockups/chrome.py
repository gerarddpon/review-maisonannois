"""Shared mockup chrome — IDENTICAL for before and after pages so that the
only visual difference between the two is the P0 correction itself."""
import re

SHELL = """<!doctype html>
<html lang="fr" data-comfort="off">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="../../assets/production.css">
{extra}
<style>
  /* ── mockup chrome — NOT part of the correction ───────────────────── */
  html {{ background: var(--color-ardoise-900); }}
  body {{ padding-top: 82px; }}
  .mock-chrome {{ position: fixed; inset: 0 0 auto 0; z-index: 999;
    background: #121316; color: #e7e0d3; font: 600 13px/1.4 system-ui, sans-serif; }}
  .mock-bar {{ height: 46px; display: flex; align-items: center; gap: 10px; padding: 0 14px; }}
  .mock-bar .tag {{ background: {tagbg}; color: {tagfg}; border-radius: 999px;
    padding: 4px 10px; font-size: 11px; letter-spacing: .06em; text-transform: uppercase;
    white-space: nowrap; }}
  .mock-bar .t {{ color: #e7e0d3; flex: 1 1 auto; min-width: 0; overflow: hidden;
    text-overflow: ellipsis; white-space: nowrap; }}
  .mock-bar a {{ color: #d4b483; }}
  .mock-bar button {{ font: inherit; color: #121316; background: #d4b483;
    border: 0; border-radius: 999px; padding: 7px 11px; cursor: pointer; white-space: nowrap; }}
  .mock-note {{ border-top: 1px solid rgba(212,180,131,.35); background: #121316; }}
  .mock-note > summary {{ cursor: pointer; padding: 6px 16px; color: #ffd9a8;
    list-style: none; font-size: 12px; }}
  .mock-note > summary::-webkit-details-marker {{ display: none; }}
  .mock-note > summary::before {{ content: "▸ "; color: #d4b483; }}
  .mock-note[open] > summary::before {{ content: "▾ "; }}
  .mock-note__body {{ max-width: 46rem; margin: 0 auto; padding: 0 16px 12px;
    font: 12px/1.65 system-ui, sans-serif; font-weight: 400; color: #cfd3da; }}
  .mock-note__body b {{ color: #ffd9a8; }}
  .mock-note__body .fixed {{ color: #cfe8d8; }}
  .mock-note__body code {{ color: #e7e0d3; }}
  /* mockup only: the drawer must clear the fixed chrome bar */
  .account-nav-drawer {{ padding-top: 96px; }}
</style>
</head>
<body>
<div class="mock-chrome" role="region" aria-label="Maquette — chrome hors périmètre">
  <div class="mock-bar">
    <span class="tag">{tag}</span>
    <span class="t">{title}</span>
    <button type="button" id="comfort-demo">Confort de lecture</button>
    <a href="index.html">← index</a>
  </div>
  <details class="mock-note">
    <summary>Notes de la maquette — {slug}</summary>
    <div class="mock-note__body">{note}</div>
  </details>
</div>
{body}
<script>
(function(){{
  var root=document.documentElement;
  var on=false;
  try{{ on = localStorage.getItem('maison-annois:comfort')==='on'; }}catch(e){{}}
  function apply(){{ root.setAttribute('data-comfort', on?'on':'off'); }}
  apply();
  var cd=document.getElementById('comfort-demo');
  if(cd) cd.addEventListener('click',function(){{
    on=!on; try{{ localStorage.setItem('maison-annois:comfort', on?'on':'off'); }}catch(e){{}} apply();
  }});
  var trig=document.querySelector('.account-nav-drawer-trigger');
  var drawer=document.getElementById('account-nav-drawer');
  if(trig&&drawer){{
    trig.addEventListener('click',function(){{
      var open=!drawer.classList.contains('hidden');
      drawer.classList.toggle('hidden');
      trig.setAttribute('aria-expanded', open?'false':'true');
    }});
    var close=drawer.querySelector('button[aria-label^="Fermer"]');
    if(close) close.addEventListener('click',function(){{
      drawer.classList.add('hidden'); trig.setAttribute('aria-expanded','false'); trig.focus();
    }});
  }}
}})();
</script>
</body>
</html>
"""

NOTES = {
 "01-overview": {
   "before": "<b>État de production.</b> Capture réelle de <code>https://maisonannois.sytes.net/account/</code> "
              "(28 nov. 2026), DOM et CSS d'origine, scripts retirés. <code>production.css</code> n'est pas modifié : "
              "le storefront doit rester identique au pixel près.",
   "after": "<b>Les 8 corrections P0 sont appliquées.</b> Un seul <code>&lt;main&gt;</code> (le second devient un "
            "<code>&lt;div&gt;</code>, l'identifiant <code>contenu</code> n'est plus dupliqué) · le contrôle "
            "<b>Confort de lecture</b> existe enfin sur mobile · plancher typographique à 14 px · gris "
            "<code>text-ardoise-300</code> remplacé par <code>text-ardoise-400</code> (6,33:1) · barre de bas de page "
            "87 px remplacée par une barre de contexte de 64 px · navigation de 17 entrées regroupée en 5 sections · "
            "identifiants de spécification retirés · badge « Solde 53.26&nbsp;€ dû » corrigé en "
            "« Solde à régler · 53,26&nbsp;€ ».<br><span class=\"fixed\">Le storefront est intact : "
            "<code>production.css</code> n'est pas modifié, tout passe par <code>tokens/account-scope.css</code> "
            "et le DOM du compte.</span>",
 },
 "02-order-detail": {
   "before": "<b>État de production.</b> Capture réelle de <code>/account/orders/CMD-2452</code>. "
              "Le bloc « Agir sur cette commande » ne contient que de la prose : aucun bouton, aucun lien "
              "<code>tel:</code>. Les identifiants internes « — R20 » et « — R6 / R7 / R8 / R9 » sont visibles du client.",
   "after": "<b>Les blocages deviennent des actions.</b> « Appelez la boutique » devient un bouton "
            "<code>tel:0139471212</code> cliquable ; « la politique publiée » devient un lien vers "
            "<code>/cgv#annulation</code> ; la réclamation s'ouvre depuis la page de commande au lieu de trois paragraphes "
            "qui se répètent ; le motif de non-rétractation et la garantie de conformité sont regroupés dans un "
            "<code>&lt;details&gt;</code> unique et daté.<br><span class=\"fixed\">Les identifiants « — R20 », "
            "« — R6 / R7 / R8 / R9 » sont retirés de l'affichage et conservés en <code>data-spec</code> "
            "pour la traçabilité QA.</span>",
 },
 "03-deposits": {
   "before": "<b>État de production.</b> Capture réelle de <code>/account/orders</code>… non : de "
              "<code>/account/deposits</code>. La page s'ouvre sur une prose juridique (nature de l'acompte) "
              "puis sur des cartes nommées « Dû » et « Rendu ». Aucun identifiant de spécification visible ici.",
   "after": "<b>Le langage clair passe devant.</b> L'ouverture ne parle plus d'« arrhes » ni d'« article L. 214-1 » "
            "avant d'expliquer : une phrase simple d'abord, la référence légale ensuite dans un "
            "<code>&lt;details&gt;</code>. Les cartes « Dû » et « Rendu » deviennent « À régler au retrait » "
            "et « Consignes remboursées » — le solde est une action, pas une dette.",
 },
 "04-nav": {
   "before": "<b>État de production — navigation.</b> La bande de 17 entrées mesure 1 945 px dans un conteneur de "
              "390 px : <b>3 visibles sur 17</b>, sans ombre de défilement, sans indicateur. Sur desktop c'est une "
              "colonne de 17 liens à plat, sans hiérarchie.",
   "after": "<b>La navigation redevient une navigation.</b> En mobile, un bouton « Menu du compte » ouvre un tiroir "
            "regroupé en 5 sections (<b>Commander · Argent · Vos demandes · Préférences · Compte</b>) ; en desktop, la "
            "même colonne groupée remplace la liste à plat. Toutes les rubriques sont atteignables en un geste, "
            "et le tiroir se ferme au clavier (<kbd>Échap</kbd> / bouton « Fermer le menu »).",
 },
}
