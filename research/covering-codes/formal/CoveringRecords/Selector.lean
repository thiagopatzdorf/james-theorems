import CoveringCodes.Database.ExplicitCode

namespace CoveringRecords
open CoveringCodes CoveringCodes.Database

/-- Reuse upstream coverage: a checked selector suffices; its generator is untrusted.
This is a generic bridge, not an assertion that any principal selector exists. -/
theorem covers_of_selector {q n R : Nat} (C : Finset (QaryWord q n))
    (choose : QaryWord q n → QaryWord q n)
    (member : ∀ x, choose x ∈ C)
    (near : ∀ x, dist x (choose x) ≤ R) : CoversFinset C R := by
  intro x
  exact ⟨choose x, member x, near x⟩

def explicit_of_selector {q n R M : Nat} (C : Finset (QaryWord q n))
    (card : C.card ≤ M) (choose : QaryWord q n → QaryWord q n)
    (member : ∀ x, choose x ∈ C)
    (near : ∀ x, dist x (choose x) ≤ R) : ExplicitQaryUpper q n R M :=
  { code := C, card_le := card, covers := covers_of_selector C choose member near }

end CoveringRecords
