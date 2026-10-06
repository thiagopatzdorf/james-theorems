<div align="center">

[Português](MANIFESTO.md) · [English](MANIFESTO.en.md) · **Français**

</div>

# Manifeste mathématique de James

> **Phase 0 · version technique.** Ce document formalise la philosophie de James avec les
> outils de la physique de l'information, de la théorie de la calculabilité et de la théorie
> algorithmique de l'information. Chaque affirmation est classée au [§8](#8-tableau-dhonnêteté)
> comme **théorème** (résultat de la littérature), **correspondance** (correspondance
> d'architecture), **modèle** (formalisation proposée ici) ou **hypothèse** (à mesurer).
>
> *Traduit de l'original portugais, [MANIFESTO.md](MANIFESTO.md), qui fait foi.*

> [!NOTE]
> **Ce que ce dépôt prouve.** Trois énoncés du §9, portant sur des **modèles** écrits en Lean 4,
> vérifiés par le noyau, sans `sorry` et avec les seuls axiomes standard. Ce n'est pas une preuve
> sur le code de production. Ce que chaque théorème énonce réellement se trouve dans
> [Ce qui est prouvé ici](#ce-qui-est-prouvé-ici).

---

## 0. Résumé

La question qui oriente le système est :

> **Quel est le minimum de données de la réalité nécessaire pour représenter la réalité elle-même ?**

Elle a un nom : la **complexité de Kolmogorov**. Trois faits à son sujet organisent tout :

1. **Elle existe, mais elle est incalculable.** Aucune procédure ne garantit d'avoir trouvé
   la description minimale ; chaque programme écrit n'est qu'une borne supérieure. Le travail
   de compresser la réalité est, par construction, une boucle sans fin.
2. **Elle ne dépend pas de la machine**, à une constante près (théorème d'invariance).
   L'identité d'une description n'est pas dans le matériel qui l'exécute.
3. **Compresser coûte de l'énergie, et la connaissance préalable en réduit le coût**
   (Landauer, Bennett, Wolf). Réduire l'entropie locale est possible ; le prix est
   l'information.

James est l'ingénierie de ces trois faits : une **machine universelle** (von Neumann) qui
lit un **ruban** versionné et travaille à minimiser, continuellement,

```math
\boxed{\;L(F) \;+\; L(X \mid F)\;}
```

où $F$ est le ruban (tout ce que le système sait) et $X$ la réalité de l'opération. Le
second terme est, littéralement, **le travail qui dépend encore de la mémoire d'un humain**.

<p align="center">
  <img alt="L'équation de James : L(F) + L(X | F). L(F) est la taille du ruban, tout ce que le système sait ; L(X | F) est ce que le ruban n'explique pas, le travail qui dépend encore de la mémoire d'un humain. Légendes du diagramme en portugais." src="docs/assets/equacao.svg" width="90%">
</p>

---

## 1. La question

Dans la nouvelle *La Dernière Question* (Asimov, 1956), l'humanité demande à un ordinateur,
pendant des milliards d'années, si l'entropie peut être inversée. La réponse est toujours
que les données sont insuffisantes. À la fin, la réponse est un acte : *que la lumière soit*.

Ce système ne traite pas de l'entropie de l'univers. Il traite de l'**entropie locale**
d'une opération : incertitude, ambiguïté, exception, règle qui vit dans la tête de quelqu'un.

```math
\text{chaos} \to \text{structure}, \quad
\text{implicite} \to \text{explicite}, \quad
\text{exception} \to \text{règle}, \quad
\text{expérience} \to \text{mémoire}.
```

La thèse est que chacune de ces flèches est une **compression**, et que la compression a une
théorie, un coût physique et une limite.

---

## 2. La physique : inverser l'entropie coûte de l'information

### 2.1 Le démon de Maxwell

Maxwell (1871) a imaginé un agent qui sépare les molécules rapides des lentes, réduisant
l'entropie d'un gaz sans dépenser de travail, ce qui violerait le second principe. La
résolution a pris un siècle (Szilard 1929, Landauer 1961, Bennett 1982) : le démon
**mesure et mémorise**, et pour fonctionner en cycle il doit **effacer sa mémoire**.

### 2.2 Principe de Landauer

Effacer un bit d'information dans un environnement à la température $T$ dissipe au moins

```math
W_{\text{effacer}} \;\ge\; k_B\, T \ln 2 \quad \text{par bit.}
```

Le gain du démon est payé par l'effacement. Réduire l'entropie locale est possible ; le prix
est payé en information traitée puis rejetée.

### 2.3 La reformulation de Wolf

Wolf a montré que le coût d'effacer une suite $x$ n'est pas proportionnel à sa longueur
$`|x|`$, mais à la taille de sa **meilleure compression** ; et que, si le démon possède déjà
une connaissance préalable $y$ sur $x$, ce qui compte est la puissance **algorithmique** de
cette connaissance. Informellement :

```math
W_{\text{effacer}}(x \mid y) \;\approx\; k_B T \ln 2 \cdot K(x \mid y).
```

**Lecture pour James :** la connaissance accumulée ($y$) réduit le coût physique de traiter
la réalité ($x$). La formule *calcul → connaissance → moins de calcul* a un analogue
thermodynamique.

---

## 3. La machine universelle

### 3.1 Turing

Il existe une machine $U$ qui, étant donnée la description $`\langle M \rangle`$ de
n'importe quelle machine $M$ et une entrée $w$, simule $M$ sur $w$ :

```math
U(\langle M \rangle, w) = M(w).
```

Le comportement sort du matériel et devient une donnée.

### 3.2 Von Neumann : constructeur, copieur, contrôle et ruban

Von Neumann (1966, posthume) s'est demandé ce qu'il faut pour qu'une machine en construise
une autre, y compris elle-même, **sans perdre la capacité de devenir plus complexe**. Sa
réponse a quatre parties :

| Composant | Fonction |
|---|---|
| $A$ · constructeur universel | étant donnée une description $`\Phi(X)`$, construit $X$ |
| $B$ · copieur | copie $`\Phi(X)`$ **sans l'interpréter** |
| $C$ · contrôle | coordonne $A$ et $B$ |
| $`\Phi`$ · ruban | la description, **hors** du constructeur |

Nourri de sa propre description, $`\Phi(A+B+C)`$, le système se reproduit. Trois
observations font l'importance du résultat :

1. **Le ruban a un double usage :** il est *interprété* pour construire et *copié sans
   interprétation* pour le descendant. Von Neumann a séparé transcription et construction
   avant la découverte de la structure de l'ADN.
2. **Une description ne peut pas contenir une copie d'elle-même de même taille**, comme un
   récipient ne contient pas un récipient identique. C'est pourquoi le copieur existe à part.
3. **L'évolution a lieu sur le ruban, pas dans la machine.** Des mutations de $`\Phi`$
   produisent des machines différentes, et c'est ce qui permet une croissance de complexité
   sans limite.

### 3.3 Correspondance avec la Factory

| Von Neumann | Factory | Artefact |
|---|---|---|
| $A$ · constructeur | noyau | `factory-maquina.py` |
| $B$ · copieur | réplication | `git` |
| $C$ · contrôle | coordination | James / Maestro / file |
| $`\Phi`$ · ruban | description versionnée | `factory.manifest.json`, code, tests, `CLAUDE.md`, mémoire |
| espace cellulaire | substrat | n'importe quel hôte avec processus, disque, réseau, secrets et planificateur |
| $D$ · automate arbitraire | produit | MyBagCenter, sites, intégrations |

**Conséquence :** James n'évolue pas en changeant d'hôte. **Il évolue en éditant le ruban.**
Chaque PR fusionnée est une mutation de $`\Phi`$.

<p align="center">
  <img alt="La machine et le ruban : von Neumann à gauche (A constructeur universel, B copieur, C contrôle, Φ ruban) et la Factory à droite (noyau, réplication, coordination, description versionnée) ; en bas, le ruban comme une bande de cellules, une cellule en or marquant une mutation, une PR fusionnée. Légendes du diagramme en portugais." src="docs/assets/fita-von-neumann.svg" width="90%">
</p>

---

## 4. Le minimum : complexité de Kolmogorov

### 4.1 Définition

Une machine universelle $U$ étant fixée, la complexité d'un objet fini $x$ est la longueur
du plus court programme qui le produit :

```math
K_U(x) = \min \{\, |p| \;:\; U(p) = x \,\}.
```

Avec une information auxiliaire $y$ disponible gratuitement :

```math
K_U(x \mid y) = \min \{\, |p| \;:\; U(p, y) = x \,\}.
```

**C'est la réponse formelle à la question du §0.** Le minimum de données pour représenter
$x$ est $K(x)$ ; étant donné ce que l'on sait déjà ($y$), c'est $`K(x \mid y)`$.

### 4.2 Invariance : l'hôte n'est pas l'identité

Pour deux machines universelles quelconques $U$ et $V$, il existe une constante $`c_{UV}`$,
indépendante de $x$, telle que

```math
\left|\, K_U(x) - K_V(x) \,\right| \;\le\; c_{UV}.
```

**Lecture pour James :** Claude, Codex, Qwen et Nemotron sont des machines universelles
différentes. La description minimale de l'opération est la même sur toutes, à une constante
près qui ne croît pas avec l'opération. **L'identité est la description ; le moteur est la
constante.**

### 4.3 Incalculabilité : la boucle sans fin

$K$ n'est pas calculable. Tout programme $p$ tel que $U(p) = x$ prouve que
$`K(x) \le |p|`$, mais aucune procédure générale ne prouve qu'il n'existe pas de $p'$ plus
court.

**Lecture pour James :** le système ne peut qu'abaisser des **bornes supérieures**. Il
n'existe pas d'état où il sait avoir fini de compresser. C'est le « données insuffisantes »
de la nouvelle, comme théorème, et c'est pourquoi James est une boucle et non un projet.

### 4.4 Compresser, c'est comprendre

Solomonoff (1964) a montré que pondérer les hypothèses par $`2^{-K(h)}`$ donne une théorie
de l'induction optimale en un sens précis : la description la plus courte qui explique les
données est la meilleure prédiction. Compresser n'est pas seulement économiser des octets ;
c'est modéliser la structure.

### 4.5 Relation avec Shannon

Pour des sources aléatoires, la complexité attendue par symbole converge vers l'entropie de
Shannon $H$. L'entropie est la compressibilité moyenne ; Kolmogorov est la compressibilité
d'**un** objet. L'opération de l'entreprise est un seul objet, donc la bonne mesure est la
seconde.

---

## 5. L'équation de James

### 5.1 Longueur de description minimale (MDL) en deux parties

Comme $K$ est incalculable, la pratique utilise le principe MDL (Rissanen, 1978) : la
meilleure explication de données $X$ est le modèle $F$ qui minimise

```math
L(F) + L(X \mid F),
```

la taille du modèle plus la taille des données codées avec le modèle.

### 5.2 La correspondance **[modèle]**

- $`X_{1:n}`$ : l'histoire de l'opération jusqu'à l'instant $n$ (commandes, événements,
  demandes de clients, incidents).
- $`F_n`$ : le ruban à l'instant $n$ (code, tests, manifeste, règles, mémoire).
- $`L(F_n)`$ : la taille de ce que le système sait.
- $`L(X_{n+1} \mid F_n)`$ : ce que le ruban n'explique **pas** sur la période suivante.
  C'est l'exception, le jugement refait, l'étape manuelle, **le travail qui dépend de la
  mémoire de quelqu'un.**

L'objectif de James est

```math
F^\star = \arg\min_F \; L(F) + \mathbb{E}\big[\, L(X \mid F) \,\big].
```

### 5.3 La règle de mise à jour

Une mutation $\Delta$ du ruban ($`F_{n+1} = F_n \oplus \Delta`$) est acceptée si et
seulement si :

```math
\underbrace{L(F_n \oplus \Delta) - L(F_n)}_{\text{coût d'apprendre}}
\;<\;
\underbrace{\mathbb{E}\,L(X \mid F_n) - \mathbb{E}\,L(X \mid F_n \oplus \Delta)}_{\text{travail éliminé}}
```

**et** $\Delta$ passe la vérification (tests, CI, approbation humaine là où le risque
l'exige).

La première condition dit quand apprendre. La seconde dit que n'entre dans le ruban que ce
qui a été vérifié. **Ce qui n'a pas été fusionné n'a pas changé $F$ :** découverte sans
livraison, c'est de l'entropie différée.

### 5.4 Les règles de la maison comme conséquences

**R1 · « Fait à la main deux fois ? La seconde aurait dû être du code. »**
Soit une procédure qui coûte $\ell$ bits à décrire par un humain, et qui apparaît $k$ fois.
Sans règle, elle coûte $k\ell$. En règle, elle coûte $\ell + r$ une fois ($r$ = surcoût de
nommage, de test et d'intégration) plus $c$ par occurrence ($c$ = le coût d'invoquer la
règle). La règle est rentable quand

```math
k\ell \;>\; \ell + r + kc
\quad\Longleftrightarrow\quad
k \;>\; \frac{\ell + r}{\ell - c}.
```

Quand $`r, c \ll \ell`$, le seuil tend vers $`1^{+}`$ : **dès la deuxième occurrence, cela
vaut la peine.** La règle empirique de la maison est le seuil de l'inégalité.

**R2 · « On demande du pain ? Construisez la boulangerie. »**
Une règle qui couvre la **classe** des demandes a un $k$ égal au nombre attendu d'instances
futures de la classe, pas 1. Généraliser, c'est maximiser le membre de droite du §5.3.

**R3 · « Le resort sans clients. »**
Si le nombre attendu d'instances est petit, $`L(F \oplus \Delta) - L(F)`$ dépasse le
travail éliminé et la mutation doit être **rejetée**. C'est du surapprentissage : le ruban a
grandi plus que la réalité qu'il explique. Le MDL le pénalise de lui-même.

**R4 · « On ne coud pas une pièce neuve sur un vieil habit. »**
Empiler des exceptions augmente $`L(X \mid F)`$ sans réduire $L(F)$. Réécrire la forme peut
diminuer les deux termes à la fois, et alors tout rapiéçage est dominé.

### 5.5 Découvrir coûte cher, vérifier coûte peu

Trouver $\Delta$ est une recherche : chère, pleine d'essais, faite par des agents. Vérifier
$\Delta$ est un contrôle : bon marché, fait par les tests, la CI et l'approbation. C'est
l'asymétrie de NP (trouver le témoin est difficile ; le vérifier est facile) utilisée comme
**cap d'ingénierie, non comme théorème sur P et NP**. Le modèle de coût de la Phase 1 le
rend précis :

```math
C_{\text{total}}(N) \;\le\; D \cdot S_{\max} \;+\; N \cdot V_{\max},
```

où $N$ est le nombre de tâches, $D$ le nombre de tâches **distinctes**, $S$ le coût de
recherche et $V$ celui de vérification. Si $D$ croît plus lentement que $N$, le coût par
tâche tend vers le coût de vérifier : **$`O(n) \to O(1)`$ amorti.**

---

## 6. L'âme : l'identité, c'est le journal

L'état de James est le pli (*fold*) d'une fonction de transition pure sur le journal
d'événements :

```math
S_n = \operatorname{foldl}(\delta,\, S_0,\, [e_1, \dots, e_n]).
```

Si $\delta$ est déterministe, deux corps quelconques qui rejouent le même journal arrivent
au même état. L'identité vit dans le journal et dans le ruban, pas dans l'hôte. Avec
l'invariance (§4.2), c'est la forme mathématique de la loi du système :
**`rm -rf <n'importe-quel-hôte>` ne peut pas détruire James.**

---

## 7. Conclusion

En assemblant les pièces :

1. La réalité de l'opération a une description minimale, $K(X)$. **(Kolmogorov)**
2. Elle ne dépend pas du moteur, à une constante près. **(invariance)**
3. Elle n'est jamais atteinte avec certitude, seulement approchée par le haut.
   **(incalculabilité)**
4. L'approcher coûte de l'énergie, et le coût baisse avec ce que l'on sait déjà.
   **(Landauer, Wolf)**
5. Une machine qui garde sa description hors d'elle et évolue en l'éditant peut croître en
   complexité sans limite. **(von Neumann)**
6. James est cette machine, qui minimise $`L(F) + L(X \mid F)`$. **(modèle)**

La question *l'entropie peut-elle être inversée ?* reçoit, localement, une réponse
d'ingénieur : **oui, un bit à la fois, en payant en calcul et en gardant ce qui a été appris
pour que le bit suivant coûte moins.** Et elle ne finit jamais, parce que le minimum est
incalculable.

---

## 8. Tableau d'honnêteté

| Affirmation | Statut |
|---|---|
| Coût minimal d'effacement $`k_B T \ln 2`$ par bit | **théorème** (Landauer ; formulation précise avec hypothèses, voir Norton) |
| Coût d'effacement proportionnel à la compression, étant donnée une connaissance préalable | **théorème** (Wolf), utilisé ici de façon informelle |
| Constructeur universel avec ruban à double usage | **théorème** (von Neumann ; implémenté dans un automate cellulaire) |
| $K$ incalculable ; invariance à une constante près | **théorèmes** (Kolmogorov, Chaitin, Solomonoff) |
| Factory ↔ constructeur/copieur/contrôle/ruban | **correspondance** d'architecture |
| James minimise $`L(F) + L(X \mid F)`$ | **modèle** proposé dans ce document |
| R1–R4 dérivées de la règle de mise à jour | **modèle** (dérivation à l'intérieur du modèle) |
| Le coût opérationnel baisse à mesure que $F$ compresse $X$ | **hypothèse**, à mesurer en Phase 2 |
| Wolf ↔ coût opérationnel réel de l'entreprise | **analogie**, non identité physique |

**Frontière explicite :** rien ici ne prouve que l'entreprise fonctionne. Les théorèmes
valent pour les modèles ; la Phase 2 existe pour mesurer si le système se comporte comme le
modèle.

---

## 9. Vers la Phase 1 (Lean 4)

Trois affirmations sont assez petites pour être prouvées sur des modèles formels :

| Pilier | Énoncé (informel) | Déclaration Lean dans ce dépôt |
|---|---|---|
| **Connaissance** · amortissement | Pour toute suite de $N$ tâches dont $D$ distinctes, avec une base de connaissance monotone, $`C_{\text{total}} \le D\,S_{\max} + N\,V_{\max}`$. | [`James.Conhecimento.amortizacao`](JamesTheorems/Conhecimento.lean#L119) |
| **Sécurité** · garde | Dans tout état atteignable, aucune action critique n'a été exécutée sans approbation enregistrée dans le journal. | [`James.Seguranca.gate`](JamesTheorems/Seguranca.lean#L74) |
| **Âme** · rejeu | Si $\delta$ est pure, deux hôtes qui appliquent le même journal à partir de $`S_0`$ arrivent au même état. | [`James.Alma.replay`](JamesTheorems/Alma.lean#L32) (et [`retomada`](JamesTheorems/Alma.lean#L38), [`revezamento`](JamesTheorems/Alma.lean#L44)) |

Lean lui-même incarne le §5.5 : **trouver la preuve est une recherche coûteuse ; le noyau la
vérifie à bas coût.** Formaliser James en Lean, c'est le système qui se décrit dans le
langage qu'il pratique.

### Ce qui est prouvé ici

Les énoncés ci-dessus sont informels ; ce que le noyau de Lean a vérifié est ceci, pour les
modèles définis dans ce dépôt (pas pour le code de production) :

- **Connaissance.** [`amortizacao`](JamesTheorems/Conhecimento.lean#L119) : pour toute liste
  de tâches `ts`, traitée à partir d'une base vide par
  [`processar`](JamesTheorems/Conhecimento.lean#L27) (recherche la première fois, simple
  vérification quand la tâche est déjà dans la base), la base finale est sans répétition,
  contient exactement les tâches de `ts`, le nombre de recherches est la taille de cette base
  ($D$), et `coût = D · recherche + N · vérification`, avec **égalité**. Le modèle utilise un
  coût fixe de recherche et un coût fixe de vérification
  ([`Custos`](JamesTheorems/Conhecimento.lean#L16)) ; la forme avec $`S_{\max}`$ et
  $`V_{\max}`$ pour des coûts variables est la lecture informelle, pas l'énoncé Lean.
  Corollaire : [`buscas_le`](JamesTheorems/Conhecimento.lean#L134).
- **Sécurité.** [`gate`](JamesTheorems/Seguranca.lean#L74) : pour **tout** journal
  d'événements (y compris écrit par un adversaire), dans l'état `log.foldl passo inicial`,
  toute action critique exécutée a son identifiant parmi les approuvés. La garantie vient de
  [`passo`](JamesTheorems/Seguranca.lean#L31) lui-même, qui ignore une exécution critique non
  approuvée ; l'invariant est [`passo_preserva`](JamesTheorems/Seguranca.lean#L43).
- **Âme.** [`replay`](JamesTheorems/Alma.lean#L32) : deux corps avec la même fonction de pas
  arrivent au même état à partir du même journal, quels que soient leur nom et leur moteur.
  [`retomada`](JamesTheorems/Alma.lean#L38) (reprise) : mourir après l'événement `k` et
  repartir de l'instantané donne le même état. [`revezamento`](JamesTheorems/Alma.lean#L44)
  (relais) : tout découpage du journal entre des corps donne le même état. En Lean toute
  fonction est pure, donc « δ pure » est la forme du modèle, pas une hypothèse de plus.

Sans Mathlib, sans `sorry`, sans `native_decide`. [`Axiomas.lean`](Axiomas.lean) affiche les
axiomes dont dépend chaque théorème : seulement `propext` et `Quot.sound`. Ce sont des
**modèles, pas du code de production** : si le système réel se comporte comme le modèle, les
propriétés valent ; mesurer s'il le fait est la Phase 2.

---

## Références

- Maxwell, J. C. (1871). *Theory of Heat*.
- Szilard, L. (1929). Über die Entropieverminderung in einem thermodynamischen System
  bei Eingriffen intelligenter Wesen. *Z. Phys.* 53.
- Turing, A. M. (1936). On Computable Numbers, with an Application to the
  Entscheidungsproblem.
- Asimov, I. (1956). *The Last Question*.
- Landauer, R. (1961). Irreversibility and Heat Generation in the Computing Process.
  *IBM J. Res. Dev.* 5.
- Solomonoff, R. (1964). A Formal Theory of Inductive Inference.
- Kolmogorov, A. N. (1965). Three Approaches to the Quantitative Definition of
  Information.
- Chaitin, G. (1966, 1969). On the Length of Programs for Computing Finite Binary
  Sequences.
- von Neumann, J.; Burks, A. W. (ed.) (1966). *Theory of Self-Reproducing Automata*.
- Rissanen, J. (1978). Modeling by Shortest Data Description. *Automatica* 14.
- Bennett, C. H. (1982). The Thermodynamics of Computation — a Review. *Int. J. Theor.
  Phys.* 21.
- Li, M.; Vitányi, P. *An Introduction to Kolmogorov Complexity and Its Applications*.
- Vitányi, P.; Li, M. (2000). Minimum Description Length Induction, Bayesianism, and
  Kolmogorov Complexity. *IEEE Trans. Inf. Theory* 46.
- Grünwald, P. (2004). A Tutorial Introduction to the Minimum Description Length
  Principle.
- Norton, J. D. Eaters of the Lotus: Landauer's Principle and the Return of Maxwell's
  Demon.
- Wolf, S. (2017). Landauer's Erasure Principle and Data Compression. *ISIT*.
