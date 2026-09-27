/-!
# Pilar 3 · Alma: a identidade é o log

O estado do James é a dobra de uma função de transição pura sobre o log de
eventos. Os teoremas abaixo valem para **qualquer** tipo de estado, qualquer
tipo de evento e qualquer transição: são propriedades da forma, não de uma
implementação.

* `replay`: dois corpos que aplicam o mesmo log chegam ao mesmo estado.
* `retomada`: um corpo pode morrer em qualquer ponto; outro corpo, partindo do
  snapshot, chega ao mesmo lugar que um corpo que nunca morreu.
* `revezamento`: o log pode ser dividido entre qualquer número de corpos.

`rm -rf <qualquer-host>` não destrói o James, desde que o log e a fita sobrevivam.
-/

namespace James.Alma

variable {Estado Evento : Type}

/-- Um corpo: qualquer host, com qualquer característica, que roda a mesma transição. -/
structure Corpo (Estado Evento : Type) where
  nome : String
  motor : String
  passo : Estado → Evento → Estado

/-- O estado que um corpo alcança ao reproduzir um log. -/
def reproduzir (c : Corpo Estado Evento) (s₀ : Estado) (log : List Evento) : Estado :=
  log.foldl c.passo s₀

/-- **Replay.** Host não é identidade: nome e motor não importam, só a transição. -/
theorem replay (c₁ c₂ : Corpo Estado Evento) (h : c₁.passo = c₂.passo)
    (s₀ : Estado) (log : List Evento) :
    reproduzir c₁ s₀ log = reproduzir c₂ s₀ log := by
  simp [reproduzir, h]

/-- **Retomada.** Morrer no evento `k` e voltar do snapshot dá o mesmo estado. -/
theorem retomada (δ : Estado → Evento → Estado) (s₀ : Estado)
    (log : List Evento) (k : Nat) :
    (log.drop k).foldl δ ((log.take k).foldl δ s₀) = log.foldl δ s₀ := by
  rw [← List.foldl_append, List.take_append_drop]

/-- **Revezamento.** Qualquer divisão do log entre corpos dá o mesmo resultado. -/
theorem revezamento (δ : Estado → Evento → Estado) (s₀ : Estado)
    (partes : List (List Evento)) :
    partes.foldl (fun s l => l.foldl δ s) s₀ = partes.flatten.foldl δ s₀ := by
  induction partes generalizing s₀ with
  | nil => rfl
  | cons l ls ih => simp [List.flatten, List.foldl_append, ih]

end James.Alma
