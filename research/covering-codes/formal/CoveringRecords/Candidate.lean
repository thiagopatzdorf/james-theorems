import CoveringCodes.CoveringNumber
import CoveringCodes.Database.ExplicitCode

namespace CoveringRecords

open CoveringCodes
open CoveringCodes.Database

/--
The exact statement that the principal candidate must eventually prove.
This file deliberately does *not* manufacture the 1351-word witness: the
canonical code and its certificate must be ingested first.
-/
def PrincipalClaim : Prop := QaryKUpper 7 9 4 1351

/--
A generic bridge supplied by Florath's explicit-code interface. Once the
canonical 1351-word code has been converted into `ExplicitQaryUpper`, no
additional mathematical assumption is needed to obtain the advertised bound.
-/
theorem principalClaim_of_explicit
    (E : ExplicitQaryUpper 7 9 4 1351) : PrincipalClaim := by
  exact E.toUpper

/-- Secondary working claims, kept as propositions rather than asserted facts. -/
def Q4N10R4M192 : Prop := QaryKUpper 4 10 4 192
def Q5N7R2M500  : Prop := QaryKUpper 5 7 2 500
def Q5N9R3M1250 : Prop := QaryKUpper 5 9 3 1250
def Q5N10R4M625 : Prop := QaryKUpper 5 10 4 625
def Q5N9R4M250  : Prop := QaryKUpper 5 9 4 250
def Q5N9R5M50   : Prop := QaryKUpper 5 9 5 50
def Q7N8R3M1893 : Prop := QaryKUpper 7 8 3 1893

end CoveringRecords
