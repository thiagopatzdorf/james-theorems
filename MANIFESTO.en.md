<div align="center">

[Português](MANIFESTO.md) · **English** · [Français](MANIFESTO.fr.md)

</div>

# James's mathematical manifesto

> **Phase 0 · technical version.** This document formalizes James's philosophy with the
> tools of the physics of information, computability theory and algorithmic information
> theory. Every claim is classified in [§8](#8-honesty-table) as a **theorem** (a result
> from the literature), a **correspondence** (an architectural mapping), a **model** (a
> formalization proposed here) or a **hypothesis** (to be measured).
>
> *Translated from the Portuguese original, [MANIFESTO.md](MANIFESTO.md), which prevails.*

> [!NOTE]
> **What this repository proves.** Three statements from §9, about **models** written in Lean 4,
> checked by the kernel, with no `sorry` and only the standard axioms. It is not a proof about
> production code. What each theorem actually states is in [What is proved here](#what-is-proved-here).

---

## 0. Summary

The question that guides the system is:

> **What is the minimum amount of data from reality needed to represent reality itself?**

It has a name: **Kolmogorov complexity**. Three facts about it organize everything:

1. **It exists, but it is uncomputable.** No procedure guarantees it has found the minimal
   description; every program written is only an upper bound. The work of compressing
   reality is, by construction, an endless loop.
2. **It does not depend on the machine**, up to a constant (the invariance theorem). The
   identity of a description does not live in the hardware that runs it.
3. **Compressing costs energy, and prior knowledge makes it cheaper** (Landauer, Bennett,
   Wolf). Reducing local entropy is possible; the price is information.

James is the engineering of these three facts: a **universal machine** (von Neumann) that
reads a versioned **tape** and works to minimize, continuously,

```math
\boxed{\;L(F) \;+\; L(X \mid F)\;}
```

where $F$ is the tape (everything the system knows) and $X$ is the reality of the
operation. The second term is, literally, **the work that still depends on a human
remembering**.

<p align="center">
  <img alt="James's equation: L(F) + L(X | F). L(F) is the size of the tape, everything the system knows; L(X | F) is what the tape does not explain, the work that still depends on a human remembering. Diagram labels in Portuguese." src="docs/assets/equacao.svg" width="90%">
</p>

---

## 1. The question

In the story *The Last Question* (Asimov, 1956), humanity asks a computer, for billions of
years, whether entropy can be reversed. The answer is always that the data are
insufficient. In the end, the answer is an act: *let there be light*.

This system is not about the entropy of the universe. It is about the **local entropy** of
an operation: uncertainty, ambiguity, exceptions, rules that live in someone's head.

```math
\text{chaos} \to \text{structure}, \quad
\text{implicit} \to \text{explicit}, \quad
\text{exception} \to \text{rule}, \quad
\text{experience} \to \text{memory}.
```

The thesis is that each of these arrows is a **compression**, and that compression has a
theory, a physical cost and a limit.

---

## 2. The physics: reversing entropy costs information

### 2.1 Maxwell's demon

Maxwell (1871) imagined an agent that separates fast molecules from slow ones, reducing the
entropy of a gas without spending work, which would violate the second law. The resolution
took a century (Szilard 1929, Landauer 1961, Bennett 1982): the demon **measures and
memorizes**, and to operate in a cycle it must **erase its memory**.

### 2.2 Landauer's principle

Erasing one bit of information in an environment at temperature $T$ dissipates at least

```math
W_{\text{erase}} \;\ge\; k_B\, T \ln 2 \quad \text{per bit.}
```

The demon's gain is paid for by the erasure. Reducing local entropy is possible; the price
is paid in information processed and discarded.

### 2.3 Wolf's reformulation

Wolf showed that the cost of erasing a sequence $x$ is not proportional to its length
$`|x|`$, but to the length of its **best compression**; and that, if the demon already has
prior knowledge $y$ about $x$, what counts is the **algorithmic** power of that knowledge.
Informally:

```math
W_{\text{erase}}(x \mid y) \;\approx\; k_B T \ln 2 \cdot K(x \mid y).
```

**Reading for James:** accumulated knowledge ($y$) reduces the physical cost of dealing
with reality ($x$). The phrase *computation → knowledge → less computation* has a
thermodynamic analogue.

---

## 3. The universal machine

### 3.1 Turing

There is a machine $U$ that, given the description $`\langle M \rangle`$ of any machine $M$
and an input $w$, simulates $M$ on $w$:

```math
U(\langle M \rangle, w) = M(w).
```

Behavior leaves the hardware and becomes data.

### 3.2 Von Neumann: constructor, copier, control and tape

Von Neumann (1966, posthumous) asked what it takes for a machine to build another,
including itself, **without losing the ability to become more complex**. His answer has
four parts:

| Component | Function |
|---|---|
| $A$ · universal constructor | given a description $`\Phi(X)`$, builds $X$ |
| $B$ · copier | copies $`\Phi(X)`$ **without interpreting it** |
| $C$ · control | coordinates $A$ and $B$ |
| $`\Phi`$ · tape | the description, **outside** the constructor |

Fed its own description, $`\Phi(A+B+C)`$, the system reproduces itself. Three observations
make the result matter:

1. **The tape has a dual use:** it is *interpreted* to build and *copied without
   interpretation* for the offspring. Von Neumann separated transcription from
   construction before the structure of DNA was discovered.
2. **A description cannot contain a copy of itself of the same size**, just as a container
   cannot hold another one equal to it. That is why the copier exists separately.
3. **Evolution happens on the tape, not in the machine.** Mutations in $`\Phi`$ produce
   different machines, and that is what allows complexity to grow without limit.

### 3.3 Correspondence with the Factory

| Von Neumann | Factory | Artifact |
|---|---|---|
| $A$ · constructor | core | `factory-maquina.py` |
| $B$ · copier | replication | `git` |
| $C$ · control | coordination | James / Maestro / queue |
| $`\Phi`$ · tape | versioned description | `factory.manifest.json`, code, tests, `CLAUDE.md`, memory |
| cellular space | substrate | any host with processes, disk, network, secrets and a scheduler |
| $D$ · arbitrary automaton | product | MyBagCenter, websites, integrations |

**Consequence:** James does not evolve by changing hosts. **It evolves by editing the
tape.** Every merged PR is a mutation of $`\Phi`$.

<p align="center">
  <img alt="The machine and the tape: von Neumann on the left (A universal constructor, B copier, C control, Φ tape) and the Factory on the right (core, replication, coordination, versioned description); below, the tape as a strip of cells, one cell in gold marking a mutation, a merged PR. Diagram labels in Portuguese." src="docs/assets/fita-von-neumann.svg" width="90%">
</p>

---

## 4. The minimum: Kolmogorov complexity

### 4.1 Definition

Fix a universal machine $U$. The complexity of a finite object $x$ is the length of the
shortest program that produces it:

```math
K_U(x) = \min \{\, |p| \;:\; U(p) = x \,\}.
```

With side information $y$ available for free:

```math
K_U(x \mid y) = \min \{\, |p| \;:\; U(p, y) = x \,\}.
```

**This is the formal answer to the question of §0.** The minimum data needed to represent
$x$ is $K(x)$; given what is already known ($y$), it is $`K(x \mid y)`$.

### 4.2 Invariance: the host is not the identity

For any two universal machines $U$ and $V$ there is a constant $`c_{UV}`$, independent of
$x$, such that

```math
\left|\, K_U(x) - K_V(x) \,\right| \;\le\; c_{UV}.
```

**Reading for James:** Claude, Codex, Qwen and Nemotron are different universal machines.
The minimal description of the operation is the same on all of them, up to a constant that
does not grow with the operation. **The identity is the description; the engine is the
constant.**

### 4.3 Uncomputability: the endless loop

$K$ is not computable. Every program $p$ with $U(p) = x$ proves that $`K(x) \le |p|`$, but
no general procedure proves that no smaller $p'$ exists.

**Reading for James:** the system can only lower **upper bounds**. There is no state in
which it knows it has finished compressing. It is the story's "insufficient data", as a
theorem, and it is why James is a loop and not a project.

### 4.4 To compress is to understand

Solomonoff (1964) showed that weighting hypotheses by $`2^{-K(h)}`$ gives an optimal theory
of induction in a precise sense: the shortest description that explains the data is the
best prediction. Compressing is not just saving bytes; it is modeling structure.

### 4.5 Relation to Shannon

For random sources, the expected complexity per symbol converges to the Shannon entropy
$H$. Entropy is average compressibility; Kolmogorov is the compressibility of **one**
object. The company's operation is a single object, so the right measure is the second.

---

## 5. James's equation

### 5.1 Two-part minimum description length (MDL)

Since $K$ is uncomputable, practice uses the MDL principle (Rissanen, 1978): the best
explanation of data $X$ is the model $F$ that minimizes

```math
L(F) + L(X \mid F),
```

the size of the model plus the size of the data encoded with the model.

### 5.2 The mapping **[model]**

- $`X_{1:n}`$: the history of the operation up to time $n$ (orders, events, customer
  requests, incidents).
- $`F_n`$: the tape at time $n$ (code, tests, manifest, rules, memory).
- $`L(F_n)`$: the size of what the system knows.
- $`L(X_{n+1} \mid F_n)`$: what the tape does **not** explain in the next period. It is the
  exception, the judgment made again, the manual step, **the work that depends on someone
  remembering.**

James's objective is

```math
F^\star = \arg\min_F \; L(F) + \mathbb{E}\big[\, L(X \mid F) \,\big].
```

### 5.3 The update rule

A mutation $\Delta$ of the tape ($`F_{n+1} = F_n \oplus \Delta`$) is accepted if and only
if:

```math
\underbrace{L(F_n \oplus \Delta) - L(F_n)}_{\text{cost of learning}}
\;<\;
\underbrace{\mathbb{E}\,L(X \mid F_n) - \mathbb{E}\,L(X \mid F_n \oplus \Delta)}_{\text{work eliminated}}
```

**and** $\Delta$ passes verification (tests, CI, human approval where the risk requires it).

The first condition says when to learn. The second says that only what was verified enters
the tape. **What was not merged did not change $F$:** discovery without delivery is
postponed entropy.

### 5.4 The house rules as consequences

**R1 · "Did it by hand twice? The second time should have been code."**
Let a procedure cost $\ell$ bits to be described by a human, and appear $k$ times. Without
a rule, it costs $k\ell$. As a rule, it costs $\ell + r$ once ($r$ = the overhead of naming,
testing and integration) plus $c$ per occurrence ($c$ = the cost of invoking the rule). The
rule pays off when

```math
k\ell \;>\; \ell + r + kc
\quad\Longleftrightarrow\quad
k \;>\; \frac{\ell + r}{\ell - c}.
```

When $`r, c \ll \ell`$, the threshold tends to $`1^{+}`$: **from the second occurrence on,
it is worth it.** The house's rule of thumb is the threshold of the inequality.

**R2 · "Asked for bread? Build the bakery."**
A rule that covers the **class** of requests has $k$ equal to the expected number of future
instances of the class, not 1. Generalizing is maximizing the right-hand side of §5.3.

**R3 · "The resort with no guests."**
If the expected number of instances is small, $`L(F \oplus \Delta) - L(F)`$ exceeds the
work eliminated and the mutation must be **rejected**. It is overfitting: the tape grew more
than the reality it explains. MDL penalizes this on its own.

**R4 · "No one sews new cloth onto an old garment."**
Piling up exceptions increases $`L(X \mid F)`$ without reducing $L(F)$. Rewriting the form
can shrink both terms at once, and then any patch is dominated.

### 5.5 Discovering is expensive, verifying is cheap

Finding $\Delta$ is search: expensive, full of trial, done by agents. Verifying $\Delta$ is
checking: cheap, done by tests, CI and approval. It is the asymmetry of NP (finding the
witness is hard; checking it is easy) used as an **engineering north star, not as a theorem
about P and NP**. The Phase 1 cost model makes this precise:

```math
C_{\text{total}}(N) \;\le\; D \cdot S_{\max} \;+\; N \cdot V_{\max},
```

where $N$ is the number of tasks, $D$ the number of **distinct** tasks, $S$ the cost of
search and $V$ the cost of verification. If $D$ grows more slowly than $N$, the cost per
task tends to the cost of verifying: **$`O(n) \to O(1)`$ amortized.**

---

## 6. The soul: identity is the log

James's state is the fold of a pure transition function over the event log:

```math
S_n = \operatorname{foldl}(\delta,\, S_0,\, [e_1, \dots, e_n]).
```

If $\delta$ is deterministic, any two bodies that replay the same log reach the same state.
Identity lives in the log and in the tape, not in the host. Together with invariance
(§4.2), this is the mathematical form of the system's law: **`rm -rf <any-host>` cannot
destroy James.**

---

## 7. Closing

Putting the pieces together:

1. The reality of the operation has a minimal description, $K(X)$. **(Kolmogorov)**
2. It does not depend on the engine, up to a constant. **(invariance)**
3. It is never reached with certainty, only approximated from above. **(uncomputability)**
4. Approximating it costs energy, and the cost falls with what is already known.
   **(Landauer, Wolf)**
5. A machine that keeps its description outside itself and evolves by editing it can grow
   in complexity without limit. **(von Neumann)**
6. James is that machine, minimizing $`L(F) + L(X \mid F)`$. **(model)**

The question *can entropy be reversed?* receives, locally, an engineering answer: **yes,
one bit at a time, paying in computation and keeping what was learned so that the next bit
costs less.** And it never ends, because the minimum is uncomputable.

---

## 8. Honesty table

| Claim | Status |
|---|---|
| Minimum erasure cost $`k_B T \ln 2`$ per bit | **theorem** (Landauer; precise formulation with hypotheses, see Norton) |
| Erasure cost proportional to compression, given prior knowledge | **theorem** (Wolf), used here informally |
| Universal constructor with a dual-use tape | **theorem** (von Neumann; implemented in a cellular automaton) |
| $K$ uncomputable; invariance up to a constant | **theorems** (Kolmogorov, Chaitin, Solomonoff) |
| Factory ↔ constructor/copier/control/tape | architectural **correspondence** |
| James minimizes $`L(F) + L(X \mid F)`$ | **model** proposed in this document |
| R1–R4 derived from the update rule | **model** (derivation within the model) |
| Operational cost falls as $F$ compresses $X$ | **hypothesis**, to be measured in Phase 2 |
| Wolf ↔ the company's real operational cost | **analogy**, not physical identity |

**Explicit boundary:** nothing here proves that the company works. The theorems hold for
the models; Phase 2 exists to measure whether the system behaves like the model.

---

## 9. Toward Phase 1 (Lean 4)

Three claims are small enough to be proved about formal models:

| Pillar | Statement (informal) | Lean declaration in this repository |
|---|---|---|
| **Knowledge** · amortization | For any sequence of $N$ tasks with $D$ distinct ones, with a monotone knowledge base, $`C_{\text{total}} \le D\,S_{\max} + N\,V_{\max}`$. | [`James.Conhecimento.amortizacao`](JamesTheorems/Conhecimento.lean#L119) |
| **Safety** · gate | In every reachable state, no critical action was executed without an approval recorded in the log. | [`James.Seguranca.gate`](JamesTheorems/Seguranca.lean#L74) |
| **Soul** · replay | If $\delta$ is pure, two hosts that apply the same log from $`S_0`$ reach the same state. | [`James.Alma.replay`](JamesTheorems/Alma.lean#L32) (and [`retomada`](JamesTheorems/Alma.lean#L38), [`revezamento`](JamesTheorems/Alma.lean#L44)) |

Lean itself embodies §5.5: **finding the proof is expensive search; the kernel checks it
cheaply.** Formalizing James in Lean is the system describing itself in the language it
practices.

### What is proved here

The statements above are informal; what the Lean kernel checked is this, for the models
defined in this repository (not for production code):

- **Knowledge.** [`amortizacao`](JamesTheorems/Conhecimento.lean#L119): for every task list
  `ts`, processed from an empty base by [`processar`](JamesTheorems/Conhecimento.lean#L27)
  (search the first time, only verification once the task is in the base), the final base
  has no repetitions, contains exactly the tasks of `ts`, the number of searches is the size of
  that base ($D$), and `cost = D · search + N · verification`, as an **equality**. The model
  uses one fixed search cost and one fixed verification cost
  ([`Custos`](JamesTheorems/Conhecimento.lean#L16)); the form with $`S_{\max}`$ and
  $`V_{\max}`$ for varying costs is the informal reading, not the Lean statement. Corollary:
  [`buscas_le`](JamesTheorems/Conhecimento.lean#L134).
- **Safety.** [`gate`](JamesTheorems/Seguranca.lean#L74): for **every** event log (including
  one written by an adversary), in the state `log.foldl passo inicial` every executed critical
  action has its identifier among the approved ones. The guarantee comes from
  [`passo`](JamesTheorems/Seguranca.lean#L31) itself, which ignores an unapproved critical
  execution; the invariant is [`passo_preserva`](JamesTheorems/Seguranca.lean#L43).
- **Soul.** [`replay`](JamesTheorems/Alma.lean#L32): two bodies with the same step function
  reach the same state from the same log, whatever their name and engine.
  [`retomada`](JamesTheorems/Alma.lean#L38) (resumption): dying after event `k` and continuing
  from the snapshot gives the same state. [`revezamento`](JamesTheorems/Alma.lean#L44) (relay):
  any split of the log among bodies gives the same state. In Lean every function is pure, so
  "δ is pure" is the shape of the model, not an extra hypothesis.

No Mathlib, no `sorry`, no `native_decide`. [`Axiomas.lean`](Axiomas.lean) prints the axioms
each theorem depends on: only `propext` and `Quot.sound`. These are **models, not production
code**: if the real system behaves like the model, the properties hold; measuring whether it
does is Phase 2.

---

## References

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
