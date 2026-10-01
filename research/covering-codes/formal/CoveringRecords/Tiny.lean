import CoveringCodes.Database.ExplicitCode
import CoveringCodes.Database.ProofMode

namespace CoveringRecords
open CoveringCodes CoveringCodes.Database

/-- Test fixture only, separate from the recovered principal artifact. -/
def tinyCode : Finset (QaryWord 2 3) := {![0, 0, 0], ![1, 1, 1]}

def tinyExplicit : ExplicitQaryUpper 2 3 1 2 where
  code := tinyCode
  card_le := by decide
  covers := by
    show ∀ x : QaryWord 2 3,
      ∃ c : QaryWord 2 3, c ∈ tinyCode ∧ hammingDist x c ≤ 1
    covering_decide +kernel

theorem q2_n3_r1_m2 : QaryKUpper 2 3 1 2 := tinyExplicit.toUpper

end CoveringRecords
