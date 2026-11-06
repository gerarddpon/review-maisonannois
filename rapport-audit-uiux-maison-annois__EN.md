# UI/UX Audit — Maison Annois Customer Account Area

**Target:** `https://maisonannois.sytes.net/account/` (plus `/track`, `/compte`, and the public storefront)
**Date:** 6 November 2026
**Audience:** Frontend engineering team and product design team
**Standard applied:** WCAG 2.2 AA / RGAA 4.1.2
**Method:** 56 full-page captures (390 px and 1440 px viewports), 28 pages crawled, axe-core 4.10.2 injected on every page, computed contrast and target-size measurement, DOM inspection, authenticated walkthrough (demo account) and guest walkthrough.
**Reference spec:** `customer-account-area-spec.md` — functional gaps are flagged against it (F-xx / R-xx / UI-xx).

> **One-line verdict.** The legal and editorial work in this product is excellent — the withdrawal journey, the recall notice and the claim form are better written than most of the market. But the **mobile interface was never finished**: an unsignposted horizontal nav, a fixed bar that covers content, the reading-comfort control missing on mobile, 95 sub-14.5 px text nodes per account page, and one decorative grey below AA. That is where conversion and elderly-customer trust are being lost.

> **Note for the team.** Two headings in this report are *credit*, not criticism: §1.5 (withdrawal) and §1.6 (claims) record that the implementation is conformant. Do not "simplify" them. The defects listed inside those sections are limited to touch-target size, internal ID leakage, and the missing photo upload.

---

## 1. Expert UI/UX audit and technical findings

### 1.1 Shell and navigation (all pages)

| # | Finding | Severity | Impact |
|---|---|---|---|
| S-01 | **Duplicate `<main>` landmark.** On all 20 account pages, a shell `<main>` (h = 3262 px) contains a second `<main>` inside the grid (h = 2763 px). axe-core raises 4 violations across 40 captured viewports: `landmark-no-duplicate-main`, `landmark-main-is-top-level`, `landmark-unique`, `region`. | **High** | Landmark navigation (screen-reader landmark list / D5 shortcut) is broken — the customer cannot jump to main content. ARIA 1.2 and WCAG 2.4.1 failure. |
| S-02 | **Fixed bottom bar "Appeler / Panier"**: `fixed inset-x-0 bottom-0 z-40`, 87 px tall on an 844 px viewport → **10.3 % of the mobile viewport permanently consumed**. Measured occlusion: the `<h2>` "Commande CMD-2452" (y = 737) and its meta paragraph (y = 768) sit behind the bar at first paint. | **Medium** | A section heading is sliced in half on page load. On every page, whatever content lands at the bottom of the viewport is unreadable without scrolling. The bar carries a cart CTA that has little value for someone already in their account. |
| S-03 | **Announcement bar truncated on mobile.** The `<p class="truncate">` cuts "Livraison frigorifique Chronofresh 24/48 h · offerte dès 99 €" down to "… · of…". The phone number and the reading-comfort control are pushed off-screen. | **Medium** | The free-delivery threshold — a primary conversion message — becomes unreadable on the main channel. |
| S-04 | **"Confort de lecture" is absent on mobile.** The control exists (145 × 44 px, visible at 1440 px) but is `hidden` below 1024 px; the corresponding `<span>` exists in the DOM yet reports `is_visible() === false` at 390 px. | **High** | The platform's own low-vision accommodation is **unavailable on the mobile-first device**, i.e. removed from the most fragile segment. |
| S-05 | **Account navigation: 17 items in a 1945 px scroll strip.** Measured `scrollWidth 1945 / clientWidth 390` — 3 of 17 visible, with no fade, no edge shadow and no "drag me" affordance. | **High** | 14 destinations (Factures, Paiements, Arrhes & consignes, Réclamations, Sécurité produit, Préférences, Atelier, Cagnotte, Avis, Professionnel, Notifications, Adresses, Compte & sécurité, Vie privée, Favoris) are **invisible and undiscoverable** without already knowing the gesture. High abandonment risk. |
| S-06 | **Category chips clipped.** Measured `scrollWidth 444 / clientWidth 390`; "Tous les rayons →" is cut at the viewport edge with no affordance. | **Medium** | The link to the full catalogue — the highest-value link in the header — is unrecognisable. |
| S-07 | **Small tap targets.** Phone link 22 × 44 px; logo link 105 × 24 px; category links 32 px high; the fulfilment-mode control collapses to a bare 🏪 emoji at 38 × 44 px. | **Medium** | The only control for choosing pickup vs delivery is an emoji whose rendering varies by OS, at a 38 px target. |
| S-08 | **Micro-type — the real type problem.** On the account overview: 71 elements at 14 px, 23 at 12.5 px, 6 at 13 px, 3 at 12 px, 1 at 11 px; **95 text nodes under 14.5 px** on that single page. `--text-caption` (12.5 px) carries the order reference, the badge, the footer legal text *and* the leaked spec ID. | **High** | Below the comfortable reading size for a presbyopic customer — and 12.5 px is the exact size carrying every legal notice (non-withdrawal reasons, retention periods). |
| S-09 | **Contrast below WCAG AA — narrower than first measured.** Re-verified against browser-resolved colours (canvas sRGB) rather than string-parsed values: every failure comes from **one colour only**, `text-ardoise-300` (`#8a9099`), and only on separator glyphs and small metadata spans — **3.22:1** on white at 12.5 px, **2.85:1** on the sunken surface, **2.42:1** on the cream card at 14 px. All body, legal and metadata copy passes comfortably (`text-ardoise-500` 8.12:1, `text-ardoise-700` 13.11:1, `text-ardoise-900` 17.67:1), as do the laiton, ocre and footer instances (6.42–14.15:1). | **Low** | The failure is confined to decorative separators, so the legal text is legible — the earlier "High" was an artefact of `oklab()` values being mis-parsed. Fix is a class swap to `text-ardoise-400` (`#5b6068` → 6.33 / 5.62 / 4.77:1), which changes no shared token and leaves the storefront untouched. |
| S-10 | **20 × 20 px checkboxes** across 21 controls (17 allergens on `/account/preferences`, 2 on `/account/addresses`, 2 on `/account/butchery`, plus the per-line checkboxes in the withdrawal flow). The adjacent label is clickable, which is why axe raises no violation, but the visual box is under the 24 × 24 px minimum of SC 2.5.8. | **Medium** | A tiny target for an arthritic or shaky finger; misses produce a false "I think I ticked the wrong box". |
| S-11 | **Focus ring invisible on "Panier, vide".** Computed `outline: 2px solid rgb(251, 249, 245)` — the button's own text colour, applied outside the button against a cream page. Net result: a near-white ring on a cream background. | **Medium** | Keyboard focus is lost on one of the most-used controls. |
| S-12 | **Notification table wider than its container.** Table 337 px inside a 304 px wrapper with `overflow-x: visible` → 33 px of overflow into the gutter. | **Medium** | Visible bleed on mobile while the rest of the page stays inside 390 px. |
| S-13 | **Internal specification IDs exposed to customers**: "— R20", "— R6 / R7 / R8 / R9", "— R1 / R2 / R3 — Art. L. 221-18…", "— F-12b", "— F-14", "— R21 — art. R. 423-3 C. conso.", "— F-10 / R18 / R19", "— C-10 / G1–G2". | **Medium** | An engineering annotation leaked into production. Meaningless to the customer, reads as an unfinished draft, and inadvertently exposes the internal legal-reasoning trail. |
| S-14 | **Footer: `bonjour@maison-annois.fr` is welded to "Espace professionnel →".** No separator between the email address and the following link. | **Medium** | The customer cannot tell where the email ends and the link begins — ambiguous click target. |
| S-15 | **Inconsistent store naming**: "Maison Annois", "Magasin Annois", "Boutique de Sannois", "Maison Annois — Sannois". | **Medium** | A customer looking for "Sannois" reads "Magasin Annois". Physical wayfinding is effectively lost. |
| S-16 | **Editorial preamble of 3–5 lines before any actionable content**, on every page ("Votre maison, en un coup d'œil", "Chaque commande garde son détail…", "Vous pouvez tout voir, tout exporter…"). | **Medium** | On mobile, two to three screens of reading before the first interaction. Pure cognitive tax. |
| S-17 | **Two competing navigation systems.** The 17-item tab strip plus a 9-card "Aller à" section on the overview. | **Medium** | Two ways to reach the same list; drift risk and redundancy. |

### 1.2 Account overview (`/account`)

| # | Finding | Severity | Impact |
|---|---|---|---|
| O-01 | **Wrong decimal separator.** The badge renders "SOLDE **53.26** € DÛ" (full stop) while the same page renders "53,26 €" (comma) and the entire site uses the comma. | **Medium** | A visible French typographic inconsistency — reads as a quality defect on a premium food site. |
| O-02 | **"Dû" framing.** The Arrhes & consignes card opens with "Dû — 144,61 € · 3 commande(s) avec solde". This balance is not a debt: it is settled at pickup after weighing. | **Medium** | Manufactured anxiety on an order that is already part-paid. The customer goes looking for an explanation. |
| O-03 | **The "À régler" card lists three identical lines** ("Solde à régler au retrait / Commande CMD-XXXX") with no date, no store and no urgency ordering. | **High** | Three indistinguishable rows — the customer cannot tell which one to act on. The card fails at its only job. |
| O-04 | **The "Vos documents" card mixes three unrelated metrics** — "Factures disponibles 3", "Arrhes versées 129,39 €", "Réclamations ouvertes 0". | **Low** | Mixed units and natures; no mental total forms. |
| O-05 | **No purchase action anywhere in the account.** No "Commander à nouveau", no "Reprendre une commande". The only action is "Ouvrir la commande". | **High** | The customer who is ready to rebuy — the highest-value e-commerce segment — exits via "Retour à la boutique". The catalogue loses the reorder. |
| O-06 | **No pickup anchor above the fold.** The next pickup is inside the "Prochaine étape" card, but the date and store appear only at the bottom of the order-detail page. | **High** | The customer scrolls two screens to learn *where* and *when* to come. |
| O-07 | **8 px timeline dots**, weakly marked current state. | **Low** | Progress is not readable at a glance. |

### 1.3 Order detail (`/account/orders/[no]`)

| # | Finding | Severity | Impact |
|---|---|---|---|
| C-01 | **Amount due, pickup date and pickup location are below the fold.** The opening screen reads "Confirmée — La commande est enregistrée pour votre créneau" without saying when or where. "Régler le solde de 53,26 €" and "sam. 31 oct. · 10h00 – 10h30" arrive further down. | **High** | The customer's first question ("when and where?") is unanswered above the fold. |
| C-02 | **Blocked states are prose with no action.** "Le délai de modification est passé… Appelez la boutique" — no `tel:` link, no button, no affordance. "l'annulation suit la politique publiée" — "politique publiée" is not a link. | **High** | The customer receives an explanation but no way to act. On mobile they must write the phone number down. |
| C-03 | **Legal copy repeated.** The non-withdrawal reason is repeated per line, then again in the "Rétractation" block, and "La garantie de conformité de deux ans reste ouverte" appears **twice** within the actions block. | **Medium** | Screen-reader noise (the text is announced three times) and visual fatigue. |
| C-04 | **"2 ARTICLE(S)"** — naive pluralisation inside a pill. | **Low** | Reads as machine-generated. |
| C-05 | **"Vous êtes reconnu par votre compte"** — technical phrasing. | **Low** | Not understood. |

### 1.4 Order list (`/account/orders`)

| # | Finding | Severity | Impact |
|---|---|---|---|
| L-01 | **No filters, no search, no sort.** The page contains **zero** `input`, `select` or filter `button` elements. Spec F-02 requires filters (period, status, fulfilment type, store), search (order number, product) and sort. | **High** | As soon as the history exceeds a handful of orders, nothing can be found. The self-service archive feature does not exist. |
| L-02 | **Ambiguous card anatomy.** A large amount with no label ("76,26 €"), then the malformed "Solde du 53,59 €", then a date. No ordering or priority between orders. | **Medium** | The customer reads a number without knowing whether it is paid, due or estimated. |
| L-03 | **"Reprendre dans le panier" is absent on in-progress orders** (present only on delivered/collected ones). | **Medium** | The reorder path is only offered after the fact. |

### 1.5 Withdrawal (`/account/orders/[no]/withdraw`) — *the best screen in the product*

| # | Finding | Severity | Impact |
|---|---|---|---|
| R-01 | **20 × 20 px checkboxes** for line selection (see S-10). | **Medium** | Same defect, here on the most legally sensitive path in the product. |
| R-02 | **Internal IDs** "— R1 / R2 / R3 — Art. L. 221-18 et suivants C. conso.". | **Medium** | See S-13. |
| R-03 | **Breadcrumb "Mon espace / Suivre une commande"** — mixes an authenticated area with a guest journey. | **Low** | The customer wonders whether they are logged in or anonymously tracking. |

> **Credit where due.** This screen gets the job right: per-line eligibility with the statutory reason, refundable amount separated from excluded amount, the explicit note that excluded items "restent votre propriété", the consequences disclosed **before** the click ("Les conséquences, dites avant le clic et non après"), a computed refund deadline ("au plus tard le vendredi 20 novembre 2026"), outbound delivery costs included (Art. 13(2)), seller withholding right (Art. 13(3)), customer-borne return costs (Art. 14(1)), a live countdown ("Il reste 11 jour(s)") and a distinct confirmation step. **Conformant with Art. 11a and spec R1–R3.** The only outstanding item is guest access to the function, to be confirmed on the `/track` journey (see 1.9).

### 1.6 Claims (`/account/orders/[no]/claim`) — *conformant, one gap*

| # | Finding | Severity | Impact |
|---|---|---|---|
| P-01 | **No photo upload.** The form contains only `select` (article), `select` (reason), `select` (remedy), `textarea` (message). Spec F-11b requires up to 5 photos (10 MB each, metadata stripped). | **Medium** | For a freshness defect or a transport damage, **the photo is the evidence**. Its absence turns an easy claim into a non-actionable report. |
| P-02 | **Round trip required.** `/account/support` shows "Aucune réclamation — Vous pouvez en ouvrir une depuis le détail d'une commande remise" plus a "Voir mes commandes" button: the customer must locate the right order, then reopen the detail page. | **Medium** | Three jumps for the single most important post-delivery action. |
| P-03 | *Credit:* "Deux délais, deux usages" — a 3-day quality window **and** the 2-year conformity guarantee with exact dates, explicitly never shortened (Art. L. 217-12). Complete reason and remedy sets, 2-working-day response committed. **Conformant with R19 and F-11b.** |

### 1.7 Notifications (`/account/notifications`)

| # | Finding | Severity | Impact |
|---|---|---|---|
| N-01 | **Table overflows its wrapper** (see S-12). | **Medium** | Bleeds into the gutter on mobile. |
| N-02 | **"Désactivé — activer" toggle.** The label conflates current state and the action it triggers. | **Medium** | Ambiguity on a control that manipulates a consent. |
| N-03 | **Internal ID** "— F-12b". | **Medium** | See S-13. |
| N-04 | *Credit:* 12 real rows, each describing the message genuinely sent; mandatory messages are flagged and explained; SMS double opt-in spelled out. **Conformant with F-12a / F-12b.** |

### 1.8 Settings, preferences, privacy, deposits, product safety, support

| # | Page | Finding | Severity |
|---|---|---|---|
| G-01 | Settings | **"COMPTE LOCAL (MOT DE PASSE)"** — implementation jargon for "password account". | **Low** |
| G-02 | Settings | **Connected devices: two identical "Ordinateur · Chrome" rows.** No OS, no country, no IP: the customer cannot tell their own session from someone else's — i.e. cannot spot a fraudulent login. | **Medium** |
| G-03 | Settings | **Internal ID** "— F-14". | **Medium** |
| G-04 | Privacy | **Typing "CONFIRMER"** to confirm account erasure. No `aria-describedby`, `autocomplete="off"`, no case guidance → failure risk (and a failed confirmation reads as a server error). | **Medium** |
| G-05 | Privacy | **Retention table: values right-aligned and wrapping onto two lines**, with no legal basis. Spec F-07 requires "sa date et sa base légale". | **Medium** |
| G-06 | Privacy | Two distinct controls share `name="note"` (a text input and a textarea) across two different forms → collision risk on submit. | **Low** |
| G-07 | Preferences | 17 allergen checkboxes in a single column, 20 × 20 px, each with a small grey description. | **Medium** |
| G-08 | Deposits | **The opening paragraph is pure legal prose**: "Le versement d'avance n'est pas une avance comme les autres : sa nature juridique décide de ce qui se passe en cas de renoncement." This is the first sentence a 75-year-old reads. | **High** |
| G-09 | Deposits | **"Dû" / "Rendu" headline cards** with large figures — the same anxious framing as O-02. | **Medium** |
| G-10 | Product safety | **Internal ID** "— R21 — art. R. 423-3 C. conso.". | **Medium** |
| G-11 | Support | **Internal ID** "— F-10 / R18 / R19". | **Medium** |
| G-12 | Support + footer | **Incomplete consumer-mediator block.** The footer carries only "Médiateur : CM2C". Art. R. 616-1 requires postal *and* electronic contact details, the mediator's website, the languages accepted and the types of dispute covered; Art. L. 616-1 requires the information to be repeated once a complaint addressed to the trader has not resolved the dispute. `/account/support` cites Art. L. 612-1, but the footer — the most-read surface — stays incomplete. | **Medium (compliance)** |
| G-13 | Support | *Credit:* free mediation announced, SignalConso and the competent court cited, "Aucune de ces démarches ne dépend de notre accord", 2-working-day response committed. **Good practice.** |

### 1.9 Guest area and public storefront

| # | Page | Finding | Severity |
|---|---|---|---|
| U-01 | `/track` | **Placeholder "Format CMD-0000."** — an invalid example order number; actively misleading. | **Low** |
| U-02 | `/track` | **Internal design rationale exposed to customers**: "Un message d'erreur ne dit jamais si la commande existe…" followed by "— C-10 / G1–G2". Engineering notes in a public interface. | **Medium** |
| U-03 | `/track` | **The "Deux niveaux d'accès" explainer sits below the form**, after a 3-line introduction. The promise "le détail — contenu, lots, factures, réclamation, **rétractation**" has no visible counterpart: the customer must enter the 6-digit code and then hunt for the action. | **Medium** |
| U-04 | `/boutique` | **238 tap targets under 44 px** measured on the mobile catalogue page alone — category links, chips, secondary links. | **Medium** |
| U-05 | `/panier` | **Heading-order violation** (axe `heading-order`): an `h3` follows an `h1` with no intervening `h2`. | **Medium** |
| U-06 | `/` | *Credit:* clear hero, reassurance strip (weighing, cut-to-order, cold chain, chosen farmers), explicit €/kg pricing. **The best work in the storefront.** |

### 1.10 The structural problem: two competing customer areas

`/compte` (legacy, unprotected) and `/account` (new) coexist. The legacy is **richer** on several points:

| Capability | `/compte` (legacy) | `/account` (new) |
|---|---|---|
| **Pickup pass QR code** | ✅ "Voir le QR code de retrait →" | ❌ **Absent** (F-05 / UI-06) |
| "Composer une commande" | ✅ 2 occurrences | ❌ Absent |
| "Client de confiance" loyalty status | ✅ (spend, allergies, seasonal e-mails) | ❌ Absent |
| "Call the counter" reassurance block | ✅ | ❌ Absent |
| Count badges on tabs ("Mes commandes **2**") | ✅ | ❌ Absent |
| Reorder | ✅ "Reprendre dans le panier" | ⚠️ only on delivered orders |

**Severity: High.** This is a split mental model: a customer who knows the old area cannot find their landmarks, and the new one is poorer on the highest-value behaviours. The pickup pass is the most critical gap — **without it, collecting in store depends on memory or a phone call**, in a multi-store butcher where collection is the default fulfilment method.

---

## 2. End-user friction points

### 2.1 The standard customer

1. **"I cannot find my documents."** 17 destinations in a 1945 px horizontal strip; 3 visible. The "Aller à" card grid on the overview is the only escape route, and it sits at the bottom of the page — unreachable from the top.
2. **"I do not know how much I owe or when."** The overview shows "SOLDE 53.26 € DÛ" — a wrong decimal separator *and* debt framing. The order detail hides date and location two screens down.
3. **"I am blocked with no way forward."** "Appelez la boutique" with no clickable number; "la politique publiée" with no link; "ouvrez une réclamation" with no destination on an order not yet handed over.
4. **"I cannot search my own history."** No search field on the order list.
5. **"I cannot reorder."** No "order again" action anywhere in the account.
6. **"I read the same thing three times."** The non-withdrawal reason and the conformity guarantee each repeat.
7. **"I do not understand what 'Dû 144,61 €' means."** The word "Dû" converts an order into a debt.
8. **"I cannot find my invoices."** A "3" on a card, a link inside an order, and an invisible tab. The spec calls for a dedicated document centre.
9. **"I cannot complain directly."** `/account/support` bounces the customer to the order list: three jumps to open a case.

### 2.2 Elderly customers — specific barriers

| Barrier | Measured evidence | Consequence |
|---|---|---|
| **Reading-comfort mode does not exist on mobile** | Control is `hidden` below 1024 px | The only software answer to visual fatigue is withdrawn from the most exposed segment |
| **11–12.5 px type** | 30 elements ≤ 12.5 px on the overview; entire legal notices at 12.5 px | The legal text — the text that binds — is the least legible |
| **One grey below AA (2.42–3.22:1)** | `text-ardoise-300` on white, sunken and cream surfaces | Confined to separator glyphs and small metadata; the legal text itself reads at 13.1:1 |
| **20 × 20 px checkboxes** | 21 controls | Missed taps, accidental double-taps, frustration |
| **22–38 px targets** | Phone, logo, category chips, fulfilment-mode button | Targets too fine for a tremor |
| **Invisible navigation** | 14 destinations off-screen with no scroll cue | The customer concludes the feature does not exist |
| **Legal prose as the opening line** | Deposits, withdrawal, privacy pages | Reading abandoned; reads as a scam |
| **Contradictory naming** | "Magasin Annois" vs "Boutique de Sannois" | The customer does not know which door to walk into |
| **Invisible focus ring** | Cart button | Keyboard navigation broken on the primary control |
| **Typing "CONFIRMER"** | Literal, case-sensitive entry | Account deletion fails; the error is read as a server bug |
| **No large-text control** | No font-size setting in the account area | Reading-comfort mode does not cover typography |

> **The decisive point.** The shop did the hard work — traceability, temperatures, lot numbers, mediation and deposits are explained with precision and without unnecessary jargon. But **all of that quality is written in 12.5 px grey at 3.2:1**. The elderly customer will not see it. This is a design problem, not a content problem.

---

## 3. Actionable correction strategy

### 3.1 Prioritised roadmap

#### P0 — Blocking (2 to 3 weeks)

| # | Action | Ref | Definition of done |
|---|---|---|---|
| 1 | **Remove the nested `<main>`.** One `main` per page; the account grid becomes `<div>` or `<section aria-labelledby>`. | S-01 | axe: 0 `landmark-*` and 0 `region` violations across all 20 pages |
| 2 | **Enable "Confort de lecture" on mobile.** A 44 × 44 px control in the mobile header; the mode raises body text to ≥ 18 px, metadata to ≥ 15 px and enforces the corrected palette. Persist via `localStorage`. | S-04 | Control reachable and functional at 390 px; body computed size ≥ 18 px in comfort mode |
| 3 | **Raise the type floor.** New scale: `text-micro` 14 px (replacing 12.5), `text-caption` 15 px, `text-small` 16 px, body 17 px, `text-body-lg` 18 px. No meaningful text below 14 px. | S-08 | 0 elements under 14 px that are not decorative |
| 4 | **Fix contrast — class swap, not token edit.** Replace the 10 offending `text-ardoise-300` occurrences with `text-ardoise-400` (`#5b6068`): 6.33:1 on white, 5.62:1 on sunken, 4.77:1 on cream. **Do not modify `--color-ardoise-300`** — it is shared with the storefront. No other colour fails. | S-09 | 0 contrast failures under axe; 0 `text-ardoise-300` on a text node in the account area |
| 5 | **Neutralise the fixed bar.** Replace "Appeler / Panier" with a **context bar that varies by page** (overview: balance + next pickup; order detail: "Régler le solde"), height ≤ 64 px, plus `padding-bottom: calc(64px + env(safe-area-inset-bottom))` on the content, and a real `tel:` action. | S-02 | 0 elements occluded at first paint across all 20 pages |
| 6 | **Rebuild the navigation.** Mobile: a "Menu" button opening a drawer grouped into 4 sections (Order / Money / Preferences / Account). Desktop: keep the column but **grouped with section headings**. Remove the "Aller à" card grid. | S-05, S-17 | Every destination reachable in one interaction, with no horizontal gesture |
| 7 | **Strip specification IDs from customer copy.** Keep them as `data-spec="R20"` for QA. | S-13 | 0 occurrences of `— R\d`, `— F-\d`, `C-10`, `G1–G2` in the rendered DOM |
| 8 | **Fix the "DÛ" badge.** "Solde à régler — 53,26 €" (comma, via `Intl.NumberFormat('fr-FR')`), and rename "Dû / Rendu" to "À régler au retrait / Consignes remboursées". | O-01, O-02, G-09 | No full stop in any rendered amount |

#### P1 — High (3 to 5 weeks)

| # | Action | Ref |
|---|---|---|
| 9 | **Filters, search and sort on `/account/orders`.** Status chips (En cours / Terminées), period selector, search on order number + product, sort by date. On mobile: one "Filtrer" button opening a sheet, plus a persistent search field. | L-01 |
| 10 | **Turn blocked states into actions.** Every blocked state becomes an **action card**: title, short explanation, and a button (`Call 01 39 47 12 12`, `Read the cancellation policy`, `Open a claim`). No dead text. | C-02 |
| 11 | **Restructure the top of the order detail.** A "Collection" block at the top: `Retrait · sam. 31 oct. · 10h00–10h30 · Boutique de Sannois` + amount + "Régler le solde de 53,26 €". | C-01, O-06 |
| 12 | **Add the pickup pass.** QR code + 6-digit code, on `/account/orders/[no]` and on the overview — matching the legacy area. | 1.10, F-05 |
| 13 | **Add "Commander à nouveau"** from the account (history, the "À régler" card, and the overview), surfacing price deltas. | O-05, F-15 |
| 14 | **De-duplicate the legal notices.** One occurrence per order of the non-withdrawal reason and the conformity guarantee, inside a collapsible "What the law allows and forbids" panel. | C-03 |
| 15 | **Make claims reachable in one step.** Add "Déposer une réclamation" on `/account/support` opening an order-independent form (article + lot) for customers who cannot locate their order. | P-02 |
| 16 | **Add photo upload to the claim form.** Drop zone for 5 × 10 MB, metadata stripped, pre-upload preview, client-side compression. | P-01, F-11b |
| 17 | **Tap targets.** Checkboxes 24 × 24 px visual with a 44 × 44 px clickable label; header links ≥ 44 px; the fulfilment-mode control 44 × 44 with a visible label instead of a bare emoji. | S-07, S-10 |
| 18 | **One visible focus ring everywhere.** Token `--focus-ring: 2px solid #9B2226` + `outline-offset: 2px` + a double halo `box-shadow: 0 0 0 4px rgba(255,255,255,.9)` so it works on light *and* dark surfaces. | S-11 |
| 19 | **One naming vocabulary.** Use "Boutique de Sannois", "Maison Annois — Sannois", "Retrait à Sannois" consistently. No concurrent designations. | S-15 |
| 20 | **Fix the footer.** Non-breaking space before "Espace professionnel", and a complete mediator block (postal + electronic contact, website, languages, dispute types) on every page rather than a name only. | S-14, G-12 |
| 21 | **The footer must carry reassurance for elderly customers**: a clickable phone number, opening hours, "who to call". | 2.2 |

#### P2 — Comfort (5 to 7 weeks)

| # | Action | Ref |
|---|---|---|
| 22 | **Remove the editorial preambles**, or cut them to one line. The page title is enough; explanatory copy moves to the footer or into a contextual help disclosure. | S-16 |
| 23 | **Rebuild the notifications table** as stacked cards on mobile (message type + e-mail state + SMS state + action), table only from 768 px up. | N-01, N-02 |
| 24 | **Separate state from action** in the toggles: state as text ("Désactivé") and the action as a distinct button ("Activer"). | N-02 |
| 25 | **Enrich connected devices** with OS, browser, approximate city, session creation date, and a "Sign out this session" action. | G-02 |
| 26 | **Erasure confirmation**: replace typing "CONFIRMER" with an explicit "I confirm I want to delete my account" checkbox, preceded by a plain summary of consequences (30-day delay, 10-year retention of some records) and a native confirm dialog. | G-04 |
| 27 | **Retention periods** as a list (duration + legal basis + consequence) rather than a table with wrapped right-aligned values. | G-05 |
| 28 | **Legal copy: short version + long version.** One plain sentence by default ("You paid a 23 € deposit. If you cancel, it is refunded to you, unless the shop has started preparing, in which case the 23 € is kept."), with the legal reference inside a collapsible panel. | G-08, C-03 |
| 29 | **Fix the placeholder** "Format CMD-0000." → "ex. CMD-2452". Remove the exposed design rationale from `/track`. | U-01, U-02 |
| 30 | **Tables**: fix heading order on `/panier` and audit `h1 → h2 → h3` globally. | U-05 |
| 31 | **Merge the two customer areas** — absorb `/compte` into `/account` (or vice versa) before adding scope. One mental model. | 1.10 |
| 32 | **Guest tracking screen**: move the "Deux niveaux d'accès" block above the form, and surface a "Withdraw" action in the detail tier. | U-03 |

### 3.2 Recommended UI patterns

| Current defect | Replacement pattern |
|---|---|
| Invisible horizontal navigation | **Grouped navigation drawer** (mobile) / **grouped column with section headings** (desktop). Current item marked with a left rule + `aria-current="page"`. |
| Dead text "Appelez la boutique" | **Action card**: icon + label + consequence + button. Model: *What you can do now.* |
| Repeated legal reasons | **Collapsible "Your rights" panel**: one plain sentence on the surface, the exact legal reference inside `<details>`. |
| "DÙ" badge | **Balance gauge**: amount + explicit label + due date. Never a bare adverb. |
| 20 px checkboxes | 24 px box + 44 px clickable label, with a high-contrast checked state (2 px border + thick tick). |
| Notifications table | **Card list** (mobile) / table with `<caption>`, `scope="col"` and `scope="row"` (desktop). |
| Amount with no label | Systematic **label/value pair**: label left in `text-small`, value right in `font-semibold`, `tabular-nums` alignment. |
| Link to a policy | A **real link** to `/cgv#annulation`, not the phrase "la politique publiée". |
| 12.5 px grey text | **Token scale**: `--fs-micro: 14px`, `--fs-caption: 15px`, `--fs-small: 16px`, `--fs-body: 17px`, `--fs-lead: 19px`. Colours: `--text-muted` at ≥ 4.5:1, `--text-subtle` reserved for borders. |
| Editorial preamble | **Title + primary action**, with the explanation in a `<details>` or contextual help. |
| Machine pluralisation ("ARTICLE(S)") | A pluralisation helper or an explicit label ("2 articles" / "1 article"). |
| Internal spec IDs in copy | Move to `data-spec` attributes, exposed to QA only. |

### 3.3 Design tokens to introduce or correct

```css
/* Typography — raised floor, ACCOUNT SCOPE ONLY (see §1.1 / H3).
   Production: --text-caption .78125rem (12.5px), --text-overline .75rem (12px),
   --text-small .875rem (14px), --text-body 1rem (16px). */
--text-caption: 0.875rem;   /* 14px — was 12.5px, new floor */
--text-overline: 0.8125rem; /* 13px — was 12px */
--text-small:   0.9375rem;  /* 15px — was 14px */
--text-body:    1.0625rem;  /* 17px — was 16px */
--text-lead:    1.1875rem;  /* 19px — unchanged */

/* Colour — scoped overrides, NOT global token edits.
   Production already provides ardoise-400 (#5b6068); the fix is to USE it.
   --color-ardoise-300 (#8a9099) stays untouched: it is shared with the storefront. */
--text-primary:  var(--color-ardoise-900);   /* #121316 — unchanged */
--text-muted:    var(--color-ardoise-400);   /* #5b6068 — 6.33:1 white, 4.77:1 cream */
--text-on-cream: var(--color-ardoise-500);   /* #4b5058 — 8.12:1 on zone-150 */
--text-accent:   var(--color-laiton-700);    /* #6e5429 — already 6.74:1, keep as-is */
--border-subtle: var(--color-lin-200);       /* #e7e0d3 — unchanged */

/* Targets */
--tap-min: 44px;           /* WCAG 2.2 / senior usage */
--checkbox-size: 24px;     /* SC 2.5.8 — was 20px */

/* Focus — legible on every surface */
--focus-ring:   2px solid #9B2226;
--focus-offset: 2px;
--focus-halo:   0 0 0 4px rgba(255,255,255,.92);

/* Navigation */
--nav-mobile: grouped drawer (replaces the 1945px strip);
--nav-mobile-safe: env(safe-area-inset-bottom);

/* Context bar */
--context-bar-height: 64px;                              /* was 87px */
--content-safe-bottom: calc(64px + env(safe-area-inset-bottom));
```

### 3.4 What must not be broken

The **legal and editorial substance is the strongest part of this product.** When fixing presentation, preserve word for word:

- the withdrawal journey (`/withdraw`) and its distinct confirmation step;
- the recall notice (`/account/safety`): reason, "Conduite à tenir", RappelConso reference, date the authority was informed, refund without proof of purchase, guest visibility;
- the "Deux délais, deux usages" framing on claims (3-day quality window vs 2-year conformity guarantee);
- the consumer-mediation transparency;
- the deposit (arrhes) vs container-deposit distinction and the refund of the deposit outside VAT;
- the lot / origin / cut date / rearing and slaughter country / establishment trace.

Every recommendation above is a **surface, hierarchy and navigation correction** — not a rewrite of the discourse. The discourse is already right; its legibility is what fails.

---

## Annex — Method and reproducibility

- **Tooling:** Playwright with Chromium 156 headless; 56 full-page captures (390 × 844 and 1440 × 1000); axe-core 4.10.2 injected on every page; contrast and target size measured via `getComputedStyle` and `getBoundingClientRect`.
- **Pages audited:** 19 authenticated account routes, plus `/track`, `/compte`, `/panier`, `/`, `/boutique`, `/boutique/boeuf`, `/livraison-retrait`, `/allergenes-origines`, `/faq`, `/mentions-legales`, `/cgv` — at both viewports.
- **axe violations recorded:** 4 across the 40 account captures (landmark), 1 on `/panier` (heading-order), 1 on the public pages.
- **Evidence artefacts:** `/home/user/audit/audit_raw.json` (raw metrics), `/home/user/audit/shots/` (56 captures), `/home/user/audit/crops/` (52 readable slices), `/home/user/audit/txt/` (per-page text).
- **Limits of this audit.** Chromium rendering only — Safari on iOS and Firefox were not tested. Test both before closing P0, in particular `env(safe-area-inset-bottom)` and the emoji rendering of the fulfilment-mode control. The guest journey with the 6-digit code was not executed end to end, so U-03 and the guest entry point to the withdrawal function remain to be confirmed.
- **Findings that were checked and found conformant**, recorded so they are not re-opened: the withdrawal journey and its Art. 11a steps (R1–R3), the recall notice and its RappelConso record (R21), the claim form structure and its two-window framing (R19), the notification matrix (F-12a/F-12b), the allergen coverage (17 items, above the 14 EU allergens), the session and password handling (F-03/F-14) and the trace data model (F-06).

---

*French version of this report: `rapport-audit-uiux-maison-annois__FR.md` — identical finding IDs, measurements and recommendations.*
