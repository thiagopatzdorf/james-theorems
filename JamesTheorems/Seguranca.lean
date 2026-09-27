/-!
# Pilar 2 · Segurança: o gate de aprovação

O James é modelado como uma máquina de estados movida por um log de eventos.
Ações seguras executam direto; ações críticas só executam se já existe uma
aprovação registrada para elas. O teorema diz que, **para qualquer log**,
inclusive um log escrito por um adversário, nenhuma ação crítica aparece como
executada sem a aprovação correspondente.
-/

namespace James.Seguranca

/-- Uma ação, identificada por um número. -/
inductive Acao where
  | segura (id : Nat)
  | critica (id : Nat)
  deriving DecidableEq

/-- O que pode acontecer no log. -/
inductive Evento where
  | aprovar (id : Nat)
  | executar (a : Acao)

structure Estado where
  aprovadas : List Nat
  executadas : List Acao

def inicial : Estado := ⟨[], []⟩

/-- A transição. O gate recusa uma ação crítica não aprovada: o estado não muda. -/
def passo (s : Estado) : Evento → Estado
  | .aprovar id => { s with aprovadas := id :: s.aprovadas }
  | .executar (.segura id) => { s with executadas := .segura id :: s.executadas }
  | .executar (.critica id) =>
    if id ∈ s.aprovadas then { s with executadas := .critica id :: s.executadas }
    else s

/-- A propriedade de segurança. -/
def Seguro (s : Estado) : Prop :=
  ∀ id, Acao.critica id ∈ s.executadas → id ∈ s.aprovadas

/-- Cada passo preserva a segurança. -/
theorem passo_preserva (s : Estado) (e : Evento) (h : Seguro s) :
    Seguro (passo s e) := by
  intro id hid
  cases e with
  | aprovar a =>
    exact List.mem_cons_of_mem _ (h id hid)
  | executar ac =>
    cases ac with
    | segura n =>
      simp [passo] at hid
      exact h id hid
    | critica n =>
      by_cases hn : n ∈ s.aprovadas
      · simp only [passo, hn, ite_true] at hid ⊢
        rcases List.mem_cons.mp hid with heq | hmem
        · cases heq; exact hn
        · exact h id hmem
      · simp only [passo, hn, ite_false] at hid ⊢
        exact h id hid

/-- Segurança se mantém ao longo de qualquer log. -/
theorem seguro_foldl (log : List Evento) (s : Estado) (h : Seguro s) :
    Seguro (log.foldl passo s) := by
  induction log generalizing s with
  | nil => exact h
  | cons e es ih => exact ih _ (passo_preserva s e h)

/--
**Teorema do gate.** Para todo log, no estado alcançado a partir do início,
toda ação crítica executada tem aprovação registrada.
-/
theorem gate (log : List Evento) : Seguro (log.foldl passo inicial) :=
  seguro_foldl log inicial (by intro id h; simp [inicial] at h)

end James.Seguranca
