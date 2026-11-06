# Audit UI/UX — Espace client Maison Annois

**Cible :** `https://maisonannois.sytes.net/account/` (+ `/track`, `/compte`, boutique publique)
**Date :** 6 novembre 2026 — **Auteur :** audit UI/UX & accessibilité (RGAA / WCAG 2.2 AA)
**Méthode :** 56 captures pleine page (390 px et 1440 px), 28 pages crawlées, axe-core 4.10.2, mesures de contraste et de cibles calculées, inspection DOM, parcours authentifié (compte de démonstration) et non authentifié.
**Périmètre :** l'espace client tel qu'il est aujourd'hui. Les écarts fonctionnels sont signalés par rapport au référentiel `customer-account-area-spec.md` (F-xx / R-xx / UI-xx).

> **Verdict en une ligne.** Le produit est juridiquement très solide — le parcours de rétractation, l'avis de rappel et le formulaire de réclamation sont conformes et mieux écrits que la plupart du marché — mais l'**interface mobile** n'a pas été terminée : navigation horizontale non signalée, barre fixe qui recouvre le contenu, aide à la lecture absente du mobile, 95 nœuds de texte sous 14,5 px par page et un seul gris décoratif sous AA. C'est là que se joue la conversion et la confiance des clients âgés.

---

## 1. Audit UI/UX expert et critiques techniques

### 1.1 Coquille et navigation (toutes pages)

| # | Constat | Gravité | Impact |
|---|---|---|---|
| S-01 | **Double landmark `<main>`.** Sur les 20 pages de l'espace client, un `<main>` de shell (h 3262 px) en contient un second dans la grille (h 2763 px). axe-core remonte 4 violations sur 40 pages capturées : `landmark-no-duplicate-main`, `landmark-main-is-top-level`, `landmark-unique`, `region`. | **Haute** | Navigation par landmark (raccourci D5 / liste des points de repère) cassée : le client ne peut pas sauter au contenu principal. Échec ARIA 1.2 et WCAG 2.4.1. |
| S-02 | **Barre fixe basse « Appeler / Panier »** : `fixed inset-x-0 bottom-0 z-40`, 87 px de haut sur un viewport de 844 px → **10,3 % de l'écran mobile consommé en permanence**. Elle recouvre le bas du viewport : mesuré, le `<h2>` « Commande CMD-2452 » (y = 737) et son paragraphe (y = 768) sont masqués au chargement. | **Moyenne** | Un titre de section est coupé en deux à l'ouverture. Sur chaque page, le contenu qui arrive en bas de l'écran est illisible sans défilement. La barre n'apporte qu'un « Panier » — peu utile pour quelqu'un qui consulte ses commandes. |
| S-03 | **Bandeau d'annonce tronqué sur mobile.** Le `<p class="truncate">` coupe « Livraison frigorifique Chronofresh 24/48 h · offerte dès 99 € » en « … · of… ». Le téléphone et le contrôle de confort de lecture sont expulsés hors écran. | **Moyenne** | La promo de livraison — argument de conversion — devient illisible sur le canal principal. |
| S-04 | **« Confort de lecture » absent du mobile.** Le bouton existe (145 × 44 px, visible sur desktop) mais est `hidden` sous 1024 px ; l'élément `<span>` correspondant est dans le DOM mais `is_visible() === false` à 390 px. | **Haute** | La fonctionnalité d'accessibilité conçue pour les clients âgés et malvoyants est **indisponible sur l'appareil mobile-first**. Le segment le plus fragile en est privé. |
| S-05 | **Navigation de l'espace client : 17 entrées dans une bande de 1 945 px.** `scrollWidth 1945 / clientWidth 390` — 3 items visibles sur 17, sans fondu, sans ombre de bord, sans indication « faites glisser ». | **Haute** | 14 rubriques (Factures, Paiements, Arrhes, Réclamations, Sécurité produit, Préférences, Atelier, Cagnotte, Avis, Professionnel, Notifications, Adresses, Compte, Vie privée, Favoris) sont **invisibles et inatteignables sans découvrir le mécanisme**. Effort de découverte élevé, abandon probable. |
| S-06 | **Puces de rayons coupées** : `scrollWidth 444 / clientWidth 390`, « Tous les rayons → » tronqué au bord, sans affordance. | **Moyenne** | Le lien vers tout le catalogue — action la plus rentable du bandeau — est méconnaissable. |
| S-07 | **Cibles tactiles réduites** : lien téléphone 22 × 44, logo 105 × 24, liens de rayons 32 px de haut, bouton « mode de réception » réduit à son emoji 🏪 sur 38 × 44 px. | **Moyenne** | Le seul contrôle de choix retrait/livraison n'a qu'un glyphe emoji, dont le rendu varie selon l'OS, et une cible de 38 px. |
| S-08 | **Micro-texte — le vrai problème typographique.** Sur la vue d'ensemble : 71 éléments à 14 px, 23 à 12,5 px, 6 à 13 px, 3 à 12 px, 1 à 11 px ; **95 nœuds de texte sous 14,5 px** sur cette seule page. `--text-caption` (12,5 px) porte la référence de commande, le badge, le texte juridique du pied de page *et* l'identifiant de spécification divulgué. | **Haute** | Sous le seuil de lecture confortable pour un presbyope ; le texte de 12,5 px est le porteur de toutes les mentions légales (motifs de non-rétractation, durées de conservation). |
| S-09 | **Contrastes sous WCAG AA — plus étroit que la première mesure.** Revérifié sur des couleurs résolues par le navigateur (sRGB via canvas) et non lues en chaîne : tous les échecs proviennent d'**une seule couleur**, `text-ardoise-300` (`#8a9099`), et uniquement sur les glyphes de séparation et les petites métadonnées — **3,22:1** sur blanc à 12,5 px, **2,85:1** sur le fond enfoncé, **2,42:1** sur la carte crème à 14 px. Tous les corps de texte, mentions légales et métadonnées passent largement (`text-ardoise-500` 8,12:1, `text-ardoise-700` 13,11:1, `text-ardoise-900` 17,67:1), de même que le laiton, l'ocre et le pied de page (6,42 à 14,15:1). | **Faible** | L'échec est cantonné aux séparateurs décoratifs : le texte juridique reste lisible. La mention antérieure « Haute » était un artefact d'un `oklab()` mal interprété. Correction par changement de classe vers `text-ardoise-400` (`#5b6068` → 6,33 / 5,62 / 4,77:1), sans toucher au jeton partagé ni à la boutique. |
| S-10 | **Cases à cocher de 20 × 20 px** sur 21 contrôles (17 allergènes, 2 adresses, 2 préférences atelier, 2 lignes de rétractation). Le libellé adjacent est cliquable, ce qui empêche axe de lever une violation, mais la boîte visuelle est sous le minimum de 24 × 24 px de SC 2.5.8. | **Moyenne** | Cible minuscule pour un doigt arthritique ou tremblant ; l'utilisateur rate la case et pense avoir coché autre chose. |
| S-11 | **Anneau de focus invisible sur « Panier, vide ».** `outline: 2px solid rgb(251,249,245)` — la couleur du texte du bouton, appliquée hors du bouton sur un fond crème. Résultat : un anneau blanc cassé sur fond crème. | **Moyenne** | Perte du focus au clavier sur l'un des contrôles les plus utilisés. |
| S-12 | **Tableau de notifications plus large que son conteneur.** Table 337 px dans un wrapper de 304 px avec `overflow-x: visible` → débordement de 33 px dans la gouttière. | **Moyenne** | Débordement visible sur mobile, alors que le reste de la page tient dans 390 px. |
| S-13 | **Identifiants de spécification internes visibles par le client** : « — R20 », « — R6 / R7 / R8 / R9 », « — R1 / R2 / R3 — Art. L. 221-18… », « — F-12b », « — F-14 », « — R21 — art. R. 423-3 C. conso. », « — F-10 / R18 / R19 », « — C-10 / G1–G2 ». | **Moyenne** | Une annotate d'ingénierie fuite dans la production. Aucun sens pour le client, impression de brouillon, et exposition involontaire de l'arbitrage juridique interne. |
| S-14 | **Pied de page : `bonjour@maison-annois.fr` collé à « Espace professionnel → ».** Aucun séparateur entre l'adresse et le lien suivant. | **Moyenne** | Le client ne sait plus où finit l'e-mail et où commence le lien ; clic ambigu. |
| S-15 | **Nommage des magasins incohérent** : « Maison Annois », « Magasin Annois », « Boutique de Sannois », « Maison Annois — Sannois ». | **Moyenne** | Le client cherche « Sannois » et lit « Magasin Annois ». Le repérage spatial est aboli dans la vraie vie. |
| S-16 | **Préambule éditorial de 3 à 5 lignes avant tout contenu actionnable**, sur chaque page (« Votre maison, en un coup d'œil », « Chaque commande garde son détail… », « Vous pouvez tout voir, tout exporter… »). | **Moyenne** | Sur mobile, deux à trois écrans de lecture avant la première action. Charge cognitive inutile. |
| S-17 | **Double navigation.** Bandeau d'onglets (17 entrées) + section « Aller à » (9 cartes) dans la vue d'ensemble. | **Moyenne** | Deux systèmes de navigation concurrents pour la même liste ; risque de divergence et surcharge. |

### 1.2 Vue d'ensemble du compte (`/account`)

| # | Constat | Gravité | Impact |
|---|---|---|---|
| O-01 | **Séparateur décimal incorrect** : le badge affiche « SOLDE **53.26** € DÛ » (point) alors que la même page affiche « 53,26 € » (virgule) et que tout le site utilise la virgule. | **Moyenne** | Incohérence typographique française, perçue comme un défaut de qualité sur un site de vente en ligne. |
| O-02 | **Cadrage « DÛ ».** La carte Arrhes & consignes présente « Dû — 144,61 € · 3 commande(s) avec solde ». Ce solde n'est pas une dette : il se règle au retrait, après pesée. | **Moyenne** | Anxiété artificielle sur une commande déjà payée en arrhes. Le client cherche une explication. |
| O-03 | **Carte « À régler » : trois lignes de libellé identique** (« Solde à régler au retrait / Commande CMD-XXXX ») sans date, sans magasin, sans ordre d'urgence. | **Haute** | Trois lignes indiscernables : impossible de savoir laquelle traiter. La carte ne fait pas son travail de priorisation. |
| O-04 | **Carte « Vos documents » : trois métriques sans rapport** — « Factures disponibles 3 », « Arrhes versées 129,39 € », « Réclamations ouvertes 0 ». | **Faible** | Mélange de nature et d'unité ; le total mental ne se forme pas. |
| O-05 | **Aucune action d'achat depuis le compte.** Ni « Commander à nouveau », ni « Reprendre une commande ». La seule action est « Ouvrir la commande ». | **Haute** | Le client prêt à racheter (le meilleur segment e-commerce) sort par « Retour à la boutique ». Le catalogue perd la commande de rappel. |
| O-06 | **Pas de repère de retrait au-dessus de la ligne de flottaison.** Le prochain retrait est dans la carte « Prochaine étape », mais la date et le magasin n'apparaissent qu'au bas de la page de détail. | **Haute** | Le client doit scroller deux écrans pour savoir **où** et **quand** il doit venir. |
| O-07 | **Pastilles de chronologie de 8 px**, état courant peu marqué. | **Faible** | La progression n'est pas perçue d'un coup d'œil. |

### 1.3 Détail de commande (`/account/orders/[no]`)

| # | Constat | Gravité | Impact |
|---|---|---|---|
| C-01 | **Le solde à payer, la date et le lieu de retrait sont sous la ligne de flottaison.** L'écran d'ouverture montre « Confirmée — La commande est enregistrée pour votre créneau » sans dire quand ni où. « Régler le solde de 53,26 € » et « sam. 31 oct. · 10h00 – 10h30 » arrivent plus bas. | **Haute** | Question première de l'utilisateur (« quand et où ? ») sans réponse au-dessus de la ligne de flottaison. |
| C-02 | **États bloqués traités en prose seule.** « Le délai de modification est passé… Appelez la boutique » : aucun lien `tel:`, aucun bouton, aucune action. « l'annulation suit la politique publiée » : « politique publiée » n'est pas un lien. | **Haute** | L'utilisateur reçoit une explication mais aucun moyen d'agir. Sur mobile il doit noter le numéro à la main. |
| C-03 | **Redondance juridique.** Le motif de non-rétractation est répété par ligne, puis dans le bloc « Rétractation », et « La garantie de conformité de deux ans reste ouverte » apparaît **deux fois** dans le bloc actions. | **Moyenne** | Bruit de lecteur d'écran (le texte est lu trois fois) et fatigue visuelle. |
| C-04 | **« 2 ARTICLE(S) »** — plurielisation automatique brute dans une pastille. | **Faible** | Typo perçue comme machine. |
| C-05 | **« Vous êtes reconnu par votre compte »** — formulation technique. | **Faible** | Incompréhensible. |

### 1.4 Liste des commandes (`/account/orders`)

| # | Constat | Gravité | Impact |
|---|---|---|---|
| L-01 | **Aucun filtre, aucune recherche, aucun tri.** La page ne contient **aucun** `input`, `select` ou `button` de filtrage. Le référentiel F-02 impose filtres (période, statut, mode, magasin), recherche (n° de commande, produit) et tri. | **Haute** | Dès que l'historique dépasse quelques commandes, le client ne retrouve plus rien. Fonctionnalité d'auto-service d'archives inexistante. |
| L-02 | **Structure des cartes ambiguë.** Montant en gros caractères sans libellé (« 76,26 € »), puis « Solde du 53,59 € » — construction fautive — puis la date. Aucune information de priorité entre les commandes. | **Moyenne** | Le client lit un chiffre sans savoir s'il est payé, dû ou estimé. |
| L-03 | **« Reprendre dans le panier » absent des commandes en cours** (présent seulement sur les commandes remises). | **Moyenne** | Le repetition pathway n'est proposé qu'après coup. |

### 1.5 Rétractation (`/account/orders/[no]/withdraw`) — *le meilleur écran du produit*

| # | Constat | Gravité | Impact |
|---|---|---|---|
| R-01 | **Cases à cocher 20 × 20** pour la sélection des lignes (cf. S-10). | **Moyenne** | Même défaut, ici sur le parcours le plus sensible juridiquement. |
| R-02 | **Identifiants internes** « — R1 / R2 / R3 — Art. L. 221-18 et suivants C. conso. ». | **Moyenne** | cf. S-13. |
| R-03 | **Fil d'Ariane « Mon espace / Suivre une commande »** — mélange un espace authentifié et un parcours invité. | **Faible** | Le client se demande s'il est connecté ou en train de suivre une commande anonyme. |

> **À créditer explicitement :** éligibilité calculée ligne par ligne avec motif légal, montant remboursable et montant exclu distingués, mention explicite que les articles exclus « restent votre propriété », informations sur les conséquences **avant** le clic (« Les conséquences, dites avant le clic et non après »), échéance de remboursement calculée (« au plus tard le vendredi 20 novembre 2026 »), frais de livraison inclus (art. 13(2)), droit de retenue (art. 13(3)), retour à la charge du client (art. 14(1)), compteur « Il reste 11 jour(s) », étape de confirmation distincte. **Conforme à l'art. 11a et au référentiel R1-R3.** Il manque seulement l'**accès invité** de la fonction, à confirmer sur le parcours `/track` (voir 1.9).

### 1.6 Réclamation (`/account/orders/[no]/claim`) — *conforme, une lacune*

| # | Constat | Gravité | Impact |
|---|---|---|---|
| P-01 | **Aucun envoi de photo.** Le formulaire ne contient que `select` (article), `select` (nature), `select` (remedy), `textarea` (message). Le référentiel F-11b exige jusqu'à 5 photos (10 Mo, métadonnées supprimées). | **Moyenne** | Pour un défaut de fraîcheur ou une avarie de transport, **la photo est la preuve**. Son absence transforme une réclamation simple en dossier non recevable. |
| P-02 | **Aller-retour inutile.** `/account/support` affiche « Aucune réclamation — Vous pouvez en ouvrir une depuis le détail d'une commande remise » avec un bouton « Voir mes commandes » : le client doit retrouver la bonne commande, puis rouvrir le détail. | **Moyenne** | Parcours en 3 sauts pour le geste le plus important après la livraison. |
| P-03 | *Points forts :* « Deux délais, deux usages » — délai qualité 3 jours **et** garantie de conformité 2 ans avec dates exactes, explicitement non raccourcie (art. L. 217-12). Motifs complets, remèdes complets, réponse annoncée sous 2 jours ouvrés. **Conforme R19 et F-11b.** |

### 1.7 Notifications (`/account/notifications`)

| # | Constat | Gravité | Impact |
|---|---|---|---|
| N-01 | **Tableau plus large que son conteneur** (cf. S-12). | **Moyenne** | Débordement dans la gouttière. |
| N-02 | **Bouton « Désactivé — activer ».** L'étiquette concatène l'état et l'action ; le client ne sait pas s'il voit son état ou ce qu'il va déclencher. | **Moyenne** | Ambiguïté sur un contrôle qui manipule un consentement. |
| N-03 | **Identifiant interne** « — F-12b ». | **Moyenne** | cf. S-13. |
| N-04 | *Points forts :* 12 lignes réelles, chaque ligne décrivant le message réellement envoyé ; les messages obligatoires sont marqués et expliqués ; SMS par double opt-in explicité. **Conforme F-12a/F-12b.** |

### 1.8 Réglages, préférences, confidentialité, dépôts, sécurité produit, support

| # | Page | Constat | Gravité |
|---|---|---|---|
| G-01 | Réglages | **« COMPTE LOCAL (MOT DE PASSE) »** — jargon d'implémentation pour désigner un compte par mot de passe. | **Faible** |
| G-02 | Réglages | **Appareils connectés : deux lignes identiques « Ordinateur · Chrome ».** Ni système d'exploitation, ni pays, ni adresse IP : le client ne peut pas distinguer sa session de celle d'un tiers — c'est-à-dire identifier un usage frauduleux. | **Moyenne** |
| G-03 | Réglages | **Identifiant interne** « — F-14 ». | **Moyenne** |
| G-04 | Confidentialité | **Saisie de « CONFIRMER »** en texte libre pour confirmer l'effacement. Aucune `aria-describedby`, `autocomplete="off"`, pas d'indication de casse → risque d'échec (et d'échec confondu avec une erreur serveur). | **Moyenne** |
| G-05 | Confidentialité | **Tableau des durées de conservation : valeurs alignées à droite et repliées sur 2 lignes**, sans la base légale. Le référentiel F-07 exige « sa date et sa base légale ». | **Moyenne** |
| G-06 | Confidentialité | Deux contrôles distincts portent `name="note"` (un `input` text, un `textarea`) dans deux formulaires différents → risque de collision lors de la soumission. | **Faible** |
| G-07 | Préférences | 17 allergènes en colonne unique, cases 20 × 20, chacun avec une description en petit gris. | **Moyenne** |
| G-08 | Dépôts | **Intro en prose juridique pur** : « Le versement d'avance n'est pas une avance comme les autres : sa nature juridique décide de ce qui se passe en cas de renoncement. » C'est la première phrase lue par un client de 75 ans. | **Haute** |
| G-09 | Dépôts | **Cartes « Dû » / « Rendu »** avec de grands chiffres — même cadrage anxogène que O-02. | **Moyenne** |
| G-10 | Sécurité produit | **Identifiant interne** « — R21 — art. R. 423-3 C. conso. ». | **Moyenne** |
| G-11 | Support | **Identifiant interne** « — F-10 / R18 / R19 ». | **Moyenne** |
| G-12 | Support + pied de page | **Bloc médiateur incomplet.** Le pied de page ne porte que « Médiateur : CM2C ». L'art. R. 616-1 impose les coordonnées **postales et électroniques**, l'adresse du site, les langues et les types de litiges ; l'art. L. 616-1 impose de répéter l'information après une réclamation non résolue. La page `/account/support` cite l'art. L. 612-1 mais le pied de page — qui est le canal le plus lu — reste lacunaire. | **Moyenne (conformité)** |
| G-13 | Support | *Point fort :* médiation annoncée gratuite, SignalConso et juridiction cités, « Aucune de ces démarches ne dépend de notre accord », délai de 2 jours ouvrés annoncé. **Bonne pratique.** |

### 1.9 Espaces invité et public

| # | Page | Constat | Gravité |
|---|---|---|---|
| U-01 | `/track` | **Placeholder « Format CMD-0000. »** — numéro d'exemple invalide ; induit en erreur. | **Faible** |
| U-02 | `/track` | **Justification de conception exposée au client** : « Un message d'erreur ne dit jamais si la commande existe… » suivi de « — C-10 / G1–G2 ». Du texte d'ingénierie dans l'interface publique. | **Moyenne** |
| U-03 | `/track` | **Bloc « Deux niveaux d'accès » placé sous le formulaire**, et texte d'introduction de 3 lignes avant. La promesse « le détail — contenu, lots, factures, réclamation, **rétractation** » n'a pas de contrepartie visible : il faut entrer le code à 6 chiffres, puis retrouver l'action. | **Moyenne** |
| U-04 | `/boutique` | **238 cibles tactiles < 44 px** relevées sur la seule page catalogue mobile — liens de catégories, puces, liens secondaires. | **Moyenne** |
| U-05 | `/panier` | **Violation d'ordre de titres** (axe `heading-order`) : un `h3` suit un `h1` sans `h2` intermédiaire. | **Moyenne** |
| U-06 | `/` | *Point fort :* hero clair, bandeau de réassurance (pesée, découpe à la commande, chaîne du froid, éleveurs choisis), prix au kg explicite. **Le meilleur work de la boutique.** |

### 1.10 Le problème structurel : deux espaces clients concurrents

`/compte` (legacy, non protégé) et `/account` (nouveau) coexistent. Le legacy est **plus riche** sur plusieurs points :

| Fonctionnalité | `/compte` (legacy) | `/account` (nouveau) |
|---|---|---|
| Pass de retrait **QR code** | ✅ « Voir le QR code de retrait → » | ❌ **Absent** (F-05 / UI-06) |
| « Composer une commande » | ✅ 2 occurrences | ❌ Absent |
| Statut de fidélité « Client de confiance » | ✅ (dépense, allergies, e-mails de saison) | ❌ Absent |
| Bloc de réassurance « Appelez le comptoir » | ✅ | ❌ |
| Badges de compteur sur les onglets (« Mes commandes **2** ») | ✅ | ❌ |
| Reprise de commande | ✅ « Reprendre dans le panier » | ⚠️ seulement sur commande remise |

**Gravité : Haute.** C'est une fracture de modèle mental : le client qui connaît l'ancien espace ne retrouve pas ses repères, et le nouveau est plus pauvre sur les usages à plus forte valeur. Le pass de retrait est le point le plus critique : **sans lui, le retrait en magasin se fait à la mémoire ou par appel**, alors que c'est le mode de retrait par défaut d'une boucherie multi-magasins.

---

## 2. Points de friction côté utilisateur final

### 2.1 Utilisateur standard

1. **Je ne sais pas où sont mes commandes.** 17 rubriques dans une bande de défilement horizontale de 1 945 px ; 3 visibles. Il faut comprendre le geste de glissement avant de découvrir qu'il existe des factures, des arrhes, des réclamations. *Effet : abandon.* — **La barre « Aller à » de la vue d'ensemble est la seule porte de sortie, mais elle est en bas de page, donc inutilisable depuis le haut.**
2. **Je ne sais pas combien je dois et quand.** La vue d'ensemble affiche « SOLDE 53.26 € DÛ » — un point décimal français incorrect et un cadrage de dette. Le détail de commande cache la date et le lieu de retrait sous deux écrans.
3. **Je suis bloqué sans issue.** « Appelez la boutique » sans numéro cliquable ; « la politique publiée » sans lien ; « ouvrez une réclamation » sans destination sur la commande non remise.
4. **Je ne peux pas filtrer mon historique.** Aucun champ de recherche sur la liste des commandes.
5. **Je ne peux pas racheter.** Aucune action « commander à nouveau » depuis le compte.
6. **Je lis la même chose trois fois.** Motif de non-rétractation répété, garantie de conformité répétée.
7. **Je ne comprends pas ce que « Dû 144,61 € » veut dire.** Le mot « Dû » transforme un bon de commande en dette.
8. **Je ne trouve pas mes factures.** « 3 » dans une carte, un lien dans le détail de commande, et un onglet invisible. Le référentiel veut un centre documentaire.
9. **Je ne peux pas claimedirectement.** `/account/support` renvoie vers la liste des commandes : trois sauts pour déposer un dossier.

### 2.2 Client âgé — barrières spécifiques

| Barrière | Constat mesuré | Conséquence |
|---|---|---|
| **Le mode confort de lecture n'existe pas sur mobile** | Le contrôle est `hidden` sous 1024 px | La seule réponse logicielle à la fatigue visuelle est retirée au segment le plus exposé |
| **Texte de 11 à 12,5 px** | 30 éléments ≤ 12,5 px sur la vue d'ensemble ; mentions légales entières en 12,5 px | Le texte juridique — celui qui engage — est le moins lisible |
| **Un gris sous AA (2,42 à 3,22:1)** | `text-ardoise-300` sur blanc, enfoncé et crème | Cantonné aux glyphes de séparation et aux métadonnées ; le texte juridique lui-même est à 13,1:1 |
| **Cases à cocher 20 × 20** | 21 contrôles | Raté de clic, double-clic involontaire, frustration |
| **Cibles de 22 à 38 px** | Téléphone, logo, rayons, bouton de retrait | Cibles trop fines pour un tremblement |
| **Navigation invisible** | 14 rubriques hors écran, sans indice de glissement | Le client conclut que la fonction n'existe pas |
| **Prose juridique en ouverture** | Page Dépôts, page Retractation, page Confidentialité | Abandon de la lecture, impression d'arnaque |
| **Contradiction de nommage** | « Magasin Annois » / « Boutique de Sannois » | Le client ne sait pas où aller |
| **Anneau de focus invisible** | Bouton Panier | Navigation clavier cassée sur le contrôle principal |
| **Saisie de « CONFIRMER »** | Saisie littérale, sensible à la casse | Échec d'effacement du compte, interpreted comme un bug serveur |
| **Aucune grande cible de texte** | Pas de réglage de taille de police dans l'espace client | Le confort de lecture ne couvre pas la typographie |

**Le point le plus important :** la boutique a fait le travail difficile — la traçabilité, la température, les lots, la médiation, les arrhes sont expliqués avec justesse et sans jargon inutile. Mais **toute cette qualité est écrite en 12,5 px gris à 3,2:1**. Le client âgé ne la verra pas. C'est un problème de design, pas de contenu.

---

## 3. Stratégie de correction et plan d'action

### 3.1 Feuille de route priorisée

#### P0 — Bloquant (2 à 3 semaines)

| # | Action | Réf. | Critère de recette |
|---|---|---|---|
| 1 | **Supprimer le `<main>` imbriqué.** Un seul `main` par page ; la grille de l'espace client passe en `<div role="none">` ou `<section aria-labelledby>`. | S-01 | axe : 0 violation `landmark-*` et `region` sur les 20 pages |
| 2 | **Activer « Confort de lecture » sur mobile.** Bouton de 44 × 44 px dans le bandeau mobile ; le mode passe le corps à ≥ 18 px, les métadonnées à ≥ 15 px, et écarte le contraste. Persistance via `localStorage`. | S-04 | Le contrôle est atteignable et actif à 390 px ; le corps passe à 18 px |
| 3 | **Remettre le texte au-dessus du seuil de lisibilité.** Nouvelle échelle : `text-micro` 14 px (au lieu de 12,5), `text-caption` 15 px, `text-small` 16 px, corps 17 px, `text-body-lg` 18 px. Aucun texte utile sous 14 px. | S-08 | 0 élément < 14 px hors décoratif |
| 4 | **Reprendre les contrastes — changement de classe, pas de jeton.** Remplacer les 10 occurrences fautives de `text-ardoise-300` par `text-ardoise-400` (`#5b6068`) : 6,33:1 sur blanc, 5,62:1 sur fond enfoncé, 4,77:1 sur crème. **Ne pas modifier `--color-ardoise-300`** : ce jeton est partagé avec la boutique. Aucune autre couleur n'échoue. | S-09 | 0 échec de contraste sous axe ; 0 `text-ardoise-300` sur un nœud de texte dans l'espace client |
| 5 | **Neutraliser la barre fixe.** Remplacer « Appeler / Panier » par une barre de contexte **par page** (sur la vue d'ensemble : solde + prochain retrait ; sur le détail : « Régler le solde »), hauteur ≤ 64 px, `padding-bottom: calc(64px + env(safe-area-inset-bottom))` sur le contenu, et un bouton d'appel `tel:` réel. | S-02 | Aucun élément masqué au chargement sur les 20 pages |
| 6 | **Rétablir la navigation.** Sur mobile : bouton « Menu » ouvrant un tiroir groupé en 4 sections (Commander / Argent / Préférences / Compte). Sur desktop : conserver la colonne, mais **groupée et avec des séparateurs**. Retirer la section « Aller à ». | S-05, S-17 | Toutes les rubriques atteignables en 1 clic, sans geste horizontal |
| 7 | **Retirer les identifiants de spécification du texte client.** Les conserver en `data-spec="R20"` pour la QA. | S-13 | 0 occurrence de `— R\d`, `— F-\d`, `C-10`, `G1–G2` dans le DOM rendu |
| 8 | **Corriger le badge « DÛ ».** « Solde à régler — 53,26 € » (virgule, via `Intl.NumberFormat('fr-FR')`), et renommer « Dû / Rendu » en « À régler au retrait / Consignes remboursées ». | O-01, O-02, G-09 | Aucun point décimal dans les montants |

#### P1 — Important (3 à 5 semaines)

| # | Action | Réf. |
|---|---|---|
| 9 | **Filtres, recherche et tri sur `/account/orders`.** Chips de statut (En cours / Terminées), sélecteur de période, recherche n° de commande + produit, tri par date. Sur mobile : un seul bouton « Filtrer » ouvrant une feuille, plus un champ de recherche persistant. | L-01 |
| 10 | **Actions sur commande en état bloqué.** Chaque état bloqué devient une **carte d'action** : titre, explication courte, et un bouton (`Appeler le 01 39 47 12 12`, `Voir la politique d'annulation`, `Ouvrir une réclamation`). Aucun texte mort. | C-02 |
| 11 | **Restructurer le haut du détail de commande.** Bloc « Récupération » en tête : `Retrait · sam. 31 oct. · 10h00–10h30 · Boutique de Sannois` + montant + bouton « Régler le solde de 53,26 € ». | C-01, O-06 |
| 12 | **Ajouter le pass de retrait.** QR code + code à 6 chiffres, sur `/account/orders/[no]` et dans la vue d'ensemble — comme dans l'espace legacy. | 1.10, F-05 |
| 13 | **Ajouter « Commander à nouveau »** depuis le compte (historique + carte « À régler » + accueil), avec rappel des écarts de prix. | O-05, F-15 |
| 14 | **Dédupliquer les mentions légales.** Une seule occurrence du motif de non-rétractation et de la garantie de conformité par commande, dans un encadré « Ce que la loi permet et ce qu'elle n'interdit pas », repliable. | C-03 |
| 15 | **Rendre la réclamation atteignable en un geste.** Bouton « Déposer une réclamation » sur `/account/support` qui ouvre un formulaire hors commande (article + lot) si le client ne retrouve pas sa commande. | P-02 |
| 16 | **Ajouter les photos à la réclamation.** Zone d dépôt 5 × 10 Mo, métadonnées supprimées, aperçu avant envoi, compresseur côté client. | P-01, F-11b |
| 17 | **Cibles tactiles.** Cases à cocher 24 × 24 px (visuel) avec zone cliquable 44 × 44 ; liens du bandeau ≥ 44 px ; bouton « mode de réception » 44 × 44 avec libellé visible, pas seulement un emoji. | S-07, S-10 |
| 18 | **Anneau de focus unique et visible partout.** Token `--focus-ring: 2px solid #9B2226` + `outline-offset: 2px` + double halo `box-shadow: 0 0 0 4px rgba(255,255,255,.9)` pour fonctionner sur fond clair comme sur fond sombre. | S-11 |
| 19 | **Groupe de navigation et tokens de nommage.** Un seul vocabulaire : « Boutique de Sannois », « Maison Annois — Sannois », « Retrait à Sannois ». Aucune désignation concurrente. | S-15 |
| 20 | **Corriger le pied de page.** Espace insécable avant « Espace professionnel », et bloc médiateur complet (coordonnées postales + électroniques + site + langues + types de litiges) visible sur toutes les pages, pas seulement le nom. | S-14, G-12 |
| 21 | **Le pied de page doit porter l'information de réassurance pour les clients âgés** : numéro de téléphone cliquable, horaires, « qui appeler ». | 2.2 |

#### P2 — Confort (5 à 7 semaines)

| # | Action | Réf. |
|---|---|---|
| 22 | **Supprimer les préambules éditoriaux** ou les réduire à une ligne. Le titre de page suffit ; le texte d'accueil part en pied de page ou dans une aide contextuelle. | S-16 |
| 23 | **Refaire le tableau de notifications** en cartes empilées sur mobile (type de message + état e-mail + état SMS + action), tableau seulement à partir de 768 px. | N-01, N-02 |
| 24 | **Distinguer état et action** dans les bascules : état en texte (« Désactivé ») + bouton d'action (« Activer ») séparés visuellement. | N-02 |
| 25 | **Appareils connectés enrichis** : système d'exploitation, navigateur, ville approximative, date de création de la session, bouton « Déconnecter cette session ». | G-02 |
| 26 | **Confirmation d'effacement** : remplacer la saisie de « CONFIRMER » par une case à cocher explicite « Je confirme vouloir supprimer mon compte », avec un résumé des conséquences (délai de 30 jours, données conservées 10 ans) et un dialogue de confirmation natif. | G-04 |
| 27 | **Durées de conservation** : passer en liste (durée + base légale + conséquence), pas en tableau à valeurs repliées. | G-05 |
| 28 | **Prose juridique : version courte + version longue.** Une phrase simple par défaut (« Vous avez payé 23 € d'acompte. Si vous annulez, cet acompte vous est rendu et vous perdez 23 € si la boutique a lancé la préparation. »), le détail juridique dans un encadré repliable. | G-08, C-03 |
| 29 | **Corriger le placeholder** « Format CMD-0000. » → « ex. CMD-2452 ». Retirer la justification de conception exposée au public sur `/track`. | U-01, U-02 |
| 30 | **Tableaux** : correction de l'ordre des titres sur `/panier`, et contrôle général de la hiérarchie `h1 → h2 → h3`. | U-05 |
| 31 | **Fusionner les deux espaces clients** : absorber `/compte` dans `/account` (ou l'inverse) avant d'élargir. Un seul modèle mental. | 1.10 |
| 32 | **Écran « Suivre une commande » invité** : remonter le bloc « Deux niveaux d'accès » au-dessus du formulaire et faire apparaître l'action « Rétracter » dans le palier detail. | U-03 |

### 3.2 Patrons d'interface recommandés

| Défaut | Patron de remplacement |
|---|---|
| Navigation horizontale invisible | **Tiroir de navigation groupé** (mobile) / **colonne groupée avec titres de section** (desktop). La section courante est marquée par un filet à gauche + `aria-current="page"`. |
| Texte mort « Appelez la boutique » | **Carte d'action** : icône + libellé + conséquence + bouton. Modèle : *Ce que vous pouvez faire maintenant.* |
| Motifs légaux répétés | **Encadré « Vos droits » repliable** : une phrase simple en surface, la référence juridique exacte dans le `<details>`. |
| Badge « DÛ » | **Jauge de solde** : montant + libellé explicite + date d'échéance. Jamais un adverbe seul. |
| Cases 20 px | **Case 24 px + label 44 px de zone cliquable**, état coché à fort contraste (bordure 2 px + coche épaisse). |
| Tableau notifications | **Liste de cartes** (mobile) / tableau avec `<caption>`, `scope="col"` et `scope="row"` (desktop). |
| Montant sans libellé | **Paire libellé/valeur** systématique, le libellé à gauche en `text-small`, la valeur à droite en `font-semibold`, alignement tabular-nums. |
| Lien vers une politique | **Lien réel** vers `/cgv#annulation`, pas la mention « la politique publiée ». |
| Texte de 12,5 px gris | **Échelle de tokens** : `--fs-micro: 14px`, `--fs-caption: 15px`, `--fs-small: 16px`, `--fs-body: 17px`, `--fs-lead: 19px`. Couleurs : `--text-muted` à 4,5:1 minimum, `--text-subtle` réservé aux bordures. |
| Préambule éditorial | **Titre + action principale**, le texte d'explication dans un `<details>` ou en aide contextuelle. |

### 3.3 Jetons de design à introduire ou corriger

```css
/* Typographie — plancher relevé, À PORTÉE ESPACE CLIENT (voir H3).
   Production : --text-caption .78125rem (12,5px), --text-overline .75rem (12px),
   --text-small .875rem (14px), --text-body 1rem (16px). */
--text-caption: 0.875rem;   /* 14px — était 12,5px, nouveau plancher */
--text-overline: 0.8125rem; /* 13px — était 12px */
--text-small:   0.9375rem;  /* 15px — était 14px */
--text-body:    1.0625rem;  /* 17px — était 16px */
--text-lead:    1.1875rem;  /* 19px — inchangé */

/* Couleurs — surcharges À PORTÉE, PAS de modification de jeton global.
   La production fournit déjà ardoise-400 (#5b6068) : la correction consiste à L'UTILISER.
   --color-ardoise-300 (#8a9099) reste intact : il est partagé avec la boutique. */
--text-primary:  var(--color-ardoise-900);   /* #121316 — inchangé */
--text-muted:    var(--color-ardoise-400);   /* #5b6068 — 6,33:1 blanc, 4,77:1 crème */
--text-on-cream: var(--color-ardoise-500);   /* #4b5058 — 8,12:1 sur zone-150 */
--text-accent:   var(--color-laiton-700);    /* #6e5429 — déjà à 6,74:1, inchangé */
--border-subtle: var(--color-lin-200);       /* #e7e0d3 — inchangé */

/* Cibles */
--tap-min: 44px;           /* cible tactile WCAG 2.2 / usage senior */
--checkbox-size: 24px;     /* SC 2.5.8 — au lieu de 20px */

/* Focus — visible sur tous les fonds */
--focus-ring: 2px solid #9B2226;
--focus-offset: 2px;
--focus-halo: 0 0 0 4px rgba(255,255,255,.92);

/* Navigation */
--nav-mobile: tiroir groupé (remplace la bande 1945px);
--nav-mobile-safe: env(safe-area-inset-bottom);

/* Contexte */
--context-bar-height: 64px;         /* au lieu de 87px */
--content-safe-bottom: calc(64px + env(safe-area-inset-bottom));
```

### 3.4 Ce qu'il ne faut pas casser

La base **juridique et éditoriale est la meilleure partie du produit**. En corrigeant l'affichage, préserver mot pour mot :

- le parcours de rétractation (`/withdraw`) et son étape de confirmation distincte ;
- l'avis de rappel (`/account/safety`) : motif, conduite à tenir, référence RappelConso, date de notification de l'autorité, remboursement sans justificatif ;
- les « Deux délais, deux usages » de la réclamation (3 jours / 2 ans) ;
- la transparence du médiateur de la consommation ;
- la distinction arrhes / consigne et la restitution de la consigne hors TVA ;
- la trace « lot, origine, date de découpe, pays d'élevage et d'abattage, établissement ».

Les corrections proposées sont **des corrections de surface, de hiérarchie et de navigation** — pas une réécriture du discours. Le discours actuel est juste ; c'est sa lisibilité qui échoue.

---

## Annexe — Méthode et reproductibilité

- **Outil :** Playwright + Chromium 156 headless, 56 captures pleine page (390 × 844 et 1440 × 1 000), axe-core 4.10.2 injecté sur chaque page, mesure de contraste et de cibles par `getComputedStyle` / `getBoundingClientRect`.
- **Pages auditées :** 19 routes de l'espace client authentifié, `/track`, `/compte`, `/panier`, `/`, `/boutique`, `/boutique/boeuf`, `/livraison-retrait`, `/allergenes-origines`, `/faq`, `/mentions-legales`, `/cgv` — en mobile et desktop.
- **Violations axe relevées :** 4 sur les 40 captures d'espace client (landmark), 1 sur `/panier` (heading-order), 1 sur les pages publiques.
- **Éléments de preuve :** `/home/user/audit/audit_raw.json` (métriques brutes), `/home/user/audit/shots/` (56 captures), `/home/user/audit/crops/` (52 segments lisibles), `/home/user/audit/txt/` (texte de chaque page).
- **Limites :** l'audit porte sur le rendu Chromium ; Safari iOS et Firefox n'ont pas été testés (recommandé avant clôture P0, notamment pour `env(safe-area-inset-bottom)` et le rendu des emoji de mode de réception). Le parcours invité avec code à 6 chiffres n'a pas été exécuté de bout en bout.
