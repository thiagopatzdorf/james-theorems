/-!
# Regras · Etiqueta automática do James Negócio

Modelo exato, em centavos (`Int`), da decisão de compra de etiqueta do Melhor Envio de
`apps/sistemas/james-negocio/expedicao_auto.py` (`teto_do_pedido`, `pedido`, `rodada`) e da trava de repetição de
`expedicao.comprar` (`_abrir_intencao`, `_envio_pago_na_loja`).

Fora do modelo (de propósito): a emissão da nota antes da etiqueta, a escolha do serviço (`escolher_servico`) e as
falhas de rede da loja. Cada pacote chega aqui com a cotação do serviço já escolhido.

O que se prova, para qualquer entrada:

* `nunca_duas_vezes`: pacote comprado (ou recuperado) numa rodada nunca é comprado de novo em rodada nenhuma depois;
* `nunca_acima_do_teto`: o que a rodada compra num pedido, somado ao que já estava pago, não passa do teto
  (frete pago + R$ 5; frete grátis, 15% do pedido até R$ 100);
* `nao_pago_nao_compra`: pedido que a loja não diz pago (cancelado, reembolsado) não compra nada nem mexe no saldo;
* `saldo_nunca_estoura`: com o saldo do Melhor Envio conhecido, a rodada inteira (todas as empresas e pedidos) não
  compra mais que o saldo;
* `para_no_saldo`: depois do primeiro bloqueio por saldo, nada mais é tentado na rodada.
-/

namespace Regras.Etiqueta

inductive Status where
  | pago | cancelado | reembolsado
  deriving DecidableEq, Repr

/-- O estado de um pacote no banco (`envios_me`) e a cotação do serviço que o pacote compraria. -/
inductive Pacote where
  /-- sem linha em `envios_me` -/
  | livre (cotacao : Int)
  /-- etiqueta comprada (status diferente de `comprando`), com o preço gravado -/
  | comprado (preco : Int)
  /-- intenção gravada há menos de 5 min, sem resposta -/
  | comprandoRecente (cotacao : Int)
  /-- intenção vencida; `pagoNaLoja` é o preço do envio que a loja achou pago pela tag do pedido, se achou -/
  | comprandoVencida (cotacao : Int) (pagoNaLoja : Option Int)
  deriving DecidableEq, Repr

inductive Resultado where
  | jaFeito
  | comprada (preco : Int)
  | recuperada (preco : Int)
  | teto
  | saldo
  | emAndamento
  | naoTentado
  | pulado
  deriving DecidableEq, Repr

structure Pedido where
  status : Status
  frete : Int
  total : Int
  pacotes : List Pacote
  deriving DecidableEq, Repr

/-- `Decimal.quantize(Decimal("0.01"))` de `n / d` com o arredondamento padrão do Python (meio para o par), `n ≥ 0`. -/
def meioPar (n d : Int) : Int :=
  let q := n / d
  let r := n % d
  if 2 * r > d then q + 1 else if 2 * r < d then q else if q % 2 = 0 then q else q + 1

/-- `teto_do_pedido`: frete pago + `TOLERANCIA` (R$ 5); frete grátis, 15% do total até `TETO_FRETE_GRATIS` (R$ 100). -/
def teto (frete total : Int) : Int :=
  if frete > 0 then frete + 500 else min (meioPar (total * 15) 100) 10000

def gastoInicial : List Pacote → Int
  | [] => 0
  | .comprado p :: resto => p + gastoInicial resto
  | _ :: resto => gastoInicial resto

def cotacao : Pacote → Int
  | .livre q | .comprandoRecente q | .comprandoVencida q _ => q
  | .comprado p => p

structure Estado where
  gasto : Int
  saldo : Option Int
  deriving DecidableEq, Repr

def debitar (e : Estado) (p : Int) : Estado := ⟨e.gasto + p, e.saldo.map (· - p)⟩

def falta (saldo : Option Int) (q : Int) : Bool :=
  match saldo with
  | some s => decide (q > s)
  | none => false

/-- Um pacote: o resultado, o estado novo e se a rodada para (`break` depois do saldo). -/
def decidir (t : Int) (e : Estado) (pk : Pacote) : Resultado × Estado × Bool :=
  match pk with
  | .comprado _ => (.jaFeito, e, false)
  | _ =>
    let q := cotacao pk
    if q > t - e.gasto then (.teto, e, false)
    else if falta e.saldo q then (.saldo, { e with saldo := some (-1) }, true)
    else match pk with
      | .comprandoRecente _ => (.emAndamento, e, false)
      | .comprandoVencida _ (some p) => (.recuperada p, debitar e p, false)
      | _ => (.comprada q, debitar e q, false)

def laco (t : Int) (e : Estado) : List Pacote → List Resultado × Estado
  | [] => ([], e)
  | pk :: resto =>
    let d := decidir t e pk
    if d.2.2 then (d.1 :: resto.map (fun _ => .naoTentado), d.2.1)
    else
      let r := laco t d.2.1 resto
      (d.1 :: r.1, r.2)

/-- `pedido`: o que acontece com cada pacote e o saldo que sobra para a rodada. -/
def pedido (saldo : Option Int) (pd : Pedido) : List Resultado × Option Int :=
  if pd.status = .pago then
    let r := laco (teto pd.frete pd.total) ⟨gastoInicial pd.pacotes, saldo⟩ pd.pacotes
    (r.1, r.2.saldo)
  else (pd.pacotes.map (fun _ => .pulado), saldo)

def parado (s : Option Int) : Bool :=
  match s with
  | some v => decide (v < 0)
  | none => false

/-- `rodada`: os pedidos em ordem, com o saldo lido uma vez e descontado a cada compra. -/
def rodada (s : Option Int) : List Pedido → List (List Resultado)
  | [] => []
  | pd :: resto =>
    if parado s then (pd :: resto).map (fun p => p.pacotes.map (fun _ => .naoTentado))
    else
      let r := pedido s pd
      r.1 :: rodada r.2 resto

/-! ## Auxiliares -/

def ehCompra : Resultado → Bool
  | .comprada _ | .recuperada _ => true
  | _ => false

def gastoNovo : Resultado → Int
  | .comprada p => p
  | _ => 0

def soma : List Resultado → Int
  | [] => 0
  | r :: rs => gastoNovo r + soma rs

def ehComprada : Resultado → Bool
  | .comprada _ => true
  | _ => false

def temCompra (rs : List Resultado) : Bool := rs.any ehComprada

theorem temCompra_cons (r : Resultado) (rs : List Resultado) :
    temCompra (r :: rs) = (ehComprada r || temCompra rs) := by simp [temCompra]

/-- Preços que a loja diz pagos e cotações nunca negativos. -/
def NaoNegativo : Pacote → Prop
  | .livre q | .comprandoRecente q => 0 ≤ q
  | .comprandoVencida q none => 0 ≤ q
  | .comprandoVencida q (some p) => 0 ≤ q ∧ 0 ≤ p
  | .comprado _ => True

theorem soma_naoTentado (l : List α) : soma (l.map (fun _ => Resultado.naoTentado)) = 0 := by
  induction l with
  | nil => rfl
  | cons _ _ ih => simp [soma, gastoNovo] at *; exact ih

theorem temCompra_naoTentado (l : List α) : temCompra (l.map (fun _ => Resultado.naoTentado)) = false := by
  simp [temCompra, ehComprada]

theorem soma_sem_compra (rs : List Resultado) (h : temCompra rs = false) : soma rs = 0 := by
  induction rs with
  | nil => rfl
  | cons r rs ih =>
    cases r <;> simp_all [temCompra, ehComprada, soma, gastoNovo]

theorem laco_length (t : Int) (e : Estado) (l : List Pacote) : (laco t e l).1.length = l.length := by
  induction l generalizing e with
  | nil => rfl
  | cons pk resto ih =>
    simp only [laco]; split <;> simp [ih]

/-! ## Nunca acima do teto -/

theorem decidir_teto (t : Int) (e : Estado) (pk : Pacote) (hn : NaoNegativo pk) :
    e.gasto + gastoNovo (decidir t e pk).1 ≤ (decidir t e pk).2.1.gasto ∧
      (∀ q, (decidir t e pk).1 = .comprada q → e.gasto + q ≤ t) := by
  cases pk with
  | comprado p => simp [decidir, gastoNovo]
  | livre q =>
    by_cases h1 : q > t - e.gasto <;> by_cases h2 : falta e.saldo q = true <;>
      simp [decidir, cotacao, h1, h2, debitar, gastoNovo] <;> omega
  | comprandoRecente q =>
    by_cases h1 : q > t - e.gasto <;> by_cases h2 : falta e.saldo q = true <;>
      simp [decidir, cotacao, h1, h2, gastoNovo]
  | comprandoVencida q o =>
    cases o with
    | none =>
      by_cases h1 : q > t - e.gasto <;> by_cases h2 : falta e.saldo q = true <;>
        simp [decidir, cotacao, h1, h2, debitar, gastoNovo] <;> omega
    | some p =>
      simp [NaoNegativo] at hn
      by_cases h1 : q > t - e.gasto <;> by_cases h2 : falta e.saldo q = true <;>
        simp [decidir, cotacao, h1, h2, debitar, gastoNovo] <;> omega

theorem laco_teto (t : Int) (l : List Pacote) (hn : ∀ pk ∈ l, NaoNegativo pk) (e : Estado) :
    e.gasto + soma (laco t e l).1 ≤ (laco t e l).2.gasto ∧
      (temCompra (laco t e l).1 = true → e.gasto + soma (laco t e l).1 ≤ t) := by
  induction l generalizing e with
  | nil => simp [laco, soma, temCompra]
  | cons pk resto ih =>
    obtain ⟨hd1, hd2⟩ := decidir_teto t e pk (hn pk (List.mem_cons_self ..))
    have ih' := ih (fun p hp => hn p (List.mem_cons_of_mem _ hp))
    simp only [laco]
    generalize decidir t e pk = d at *
    obtain ⟨r, e1, b⟩ := d
    simp only at hd1 hd2 ⊢
    cases b with
    | true =>
      simp only [ite_true, soma, soma_naoTentado]
      refine ⟨by omega, ?_⟩
      intro hc
      rw [temCompra_cons, temCompra_naoTentado] at hc
      cases r <;> simp_all [gastoNovo, ehComprada]
    | false =>
      obtain ⟨i1, i2⟩ := ih' e1
      simp only [Bool.false_eq_true, ite_false, soma]
      refine ⟨by omega, ?_⟩
      intro hc
      rw [temCompra_cons] at hc
      by_cases hr : temCompra (laco t e1 resto).1 = true
      · have := i2 hr
        cases r with
        | comprada q => have := hd2 q rfl; simp [gastoNovo] at *; omega
        | _ => simp [gastoNovo] at *; omega
      · have h0 := soma_sem_compra _ (by simpa using hr)
        cases r with
        | comprada q => have := hd2 q rfl; simp [gastoNovo] at *; omega
        | _ => simp [ehComprada, hr] at hc

/-- Nunca acima do teto: se a rodada comprou alguma etiqueta do pedido, o que já estava pago mais o que ela comprou
não passa do teto do pedido. -/
theorem nunca_acima_do_teto (s : Option Int) (pd : Pedido) (hn : ∀ pk ∈ pd.pacotes, NaoNegativo pk)
    (h : temCompra (pedido s pd).1 = true) :
    gastoInicial pd.pacotes + soma (pedido s pd).1 ≤ teto pd.frete pd.total := by
  unfold pedido at *
  split at h
  · next hp => simp only [hp, ite_true] at *; exact (laco_teto _ _ hn _).2 h
  · simp [temCompra, ehComprada] at h

/-- O teto é o que a regra diz: frete pago + R$ 5, ou 15% do pedido limitado a R$ 100 no frete grátis. -/
theorem teto_exato (frete total : Int) :
    (frete > 0 → teto frete total = frete + 500) ∧ (frete ≤ 0 → teto frete total ≤ 10000) := by
  unfold teto
  constructor
  · intro h; simp [h]
  · intro h; simp [show ¬ frete > 0 by omega]; omega

/-! ## Pedido não pago não compra -/

/-- Pedido que a loja não diz pago (cancelado, reembolsado): todo pacote fica `pulado` e o saldo não muda. -/
theorem nao_pago_nao_compra (s : Option Int) (pd : Pedido) (h : pd.status ≠ .pago) :
    pedido s pd = (pd.pacotes.map (fun _ => .pulado), s) := by
  simp [pedido, h]

/-! ## O saldo nunca estoura -/

/-- O invariante do saldo: `acc` já comprado na rodada, `cs` o saldo que o código acha que sobra, `s0` o saldo lido. -/
def J (s0 acc cs : Int) : Prop := acc ≤ s0 ∧ (0 ≤ cs → acc + cs ≤ s0)

theorem decidir_saldo (t : Int) (e : Estado) (pk : Pacote) (cs acc s0 : Int) (hs : e.saldo = some cs)
    (hn : NaoNegativo pk) (hJ : J s0 acc cs) :
    ∃ cs', (decidir t e pk).2.1.saldo = some cs' ∧ J s0 (acc + gastoNovo (decidir t e pk).1) cs' := by
  unfold J at *
  cases pk with
  | comprado p => exact ⟨cs, by simp [decidir, hs], by simpa [decidir, gastoNovo] using hJ⟩
  | livre q =>
    simp [NaoNegativo] at hn
    by_cases h1 : q > t - e.gasto
    · exact ⟨cs, by simp [decidir, cotacao, h1, hs], by simpa [decidir, cotacao, h1, gastoNovo] using hJ⟩
    · by_cases h2 : q > cs
      · refine ⟨-1, by simp [decidir, cotacao, h1, falta, hs, h2], ?_⟩
        simp [decidir, cotacao, h1, falta, hs, h2, gastoNovo]; omega
      · refine ⟨cs - q, by simp [decidir, cotacao, h1, falta, hs, h2, debitar], ?_⟩
        simp [decidir, cotacao, h1, falta, hs, h2, gastoNovo]; omega
  | comprandoRecente q =>
    by_cases h1 : q > t - e.gasto
    · exact ⟨cs, by simp [decidir, cotacao, h1, hs], by simpa [decidir, cotacao, h1, gastoNovo] using hJ⟩
    · by_cases h2 : q > cs
      · refine ⟨-1, by simp [decidir, cotacao, h1, falta, hs, h2], ?_⟩
        simp [decidir, cotacao, h1, falta, hs, h2, gastoNovo]; omega
      · exact ⟨cs, by simp [decidir, cotacao, h1, falta, hs, h2],
          by simpa [decidir, cotacao, h1, falta, hs, h2, gastoNovo] using hJ⟩
  | comprandoVencida q o =>
    by_cases h1 : q > t - e.gasto
    · exact ⟨cs, by simp [decidir, cotacao, h1, hs], by simpa [decidir, cotacao, h1, gastoNovo] using hJ⟩
    · by_cases h2 : q > cs
      · refine ⟨-1, by simp [decidir, cotacao, h1, falta, hs, h2], ?_⟩
        simp [decidir, cotacao, h1, falta, hs, h2, gastoNovo]; omega
      · cases o with
        | none =>
          simp [NaoNegativo] at hn
          refine ⟨cs - q, by simp [decidir, cotacao, h1, falta, hs, h2, debitar], ?_⟩
          simp [decidir, cotacao, h1, falta, hs, h2, gastoNovo]; omega
        | some p =>
          simp [NaoNegativo] at hn
          refine ⟨cs - p, by simp [decidir, cotacao, h1, falta, hs, h2, debitar], ?_⟩
          simp [decidir, cotacao, h1, falta, hs, h2, gastoNovo]; omega

theorem laco_saldo (t : Int) (l : List Pacote) (hn : ∀ pk ∈ l, NaoNegativo pk) (s0 : Int) :
    ∀ (e : Estado) (cs acc : Int), e.saldo = some cs → J s0 acc cs →
      ∃ cs', (laco t e l).2.saldo = some cs' ∧ J s0 (acc + soma (laco t e l).1) cs' := by
  induction l with
  | nil => intro e cs acc hs hJ; exact ⟨cs, hs, by simpa [laco, soma] using hJ⟩
  | cons pk resto ih =>
    intro e cs acc hs hJ
    obtain ⟨cs1, h1, hJ1⟩ := decidir_saldo t e pk cs acc s0 hs (hn pk (List.mem_cons_self ..)) hJ
    have ih' := ih (fun p hp => hn p (List.mem_cons_of_mem _ hp))
    simp only [laco]
    generalize decidir t e pk = d at *
    obtain ⟨r, e1, b⟩ := d
    simp only at h1 hJ1 ⊢
    cases b with
    | true => exact ⟨cs1, h1, by simpa [soma, soma_naoTentado] using hJ1⟩
    | false =>
      obtain ⟨cs2, h2, hJ2⟩ := ih' e1 cs1 _ h1 hJ1
      exact ⟨cs2, h2, by simpa [soma, Int.add_assoc] using hJ2⟩

def somaTotal (rr : List (List Resultado)) : Int := (rr.map soma).foldr (· + ·) 0

theorem somaTotal_naoTentado (pds : List Pedido) :
    somaTotal (pds.map (fun p => p.pacotes.map (fun _ => Resultado.naoTentado))) = 0 := by
  induction pds with
  | nil => rfl
  | cons p ps ih => simp [somaTotal, soma_naoTentado] at *; exact ih

theorem soma_pulado (l : List α) : soma (l.map (fun _ => Resultado.pulado)) = 0 := by
  induction l with
  | nil => rfl
  | cons _ _ ih => simp [soma, gastoNovo] at *; exact ih

theorem rodada_saldo (s0 : Int) (pds : List Pedido) (hn : ∀ pd ∈ pds, ∀ pk ∈ pd.pacotes, NaoNegativo pk) :
    ∀ cs acc, J s0 acc cs → acc + somaTotal (rodada (some cs) pds) ≤ s0 := by
  induction pds with
  | nil => intro cs acc hJ; simpa [rodada, somaTotal, J] using hJ.1
  | cons pd resto ih =>
    intro cs acc hJ
    have ih' := ih (fun p hp => hn p (List.mem_cons_of_mem _ hp))
    by_cases hp : parado (some cs) = true
    · simp only [rodada, hp, ite_true]
      have := somaTotal_naoTentado (pd :: resto)
      rw [this]; simpa using hJ.1
    · simp only [rodada, hp]
      simp only [Bool.false_eq_true, ite_false]
      unfold pedido
      by_cases hs : pd.status = .pago
      · simp only [hs, ite_true]
        obtain ⟨cs2, h2, hJ2⟩ := laco_saldo (teto pd.frete pd.total) pd.pacotes (hn pd (List.mem_cons_self ..)) s0
          ⟨gastoInicial pd.pacotes, some cs⟩ cs acc rfl hJ
        rw [h2]
        have := ih' cs2 _ hJ2
        simp only [somaTotal, List.map_cons, List.foldr_cons] at *
        omega
      · simp only [hs, ite_false]
        have := ih' cs acc hJ
        simp only [somaTotal, List.map_cons, List.foldr_cons, soma_pulado] at *
        omega

/-- O saldo nunca estoura: com o saldo do Melhor Envio conhecido e não negativo, tudo que a rodada compra, somado em
todos os pedidos, cabe no saldo lido. -/
theorem saldo_nunca_estoura (s0 : Int) (h0 : 0 ≤ s0) (pds : List Pedido)
    (hn : ∀ pd ∈ pds, ∀ pk ∈ pd.pacotes, NaoNegativo pk) : somaTotal (rodada (some s0) pds) ≤ s0 := by
  have := rodada_saldo s0 pds hn s0 0 ⟨h0, by omega⟩
  omega

/-! ## Para no primeiro bloqueio por saldo -/

/-- Depois de um `saldo`, só `naoTentado`. -/
def Bom : List Resultado → Prop
  | [] => True
  | .saldo :: rs => ∀ x ∈ rs, x = .naoTentado
  | _ :: rs => Bom rs

theorem bom_cons (r : Resultado) (rs : List Resultado) (hr : r ≠ .saldo) (h : Bom rs) : Bom (r :: rs) := by
  cases r <;> simp_all [Bom]

theorem bom_append (l1 l2 : List Resultado) (h1 : Bom l1) (h2 : Bom l2)
    (h : Resultado.saldo ∈ l1 → ∀ x ∈ l2, x = .naoTentado) : Bom (l1 ++ l2) := by
  induction l1 with
  | nil => simpa using h2
  | cons r rs ih =>
    cases r with
    | saldo =>
      simp only [Bom, List.cons_append] at h1 ⊢
      intro x hx
      rcases List.mem_append.mp hx with hx | hx
      · exact h1 x hx
      · exact h (List.mem_cons_self ..) x hx
    | _ =>
      simp only [List.cons_append]
      apply bom_cons _ _ (by simp)
      exact ih (by simpa [Bom] using h1) (fun hs => h (List.mem_cons_of_mem _ hs))

theorem decidir_parou (t : Int) (e : Estado) (pk : Pacote) :
    ((decidir t e pk).2.2 = true ↔ (decidir t e pk).1 = .saldo) ∧
      ((decidir t e pk).2.2 = true → (decidir t e pk).2.1.saldo = some (-1)) := by
  cases pk with
  | comprado p => simp [decidir]
  | livre q =>
    by_cases h1 : q > t - e.gasto <;> by_cases h2 : falta e.saldo q = true <;> simp [decidir, cotacao, h1, h2]
  | comprandoRecente q =>
    by_cases h1 : q > t - e.gasto <;> by_cases h2 : falta e.saldo q = true <;> simp [decidir, cotacao, h1, h2]
  | comprandoVencida q o =>
    cases o <;> by_cases h1 : q > t - e.gasto <;> by_cases h2 : falta e.saldo q = true <;>
      simp [decidir, cotacao, h1, h2]

theorem laco_bom (t : Int) (l : List Pacote) :
    ∀ e, Bom (laco t e l).1 ∧ (Resultado.saldo ∈ (laco t e l).1 → (laco t e l).2.saldo = some (-1)) := by
  induction l with
  | nil => intro e; simp [laco, Bom]
  | cons pk resto ih =>
    intro e
    obtain ⟨hp1, hp2⟩ := decidir_parou t e pk
    simp only [laco]
    generalize decidir t e pk = d at *
    obtain ⟨r, e1, b⟩ := d
    simp only at hp1 hp2 ⊢
    cases b with
    | true =>
      have hr : r = .saldo := hp1.mp rfl
      subst hr
      simp only [ite_true]
      refine ⟨?_, fun _ => hp2 rfl⟩
      simp [Bom]
    | false =>
      have hr : r ≠ .saldo := fun h => by simpa using hp1.mpr h
      obtain ⟨i1, i2⟩ := ih e1
      simp only [Bool.false_eq_true, ite_false]
      refine ⟨bom_cons _ _ hr i1, ?_⟩
      intro hm
      rcases List.mem_cons.mp hm with h | h
      · exact absurd h.symm hr
      · exact i2 h

theorem flatten_naoTentado (pds : List Pedido) :
    ∀ x ∈ (pds.map (fun p => p.pacotes.map (fun _ => Resultado.naoTentado))).flatten, x = .naoTentado := by
  intro x hx
  rw [List.mem_flatten] at hx
  obtain ⟨l, hl, hx⟩ := hx
  rw [List.mem_map] at hl
  obtain ⟨p, -, rfl⟩ := hl
  rw [List.mem_map] at hx
  obtain ⟨_, -, rfl⟩ := hx
  rfl

theorem bom_naoTentado (l : List Resultado) (h : ∀ x ∈ l, x = .naoTentado) : Bom l := by
  induction l with
  | nil => trivial
  | cons r rs ih =>
    have hr := h r (List.mem_cons_self ..)
    subst hr
    exact bom_cons _ _ (by simp) (ih (fun x hx => h x (List.mem_cons_of_mem _ hx)))

theorem bom_pulado (l : List α) : Bom (l.map (fun _ => Resultado.pulado)) := by
  induction l with
  | nil => trivial
  | cons _ _ ih => exact bom_cons _ _ (by simp) ih

/-- Para no saldo: na sequência de tudo que a rodada decidiu (pedido por pedido, pacote por pacote), depois do
primeiro bloqueio por saldo nada mais é tentado, nem neste pedido nem nos seguintes. -/
theorem para_no_saldo (s : Option Int) (pds : List Pedido) : Bom (rodada s pds).flatten := by
  induction pds generalizing s with
  | nil => trivial
  | cons pd resto ih =>
    by_cases hp : parado s = true
    · simp only [rodada, hp, ite_true]
      exact bom_naoTentado _ (flatten_naoTentado _)
    · simp only [rodada, hp, Bool.false_eq_true, ite_false, List.flatten_cons]
      unfold pedido
      by_cases hs : pd.status = .pago
      · simp only [hs, ite_true]
        obtain ⟨b1, b2⟩ := laco_bom (teto pd.frete pd.total) pd.pacotes ⟨gastoInicial pd.pacotes, s⟩
        apply bom_append _ _ b1 (ih _)
        intro hm
        have h1 := b2 hm
        rw [h1]
        cases resto with
        | nil => simp [rodada]
        | cons p ps =>
          simp only [rodada, parado, show decide ((-1 : Int) < 0) = true by decide, ite_true]
          exact flatten_naoTentado _
      · simp only [hs, ite_false]
        apply bom_append _ _ (bom_pulado _) (ih _)
        intro hm; simp at hm

/-! ## Nunca duas vezes -/

/-- O estado do pacote depois da rodada: comprado ou recuperado vira `comprado` (a linha gravada em `envios_me`). -/
def atualizar : Pacote → Resultado → Pacote
  | _, .comprada p => .comprado p
  | _, .recuperada p => .comprado p
  | pk, _ => pk

def proximo (pd : Pedido) (rs : List Resultado) : Pedido :=
  { pd with pacotes := List.zipWith atualizar pd.pacotes rs }

/-- Várias rodadas seguidas sobre o mesmo pedido, cada uma vendo o banco que a anterior deixou; o saldo de cada
rodada é qualquer um (recarga, outro pedido, leitura que falhou). -/
def rodadas : List (Option Int) → Pedido → List (List Resultado)
  | [], _ => []
  | s :: ss, pd => (pedido s pd).1 :: rodadas ss (proximo pd (pedido s pd).1)

def comprouEm (i : Nat) (rs : List Resultado) : Bool :=
  match rs[i]? with
  | some r => ehCompra r
  | none => false

theorem laco_comprado (t : Int) (l : List Pacote) :
    ∀ e i p, l[i]? = some (.comprado p) → comprouEm i (laco t e l).1 = false := by
  induction l with
  | nil => intro e i p h; simp at h
  | cons pk resto ih =>
    intro e i p h
    simp only [laco]
    cases i with
    | zero =>
      simp at h; subst h
      simp [decidir, comprouEm, ehCompra]
    | succ i =>
      simp at h
      generalize decidir t e pk = d
      obtain ⟨r, e1, b⟩ := d
      cases b with
      | true =>
        simp only [ite_true, comprouEm, List.getElem?_cons_succ, List.getElem?_map]
        cases resto[i]? <;> simp [ehCompra]
      | false =>
        have := ih e1 i p h
        simpa [comprouEm] using this

theorem pedido_comprado (s : Option Int) (pd : Pedido) (i : Nat) (p : Int) (h : pd.pacotes[i]? = some (.comprado p)) :
    comprouEm i (pedido s pd).1 = false := by
  unfold pedido
  split
  · exact laco_comprado _ _ _ _ _ h
  · simp only [comprouEm, List.getElem?_map, h]; simp [ehCompra]

theorem proximo_comprado (pd : Pedido) (rs : List Resultado) (i : Nat) (hl : rs.length = pd.pacotes.length)
    (h : comprouEm i rs = true ∨ ∃ p, pd.pacotes[i]? = some (.comprado p)) :
    ∃ p, (proximo pd rs).pacotes[i]? = some (.comprado p) := by
  simp only [proximo, List.getElem?_zipWith]
  rcases h with h | ⟨p, hp⟩
  · simp only [comprouEm] at h
    have hi : i < rs.length := by
      cases hr : rs[i]? with
      | none => simp [hr] at h
      | some _ => exact (List.getElem?_eq_some_iff.mp hr).1
    have hi' : i < pd.pacotes.length := hl ▸ hi
    rw [List.getElem?_eq_getElem hi'] at *
    cases hr : rs[i]? with
    | none => simp [hr] at h
    | some r =>
      simp only [hr] at h ⊢
      cases r <;> simp [ehCompra] at h <;> simp [atualizar]
  · rw [hp]
    cases hr : rs[i]? with
    | none =>
      have : i < pd.pacotes.length := (List.getElem?_eq_some_iff.mp hp).1
      rw [List.getElem?_eq_none_iff] at hr; omega
    | some r => cases r <;> simp [atualizar]

theorem pedido_length (s : Option Int) (pd : Pedido) : (pedido s pd).1.length = pd.pacotes.length := by
  unfold pedido; split
  · exact laco_length _ _ _
  · simp

def vezes (i : Nat) (rr : List (List Resultado)) : Nat := (rr.filter (comprouEm i)).length

theorem rodadas_comprado (ss : List (Option Int)) :
    ∀ pd i p, pd.pacotes[i]? = some (.comprado p) → vezes i (rodadas ss pd) = 0 := by
  induction ss with
  | nil => intro pd i p h; rfl
  | cons s ss ih =>
    intro pd i p h
    have h0 := pedido_comprado s pd i p h
    obtain ⟨p', hp'⟩ := proximo_comprado pd (pedido s pd).1 i (pedido_length s pd) (Or.inr ⟨p, h⟩)
    have := ih _ i p' hp'
    simp only [vezes, rodadas, List.filter_cons, h0] at *
    simpa using this

/-- Nunca duas vezes: em qualquer sequência de rodadas (qualquer saldo em cada uma), cada pacote é comprado (ou
recuperado de uma compra sem resposta) no máximo uma vez. -/
theorem nunca_duas_vezes (ss : List (Option Int)) (pd : Pedido) (i : Nat) : vezes i (rodadas ss pd) ≤ 1 := by
  induction ss generalizing pd with
  | nil => simp [rodadas, vezes]
  | cons s ss ih =>
    by_cases hc : comprouEm i (pedido s pd).1 = true
    · obtain ⟨p, hp⟩ := proximo_comprado pd (pedido s pd).1 i (pedido_length s pd) (Or.inl hc)
      have := rodadas_comprado ss _ i p hp
      simp only [vezes, rodadas, List.filter_cons, hc] at *
      simp [this]
    · have := ih (proximo pd (pedido s pd).1)
      simp only [vezes, rodadas, List.filter_cons, hc] at *
      simpa using this

end Regras.Etiqueta
