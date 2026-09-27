/-!
# Pilar 1 · Conhecimento: a amortização

Cada tarefa custa `busca + verificação` na primeira vez e só `verificação`
quando já está na base de conhecimento. O teorema principal diz que, partindo
de uma base vazia, o número de buscas é **exatamente** o número de tarefas
distintas, e o número de verificações é o número total de tarefas.
Logo: `custo = D · busca + N · verificação`.
-/

namespace James.Conhecimento

variable {α : Type} [DecidableEq α]

/-- Custo de encontrar uma solução nova e custo de verificar uma solução. -/
structure Custos where
  busca : Nat
  verificacao : Nat

/-- Resultado de processar uma fila de tarefas. -/
structure Relatorio (α : Type) where
  buscas : Nat
  verificacoes : Nat
  base : List α

/-- Processa as tarefas em ordem, aprendendo com cada busca. -/
def processar : List α → List α → Relatorio α
  | base, [] => ⟨0, 0, base⟩
  | base, t :: ts =>
    if t ∈ base then
      let r := processar base ts
      ⟨r.buscas, r.verificacoes + 1, r.base⟩
    else
      let r := processar (t :: base) ts
      ⟨r.buscas + 1, r.verificacoes + 1, r.base⟩

/-- Custo total de um relatório. -/
def custo (c : Custos) (r : Relatorio α) : Nat :=
  r.buscas * c.busca + r.verificacoes * c.verificacao

/-- Lista sem repetição. -/
def Distintos : List α → Prop
  | [] => True
  | x :: xs => x ∉ xs ∧ Distintos xs

/-- Toda tarefa é verificada exatamente uma vez. -/
theorem verificacoes_eq (base ts : List α) :
    (processar base ts).verificacoes = ts.length := by
  induction ts generalizing base with
  | nil => rfl
  | cons t ts ih =>
    unfold processar
    split <;> simp [ih]

/-- Cada busca acrescenta exatamente um item à base. -/
theorem buscas_mais_base (base ts : List α) :
    (processar base ts).buscas + base.length = (processar base ts).base.length := by
  induction ts generalizing base with
  | nil => simp [processar]
  | cons t ts ih =>
    unfold processar
    split
    · exact ih base
    · have := ih (t :: base)
      simp at this ⊢
      omega

/-- A base final contém exatamente a base inicial e as tarefas vistas. -/
theorem mem_base (base ts : List α) (x : α) :
    x ∈ (processar base ts).base ↔ x ∈ base ∨ x ∈ ts := by
  induction ts generalizing base with
  | nil => simp [processar]
  | cons t ts ih =>
    unfold processar
    split
    · next h =>
      rw [ih]
      constructor
      · rintro (h1 | h1)
        · exact Or.inl h1
        · exact Or.inr (List.mem_cons_of_mem _ h1)
      · rintro (h1 | h1)
        · exact Or.inl h1
        · rcases List.mem_cons.mp h1 with rfl | h2
          · exact Or.inl h
          · exact Or.inr h2
    · rw [ih]
      simp only [List.mem_cons]
      constructor
      · rintro ((rfl | h1) | h1)
        · exact Or.inr (Or.inl rfl)
        · exact Or.inl h1
        · exact Or.inr (Or.inr h1)
      · rintro (h1 | (rfl | h1))
        · exact Or.inl (Or.inr h1)
        · exact Or.inl (Or.inl rfl)
        · exact Or.inr h1

/-- A base nunca aprende a mesma coisa duas vezes. -/
theorem distintos_base (base ts : List α) (h : Distintos base) :
    Distintos (processar base ts).base := by
  induction ts generalizing base with
  | nil => simpa [processar] using h
  | cons t ts ih =>
    unfold processar
    split
    · exact ih base h
    · next ht => exact ih (t :: base) ⟨ht, h⟩

/--
**Teorema da amortização.** Partindo de uma base vazia:

* a base final não tem repetições e contém exatamente as tarefas distintas vistas;
* o número de buscas é o tamanho dessa base, isto é, o número `D` de tarefas distintas;
* o custo total é `D · busca + N · verificação`.

Se `D` cresce mais devagar que `N`, o custo por tarefa tende ao custo de verificar.
-/
theorem amortizacao (c : Custos) (ts : List α) :
    let r := processar [] ts
    Distintos r.base ∧
    (∀ x, x ∈ r.base ↔ x ∈ ts) ∧
    r.buscas = r.base.length ∧
    custo c r = r.base.length * c.busca + ts.length * c.verificacao := by
  intro r
  have hb := buscas_mais_base ([] : List α) ts
  have hv := verificacoes_eq ([] : List α) ts
  simp at hb
  refine ⟨distintos_base [] ts trivial, ?_, hb, ?_⟩
  · intro x; simpa using mem_base [] ts x
  · simp [custo, r, hb, hv]

/-- Corolário: nunca se busca mais do que o número de tarefas. -/
theorem buscas_le (base ts : List α) : (processar base ts).buscas ≤ ts.length := by
  induction ts generalizing base with
  | nil => simp [processar]
  | cons t ts ih =>
    unfold processar
    split
    · have := ih base; simp; omega
    · have := ih (t :: base); simp; omega

end James.Conhecimento
