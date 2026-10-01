import CoveringCodes.Database.Sources.SphereCovering

/-!
# Cota esférica de Hamming para o alvo principal

A cota de esferas (Hamming) diz que qualquer código que cobre o espaço
q-ário de comprimento `n` com raio `r` tem pelo menos `⌈q^n / V_q(n,r)⌉`
palavras, onde `V_q` é o volume da bola de Hamming.

Para o alvo `K_7(9,4)` isso é um número fechado, conferido pelo kernel:

`V_7(9,4) = 182791`, `7^9 = 40353607`, logo `K_7(9,4) ≥ 221`.

Isto **não** promove `K_7(9,4) ≤ 1351`. Esse lado continua dependendo do
replay da cobertura em Lean; o arquivo canônico agora está preservado.
-/

namespace CoveringRecords

open CoveringCodes
open CoveringCodes.Database

/-- Volume da bola de Hamming e o teto da cota, reduzidos pelo kernel. -/
theorem sphereLower_q7_n9_r4 : sphereLower 7 9 4 = 221 := by
  decide

/--
**Cota de Hamming / esferas.** Todo código 7-ário de comprimento 9 e raio de
cobertura 4 tem pelo menos 221 palavras.

`220 * V_7(9,4) = 40214020 < 40353607 = 7^9`, então 220 palavras não cobrem
nem no caso de bolas disjuntas.
-/
theorem hammingSphere_q7_n9_r4 : QaryKLower 7 9 4 221 := by
  simpa [sphereLower_q7_n9_r4] using sphereLower_valid 7 9 4

end CoveringRecords
