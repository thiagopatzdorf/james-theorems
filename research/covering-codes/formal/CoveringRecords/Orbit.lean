import CoveringCodes.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.ReduceModChar

namespace CoveringRecords.Orbit
open CoveringCodes

abbrev Word := Fin 9 → ZMod 7
abbrev Coeff := Fin 3 → ZMod 7

def matrix : Fin 3 → Fin 9 → ZMod 7 :=
  ![![1,1,1,1,1,1,1,1,1], ![0,2,3,2,3,6,0,1,1], ![0,5,3,0,6,4,4,3,5]]

def linear (a : Coeff) : Word := fun j => ∑ i, a i * matrix i j

theorem linear_add (a b : Coeff) : linear (a+b) = linear a + linear b := by
  funext j
  simp [linear, add_mul, Finset.sum_add_distrib]

/-- Modular coordinate translation preserves upstream Hamming distance. -/
theorem hamming_translate (x c l : Word) :
    hammingDist (x+l) (c+l) = hammingDist x c := by
  unfold hammingDist
  congr 1
  ext i
  simp

def coefficients (x : Word) : Coeff :=
  ![x 0, 2*(x 1-x 0)+6*(x 2-x 0), 5*(x 1-x 0)+6*(x 2-x 0)]

def normalize (x : Word) : Word := x - linear (coefficients x)

theorem normalize_prefix (x : Word) (i : Fin 3) :
    normalize x ⟨i.val, by omega⟩ = 0 := by
  fin_cases i <;> simp [normalize, coefficients, linear, matrix, Fin.sum_univ_succ]
  all_goals ring_nf
  all_goals reduce_mod_char

theorem coefficients_linear (a : Coeff) : coefficients (linear a) = a := by
  funext i
  fin_cases i <;> simp [coefficients, linear, matrix, Fin.sum_univ_succ]
  all_goals ring_nf
  all_goals reduce_mod_char

theorem linear_injective : Function.Injective linear := by
  intro a b h
  simpa [coefficients_linear] using congrArg coefficients h

theorem decomposition (x : Word) : normalize x + linear (coefficients x) = x := by
  simp [normalize]

/-- Every translated base witness stays in the same full coset. -/
def coset (r : Word) : Finset Word := Finset.univ.image (fun a : Coeff => r + linear a)

theorem coset_transport (r c : Word) (b : Coeff) (hc : c ∈ coset r) :
    c + linear b ∈ coset r := by
  classical
  obtain ⟨a, _, rfl⟩ := Finset.mem_image.mp hc
  apply Finset.mem_image.mpr
  refine ⟨a+b, Finset.mem_univ _, ?_⟩
  simp [linear_add, add_assoc]

theorem coset_card (r : Word) : (coset r).card = 343 := by
  classical
  unfold coset
  rw [Finset.card_image_of_injective _ (by
    intro a b h
    exact linear_injective (add_left_cancel h))]
  simp only [Finset.card_univ]
  change Fintype.card (Fin 3 → Fin 7) = 343
  simp

/-- ZMod 7 is definitionally the alphabet Fin 7 used upstream. -/
example : Word = QaryWord 7 9 := rfl

theorem cosets_transport (reps : Finset Word) (c : Word) (b : Coeff)
    (hc : c ∈ reps.biUnion coset) : c + linear b ∈ reps.biUnion coset := by
  classical
  obtain ⟨r, hr, hc⟩ := Finset.mem_biUnion.mp hc
  exact Finset.mem_biUnion.mpr ⟨r, hr, coset_transport r c b hc⟩

theorem transport_normalization (x c : Word) :
    hammingDist x (c + linear (coefficients x)) = hammingDist (normalize x) c := by
  have h := hamming_translate (normalize x) c (linear (coefficients x))
  simpa only [decomposition] using h

end CoveringRecords.Orbit
