# Maquettes avant / après — Espace client Maison Annois

**Objet.** Huit corrections P0 issues de l'audit UI/UX (`/home/user/audit/rapport-audit-uiux-maison-annois__FR.md` / `__EN.md`),
matérialisées sur le **DOM réel et authentifié** de `maisonannois.sytes.net/account/`, avec la feuille de style de
production **non modifiée**.

> **English summary.** Four production screens, each rebuilt twice: *before* = the captured production DOM untouched,
> *after* = the same DOM with the eight P0 corrections applied. Nothing was redesigned — the after pages differ from the
> before pages only by the fixes, so the diff is the specification. Verified with axe-core 4.10.2 at 390 × 844 and
> 1440 × 1000: axe rule categories drop from 4 to 1, `<main>` count from 2 to 1, sub-14 px text nodes from 81 to 0,
> the fixed bottom bar from 87 px to 61 px. The storefront is untouched — every correction is scoped to
> `[data-scope="account"]` or to an `.account-*` class, and no shared design token is redefined.

---

## 1 · Contenu

| Chemin | Rôle |
|---|---|
| `tokens/account-scope.css` | **La correction.** Les 8 P0, cloisonnées dans `[data-scope="account"]`. À charger après `production.css`. |
| `screens/01-overview.{before,after}.html` | `/account` — vue d'ensemble |
| `screens/02-order-detail.{before,after}.html` | `/account/orders/CMD-2452` — détail de commande |
| `screens/03-deposits.{before,after}.html` | `/account/deposits` — arrhes & consignes |
| `screens/04-nav.{before,after}.html` | `/account` — colonne de navigation |
| `diff/*.diff` | Document de patch par écran : chaque correction est le fragment réel de production remplacé par son fragment corrigé. |
| `components/index.html` | Les huit composants isolés, avant / après |
| `index.html` | Le hub annoté : métriques, correspondances, règle de confinement |
| `../assets/production.css` | La feuille de style de production, **non modifiée** (93 064 octets) |
| `../assets/*.production.html` | Les quatre captures de DOM d'origine |

Scripts de génération : `build_before.py`, `build_after.py`, `chrome.py` (chrome partagé), `build_diff.py`,
`validate.py` (axe + mesures), `verify_final.py` (vérification finale).

---

## 2 · Correspondance constat → correction → preuve

| Réf. audit | Constat de production | Correction appliquée | Preuve mesurée (avant → après) |
|---|---|---|---|
| **S-01** | Deux `<main>` imbriqués, **tous deux `id="contenu"`**. Identifiant dupliqué, cible de saut clavier ambiguë. | Le `<main>` intérieur devient `<div class="min-w-0" role="none">`. | 2 `<main>` + `#contenu` en double → **1 `<main>`, 0 doublon**. |
| **S-04** | « Confort de lecture » : enveloppe `hidden sm:block` → `display:none` sous 640 px. Rectangle du bouton : `[0,0,0,0]`. | Enveloppe repassée en `block`. L'état `data-comfort` sur `<html>` pilote l'échelle typographique. | Invisible (0×0) à 390 px → **visible, 107 × 50 px**. |
| **S-02** | Barre fixe de bas de page : 87 px sur 844 px (10,3 %), recouvre le titre de section. `pb-[var(--bar-clearance)]` existe dans le CSS mais n'est pas appliqué au conteneur. | Barre de contexte ≤ 64 px (`.account-context-bar`), `padding-bottom` calculé sur `--context-bar-height`. | 87 px → **61 px**. Au bas de page, **0 contenu bloqué** sous la barre. |
| **S-05** | Navigation : 17 entrées à plat, `scrollWidth` 1 945 px dans 390 px, **3 visibles sur 17**, sans indice de défilement. | Tiroir groupé en 5 sections sur mobile, colonne groupée sur desktop — un seul arbre de markup. | 3/17 visibles → **18 liens, 5 groupes**, tous atteignables. |
| **S-08** | Plancher typographique à 12,5 px (`--text-caption`) et 12 px (`--text-overline`). 95 nœuds de texte sous 14,5 px sur `/account`. | Plancher à 14 px **dans le périmètre du compte** : `--text-caption .875rem`, `--text-overline .875rem`, `--text-small .9375rem`, `--text-body 1.0625rem`. | 15 / 37 / 14 / 15 nœuds < 14 px → **0** sur les quatre écrans. |
| **S-09** | `text-ardoise-300` (#8a9099) sur les séparateurs « · » : **3,22:1** sur blanc, **2,42:1** sur crème. Seul échec de contraste authentique du site. | **Changement de classe**, pas de jeton : `text-ardoise-300` → `text-ardoise-400` (#5b6068), déjà dans la palette. | 2,42:1 (échec AA) → **4,77:1 crème / 6,33:1 blanc (AA)**. |
| **C-02** | « Appelez la boutique » sans `tel:`, « la politique publiée » sans lien. Trois blocs d'action, zéro action. | Trois cartes d'action : `tel:0139471212`, lien `/cgv#annulation`, lien vers les réclamations. | 0 action cliquable → **3 cartes d'action**. |
| **C-01** | Identifiants de spécification visibles du client : « — R20 », « — R6 / R7 / R8 / R9 », « — F-01 / F-05 »… | Supprimés de l'affichage, conservés en `data-spec` sur le paragraphe. | 2 identifiants visibles sur CMD-2452 → **0** (2 conservés en attribut). |
| **O-01** | Badge « SOLDE 53.26 € DÛ » : point décimal anglo-saxon, et un solde transformé en dette. | « Solde à régler · 53,26 € », virgule française, chiffres tabulaires. | `Solde 53.26 € dû` → **`Solde à régler · 53,26 €`**. |
| **C-03** | Ouverture de `/account/deposits` en prose juridique (« article L. 214-1 »), cartes « Dû » et « Rendu ». | Phrase simple d'abord, référence dans un `<details class="legal-disclosure">`. Cartes « À régler au retrait » / « Consignes remboursées ». | Texte juridique en tête → **placé sous disclosure**. |
| **G-08** | Mention de pied de page : 4 paragraphes de texte avant l'action, sur chaque page. | Résumé d'abord, détail ensuite. | — |

### Corrections détectées en construisant les maquettes

| Constat | Correction |
|---|---|
| Le pied de page duplique la section « Aller à » de l'en-tête : deux repères portent le même nom accessible (`landmark-unique`). | La section de pied de page reçoit son propre libellé. |
| Les liens autonomes (seul enfant d'un bloc) font 170 × 18 px : sous le seuil de 44 px. | Règle scoped : `a:only-child` → `inline-flex` + `min-height: 2.75rem`. Les liens **dans une phrase** gardent leur flux inline (exception WCAG 2.5.8). |

---

## 3 · La règle de confinement

> *« L'apparence du storefront doit rester entièrement inchangée. »* — contrainte de la spécification.

1. **Aucun jeton partagé n'est redéfini.** `--text-caption` (12,5 px) apparaît 50 à 80 fois par écran : le modifier
   cascaderait sur tout le site. Il est neutralisé **dans le périmètre du compte uniquement**, via `[data-scope="account"]`.
2. **Le contraste se corrige par changement de classe**, pas par changement de palette : `text-ardoise-300` →
   `text-ardoise-400`. Les deux classes existent déjà dans `production.css`.
3. **Aucune couleur nouvelle.** Les seules valeurs utilisées sont celles de la palette de production :
   `ardoise-400 #5b6068`, `ocre-700 #7a4d0d`, `laiton-700 #6e5429`, `lin-200 #e7e0d3`.
4. **Le laiton n'était pas un problème de contraste** (6,74:1, conforme AA) mais un **problème de taille** (11 px sur
   le logotype) : il est traité par le plancher typographique.
5. **`tokens/account-scope.css` est non stratifié.** Les utilitaires Tailwind vivent dans `@layer utilities` ; une feuille
   non stratifiée les l'emporte sans jamais les modifier.
6. **La barre réutilise le jeton existant.** `--bar-clearance` (6,5 rem) existe déjà dans le CSS de production mais n'est
   pas appliqué au conteneur du compte ; la correction l'applique avec la nouvelle hauteur de barre.

**Vérification du cloisonnement.** `production.css` est identique octet pour octet avant et après (93 064 octets).
Aucune des 19 routes du compte n'est touchée hors du bloc `[data-scope="account"]`.
Les captures « avant » et « après » partagent le même chrome de maquette, construit par `chrome.py`, afin que la seule
différence visible soit la correction.

---

## 4 · Intégration

```html
<!-- 1. dans la page du compte, sur le conteneur de mise en page -->
<div data-scope="account" class="lg:grid lg:grid-cols-[236px_minmax(0,1fr)] lg:gap-10">
```

```html
<!-- 2. après la feuille de production, dans le <head> -->
<link rel="stylesheet" href="/account/account-scope.css">
```

Puis, côté DOM :

| Élément | Avant | Après |
|---|---|---|
| Second `<main>` | `<main id="contenu" class="min-w-0">` | `<div class="min-w-0" role="none">` |
| Confort de lecture | `<div class="hidden sm:block">` | `<div class="block">` |
| Bandeau d'annonce | `<p class="truncate">` | `<p class="truncate min-w-0 flex-1">` |
| Barre de bas de page | `<div class="fixed inset-x-0 bottom-0 z-40 …">` | `<div class="account-context-bar" role="region" aria-label="Actions du compte">` |
| Navigation | `<ul class="… overflow-x-auto …">` (17 `<li>`) | `<button class="account-nav-drawer-trigger">` + `<div id="account-nav-drawer" class="account-nav-drawer">` + `<ul class="account-nav-list">` (5 groupes) |
| Badge de solde | `Solde 53.26 € dû` | `Solde à régler · 53,26 €` |
| Identifiants de spec | `<span class="text-ardoise-600"> — R20</span>` | `<p … data-spec="R20">` |
| Blocages | prose seule | cartes d'action avec `tel:` et liens |

Le JavaScript du tiroir (ouverture, fermeture, `aria-expanded`, retour du focus) est dans `chrome.py` et doit être porté
en composant React (`useState` + `useEffect` + gestion du focus) en production.

---

## 5 · Vérification

`verify_final.py` rejoue tout dans Chromium et compare les mêmes fichiers avant et après.

| Mesure | Avant | Après | Source |
|---|---|---|---|
| Catégories de règles axe violées | 4 | **1** | axe-core 4.10.2 |
| `landmark-main-is-top-level` | 1 | **0** | axe |
| `landmark-no-duplicate-main` | 1 | **0** | axe |
| `landmark-unique` | 1 | **0** | axe |
| `region` | 3 | 3 | axe — **hors périmètre** (en-tête du storefront) |
| Éléments `<main>` | 2 | **1** | DOM |
| Identifiants dupliqués | `contenu` | **aucun** | DOM |
| Nœuds de texte < 14 px dans la colonne du compte | 15 / 37 / 14 / 15 | **0 / 0 / 0 / 0** | DOM |
| Barre de bas de page | 87 px | **61 px** | DOM |
| Contenu bloqué sous la barre (bas de page) | — | **0** | DOM |
| Bouton « Confort de lecture » à 390 px | 0 × 0 | **107 × 50** | DOM |
| Liens de navigation atteignables | 3 sur 17 visibles | **18 liens, 5 groupes** | DOM |
| Cibles tactiles < 24 px dans le compte | 8 | **0** | DOM |

**La règle `region` qui subsiste** porte sur trois nœuds de l'en-tête du storefront : le lien d'évitement, le bandeau
d'annonce et le lien téléphone. Les corriger modifierait l'apparence du site public, ce que la spécification interdit ;
ils restent classés **P1** dans le rapport d'audit.

---

## 6 · Limites

- **Chromium uniquement.** Safari/iOS et Firefox n'ont pas été testés (le rapport d'audit le signale aussi).
- Les pages « avant » sont des **captures du DOM rendu**, pas des pages vivantes : les scripts ont été retirés. Le
  comportement dynamique (panier, filtres, appels serveur) n'est donc pas représenté.
- Le contrôle « Confort de lecture » de la maquette est un **bouton de démonstration** : il pilote le même attribut
  `data-comfort` que le vrai contrôle, mais sans la persistance serveur.
- Les maquettes « après » illustrent les corrections **P0**. Les corrections P1 et P2 du rapport ne sont pas
  matérialisées (voir la section 5 de `index.html`).
- Le contrôle de non-régression pixel à pixel sur le storefront (N-09 / G-8) reste à mettre en place en CI : il
  n'a pas pu être exécuté ici, faute d'un serveur de rendu de référence pour le storefront.

---

*Captures du DOM de production réalisées le 28 nov. 2026 sur `maisonannois.sytes.net/account/` avec le compte de
démonstration `marie.lefevre@mail.fr`. Mesures : Chromium 156.0.8078.4, axe-core 4.10.2, 390 × 844 et 1440 × 1000.*
