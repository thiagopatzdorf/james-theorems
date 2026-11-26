/-!
# Regras · Preço da MyBagCenter

Modelo exato, em centavos (`Int`), de duas peças do código da loja:

* a **guarda de preço** (`apps/mybagcenter/scripts/catalog/guarda-preco.ts`, `conferirPrecos`): preço abaixo do custo
  bloqueia; preço mais de `DESCONTO_MAXIMO_SOBRE_ML` (20%) abaixo do Mercado Livre avisa; irmãos com o mesmo preço e
  Mercado Livre que difere mais de `DIFERENCA_ML_ENTRE_IRMAOS` (15%) avisam;
* a **regra que dá o preço do site** (`precos-abaixo-da-ideris.ts`, `precoDoSite`): 92,5% da referência (menor preço
  da Ideris/Mercado Livre) para baixo em 4,90 ou 9,90, nunca abaixo do piso custo × 1,3 (para cima em ,90), nunca igual
  ou acima da referência; sem referência, custo × 1,8 para baixo em ,90.

Não existe no código uma regra "Mercado Livre menos R$ 5": a regra de preço que existe é a de 92,5% acima, e é ela que
este arquivo modela (o "menos R$ 5" mais próximo é o degrau de 4,90/9,90, que tira até R$ 5 dos 92,5%).

`Math.round(x)` do JavaScript é `⌊x + 1/2⌋` (meio para cima), e é isso que `arred` faz sobre a fração exata.
Os testes da loja comparam o código de ponto flutuante com estas funções nos vetores gerados por `Vetores.lean`.
-/

namespace Regras.Preco

/-- `Math.round(n / d)` para `d > 0`: meio arredonda para cima. -/
def arred (n d : Int) : Int := (2 * n + d) / (2 * d)

/-- Maior valor terminado em 4,90 ou 9,90 que não passa de `v` (`abaixoEm490`). -/
def abaixo490 (v : Int) : Int := (v - 490) / 500 * 500 + 490

/-- Maior valor terminado em ,90 que não passa de `v` (`abaixoEm90`). -/
def abaixo90 (v : Int) : Int := (v - 90) / 100 * 100 + 90

/-- Menor valor terminado em ,90 que não fica abaixo de `v` (`acimaEm90`). -/
def acima90 (v : Int) : Int := if abaixo90 v ≥ v then abaixo90 v else abaixo90 v + 100

/-- O piso: custo × 1,3 (`MARGEM_MINIMA`), para cima em ,90. -/
def piso (custo : Int) : Int := acima90 (arred (custo * 13) 10)

/-- 92,5% da referência (`FATOR_DO_SITE`), para baixo em 4,90/9,90. -/
def fator (ref : Int) : Int := abaixo490 (arred (ref * 925) 1000)

inductive Regra where
  | fator | piso | semAnuncio
  deriving DecidableEq, Repr

inductive Decisao where
  | preco (p : Int) (regra : Regra)
  | semRefNemCusto
  | semCusto
  | custoAcimaDaRef
  deriving DecidableEq, Repr

/-- `precoDoSite` (custo ≤ 0 = custo desconhecido). -/
def precoDoSite (ref : Option Int) (custo : Int) : Decisao :=
  match ref with
  | none => if custo > 0 then .preco (abaixo90 (arred (custo * 18) 10)) .semAnuncio else .semRefNemCusto
  | some r =>
    if custo ≤ 0 then .semCusto
    else if fator r < piso custo then
      (if piso custo ≥ r then .custoAcimaDaRef else .preco (piso custo) .piso)
    else (if fator r ≥ r then .custoAcimaDaRef else .preco (fator r) .fator)

/-! ## A guarda (`conferirPrecos`) -/

/-- Regra 1, BLOQUEIO: preço positivo abaixo do custo conhecido. -/
def abaixoDoCusto (preco custo : Int) : Bool := decide (preco > 0 ∧ custo > 0 ∧ preco < custo)

/-- Regra 2, aviso: `preco < ml × (1 − 0,20)`, ou seja `10·preco < 8·ml`. -/
def muitoAbaixoDoML (preco ml : Int) : Bool := decide (preco > 0 ∧ ml > 0 ∧ preco * 10 < ml * 8)

/-- Regra 3, aviso (para um grupo de irmãos com o mesmo preço): `(maior − menor) / menor > 0,15`. -/
def irmaosSuspeitos (menor maior : Int) : Bool := decide (menor > 0 ∧ (maior - menor) * 100 > menor * 15)

/-! ## Propriedades da guarda -/

/-- Preço abaixo do custo SEMPRE bloqueia, e só ele bloqueia. -/
theorem abaixo_do_custo_bloqueia_exatamente (p c : Int) :
    abaixoDoCusto p c = true ↔ (p > 0 ∧ c > 0 ∧ p < c) := by
  simp [abaixoDoCusto]

/-- O aviso do Mercado Livre dispara exatamente abaixo de 80% do anúncio. -/
theorem aviso_ml_exato (p ml : Int) :
    muitoAbaixoDoML p ml = true ↔ (p > 0 ∧ ml > 0 ∧ p * 10 < ml * 8) := by
  simp [muitoAbaixoDoML]

/-- O aviso dos irmãos dispara exatamente com diferença acima de 15% do menor. -/
theorem aviso_irmaos_exato (menor maior : Int) :
    irmaosSuspeitos menor maior = true ↔ (menor > 0 ∧ (maior - menor) * 100 > menor * 15) := by
  simp [irmaosSuspeitos]

/-- Monotonia do bloqueio: baixar mais o preço (ou subir o custo) nunca tira o bloqueio. -/
theorem bloqueio_monotono (p p' c c' : Int) (hp : 0 < p') (hpp : p' ≤ p) (hc : c ≤ c')
    (h : abaixoDoCusto p c = true) : abaixoDoCusto p' c' = true := by
  simp [abaixoDoCusto] at *; omega

/-- Monotonia do aviso do Mercado Livre: preço menor ou anúncio maior nunca tiram o aviso. -/
theorem aviso_ml_monotono (p p' ml ml' : Int) (hp : 0 < p') (hpp : p' ≤ p) (hml : ml ≤ ml')
    (h : muitoAbaixoDoML p ml = true) : muitoAbaixoDoML p' ml' = true := by
  simp [muitoAbaixoDoML] at *; omega

/-- Monotonia do aviso dos irmãos: afastar o maior anúncio nunca tira o aviso. -/
theorem aviso_irmaos_monotono (menor maior maior' : Int) (h' : maior ≤ maior')
    (h : irmaosSuspeitos menor maior = true) : irmaosSuspeitos menor maior' = true := by
  simp [irmaosSuspeitos] at *; omega

/-! ## Propriedades das peças de arredondamento -/

theorem abaixo490_le (v : Int) : abaixo490 v ≤ v ∧ v < abaixo490 v + 500 := by
  unfold abaixo490; omega

theorem abaixo90_le (v : Int) : abaixo90 v ≤ v ∧ v < abaixo90 v + 100 := by
  unfold abaixo90; omega

theorem acima90_ge (v : Int) : v ≤ acima90 v ∧ acima90 v < v + 100 := by
  unfold acima90 abaixo90; split <;> omega

theorem abaixo490_monotono {a b : Int} (h : a ≤ b) : abaixo490 a ≤ abaixo490 b := by
  unfold abaixo490; omega

theorem acima90_monotono {a b : Int} (h : a ≤ b) : acima90 a ≤ acima90 b := by
  unfold acima90 abaixo90; split <;> split <;> omega

theorem arred_monotono {a b d : Int} (hd : 0 < d) (h : a ≤ b) : arred a d ≤ arred b d := by
  unfold arred; exact Int.ediv_le_ediv (by omega) (by omega)

theorem fator_monotono {a b : Int} (h : a ≤ b) : fator a ≤ fator b :=
  abaixo490_monotono (arred_monotono (by decide) (by omega))

theorem piso_monotono {a b : Int} (h : a ≤ b) : piso a ≤ piso b :=
  acima90_monotono (arred_monotono (by decide) (by omega))

/-- O piso fica sempre no custo ou acima (custo × 1,3 arredondado não desce do custo). -/
theorem piso_ge_custo (c : Int) (hc : 0 < c) : c ≤ piso c := by
  have h := acima90_ge (arred (c * 13) 10)
  unfold piso; unfold arred at *; omega

/-! ## Propriedades da regra do preço do site -/

/-- O preço com referência, antes da trava "nunca chega à referência": o maior entre 92,5% e o piso. -/
def comRef (r c : Int) : Int := if fator r < piso c then piso c else fator r

/-- O que a regra garante sempre que dá um preço com referência. -/
theorem caracteriza (r c p : Int) (g : Regra) (h : precoDoSite (some r) c = .preco p g) :
    0 < c ∧ p = comRef r c ∧ p < r := by
  simp only [precoDoSite] at h
  by_cases h1 : c ≤ 0
  · simp [h1] at h
  · by_cases h2 : fator r < piso c
    · by_cases h3 : piso c ≥ r
      · simp [h1, h2, h3] at h
      · simp [h1, h2, h3] at h; obtain ⟨rfl, -⟩ := h; simp [comRef, h2]; omega
    · by_cases h3 : fator r ≥ r
      · simp [h1, h2, h3] at h
      · simp [h1, h2, h3] at h; obtain ⟨rfl, -⟩ := h; simp [comRef, h2]; omega

/-- Com referência, o preço nunca fica abaixo do piso, nunca abaixo do custo e nunca chega à referência. -/
theorem preco_respeita_piso (r c p : Int) (g : Regra) (h : precoDoSite (some r) c = .preco p g) :
    piso c ≤ p ∧ c ≤ p ∧ p < r := by
  obtain ⟨hc, rfl, hr⟩ := caracteriza r c p g h
  have := piso_ge_custo c hc
  by_cases hh : fator r < piso c <;> simp [comRef, hh] at hr ⊢ <;> omega

/-- Por isso o preço que a própria regra dá nunca cai no bloqueio da guarda. -/
theorem preco_nunca_bloqueado (r c p : Int) (g : Regra) (h : precoDoSite (some r) c = .preco p g) :
    abaixoDoCusto p c = false := by
  have := preco_respeita_piso r c p g h
  simp [abaixoDoCusto]; omega

/-- O preço é monótono na referência: referência maior nunca dá preço menor (mesmo custo). -/
theorem preco_monotono_na_ref (r1 r2 c p1 p2 : Int) (g1 g2 : Regra) (hr : r1 ≤ r2)
    (h1 : precoDoSite (some r1) c = .preco p1 g1) (h2 : precoDoSite (some r2) c = .preco p2 g2) : p1 ≤ p2 := by
  obtain ⟨-, rfl, -⟩ := caracteriza _ _ _ _ h1
  obtain ⟨-, rfl, -⟩ := caracteriza _ _ _ _ h2
  have := fator_monotono hr
  unfold comRef; split <;> split <;> omega

/-- O preço é monótono no custo: custo maior nunca dá preço menor (mesma referência). -/
theorem preco_monotono_no_custo (r c1 c2 p1 p2 : Int) (g1 g2 : Regra) (hc : c1 ≤ c2)
    (h1 : precoDoSite (some r) c1 = .preco p1 g1) (h2 : precoDoSite (some r) c2 = .preco p2 g2) : p1 ≤ p2 := by
  obtain ⟨-, rfl, -⟩ := caracteriza _ _ _ _ h1
  obtain ⟨-, rfl, -⟩ := caracteriza _ _ _ _ h2
  have := piso_monotono hc
  unfold comRef; split <;> split <;> omega

/-- A partir de R$ 40,04 de referência, o preço da regra nunca dispara o aviso de 20% abaixo do Mercado Livre. -/
theorem preco_sem_aviso_ml (r c p : Int) (g : Regra) (hr : 4004 ≤ r) (h : precoDoSite (some r) c = .preco p g) :
    muitoAbaixoDoML p r = false := by
  have hf : r * 8 ≤ fator r * 10 := by
    have := abaixo490_le (arred (r * 925) 1000)
    unfold fator; unfold arred at *; omega
  obtain ⟨-, rfl, -⟩ := caracteriza _ _ _ _ h
  have hp : fator r ≤ comRef r c := by unfold comRef; split <;> omega
  simp [muitoAbaixoDoML]; omega

/-- Sem anúncio (custo × 1,8 para baixo em ,90) o preço só garante o custo a partir de R$ 1,25 de custo. -/
theorem sem_anuncio_cobre_custo (c p : Int) (g : Regra) (hc : 125 ≤ c) (h : precoDoSite none c = .preco p g) :
    c ≤ p := by
  simp only [precoDoSite] at h
  by_cases h1 : c > 0
  · simp [h1] at h; obtain ⟨rfl, -⟩ := h
    have := abaixo90_le (arred (c * 18) 10)
    unfold arred at *; omega
  · omega

/-- E abaixo disso não garante: custo de R$ 1,00 sem anúncio dá preço de R$ 0,90 (o ramo não tem piso). -/
theorem sem_anuncio_abaixo_do_custo : precoDoSite none 100 = .preco 90 .semAnuncio := by decide

end Regras.Preco
