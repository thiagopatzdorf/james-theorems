import CoveringRecords.Orbit
import CoveringRecords.PrincipalCode

namespace CoveringRecords.CompactReplay
open CoveringCodes CoveringCodes.Database
open CoveringRecords.Orbit

/-- Partition bridge; finite-data hypotheses are not asserted here. -/
theorem covers_of_partition (C : Finset Word) (reps : Finset Word)
    (exceptional : Word → Prop) (R : Nat)
    (baseIncluded : reps.biUnion coset ⊆ C)
    (quotient : ∀ x : Word, ¬ exceptional (normalize x) →
      ∃ c ∈ reps.biUnion coset, hammingDist (normalize x) c ≤ R)
    (exceptions : ∀ x : Word, exceptional (normalize x) →
      ∃ c ∈ C, hammingDist x c ≤ R) : CoversFinset C R := by
  classical
  intro x
  by_cases hx : exceptional (normalize x)
  · exact exceptions x hx
  · obtain ⟨c, hc, hd⟩ := quotient x hx
    refine ⟨c + linear (coefficients x), baseIncluded (cosets_transport reps c _ hc), ?_⟩
    simpa only [transport_normalization] using hd

/-- Conditional adapter, not an unconditional principal upper bound. -/
theorem principal_upper_of_partition (reps : Finset Word)
    (exceptional : Word → Prop)
    (baseIncluded : reps.biUnion coset ⊆ principalCode)
    (quotient : ∀ x : Word, ¬ exceptional (normalize x) →
      ∃ c ∈ reps.biUnion coset, hammingDist (normalize x) c ≤ 4)
    (exceptions : ∀ x : Word, exceptional (normalize x) →
      ∃ c ∈ principalCode, hammingDist x c ≤ 4) : QaryKUpper 7 9 4 1351 := by
  exact ⟨principalCode, principal_card_le,
    covers_of_partition principalCode reps exceptional 4 baseIncluded quotient exceptions⟩

theorem original_first_word_member : (![0,0,0,0,0,0,0,0,0] : Word) ∈ principalCode := by
  apply List.mem_toFinset.mpr
  exact List.mem_cons_self

theorem original_first_word_covers_pilot :
    hammingDist (![0,0,0,0,0,0,0,0,0] : Word) (![0,0,0,0,0,0,0,0,0] : Word) ≤ 4 := by
  decide

#print axioms covers_of_partition
#print axioms principal_upper_of_partition
#print axioms original_first_word_member
#print axioms original_first_word_covers_pilot
end CoveringRecords.CompactReplay
