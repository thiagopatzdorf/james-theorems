import Regras.Preco
import Regras.Etiqueta

/-!
# Vetores de teste das regras provadas

`lake exe vetores <saída-preco.json> <saída-etiqueta.json>` escreve os casos (de borda e aleatórios, com semente fixa)
com a saída calculada pelos modelos de `Regras/`. O código de verdade da casa (loja em TypeScript, James Negócio em
Python) tem de bater com eles nos testes: `apps/mybagcenter/scripts/catalog/regras-provadas.test.ts` e
`apps/sistemas/james-negocio/tests/test_regras_provadas_etiqueta.py` no `fabrica-de-sites`.
-/

open Regras

/-! ## JSON mínimo (sem dependência) -/

inductive J where
  | num (n : Int)
  | bool (b : Bool)
  | str (s : String)
  | null
  | arr (xs : List J)
  | obj (kv : List (String × J))

partial def J.render : J → String
  | .num n => toString n
  | .bool b => if b then "true" else "false"
  | .str s => "\"" ++ s ++ "\""
  | .null => "null"
  | .arr xs => "[" ++ ", ".intercalate (xs.map J.render) ++ "]"
  | .obj kv => "{" ++ ", ".intercalate (kv.map fun (k, v) => "\"" ++ k ++ "\": " ++ v.render) ++ "}"

def linhas (casos : List J) : String := "[\n  " ++ ",\n  ".intercalate (casos.map J.render) ++ "\n]"

/-! ## Gerador determinístico (LCG de 64 bits) -/

structure Rng where
  s : Nat

def Rng.prox (g : Rng) : Nat × Rng :=
  let s := (g.s * 6364136223846793005 + 1442695040888963407) % 18446744073709551616
  (s / 65536, ⟨s⟩)

/-- Inteiro em `[lo, hi]`. -/
def Rng.entre (g : Rng) (lo hi : Int) : Int × Rng :=
  let (x, g) := g.prox
  (lo + (x % (hi - lo + 1).toNat : Nat), g)

def repetir (n : Nat) (g : Rng) (f : Rng → J × Rng) : List J × Rng := Id.run do
  let mut g := g
  let mut out := #[]
  for _ in [0:n] do
    let (j, g') := f g
    out := out.push j
    g := g'
  return (out.toList, g)

/-! ## Preço -/

namespace Preco
open Regras.Preco

def regraJ : Regra → String
  | .fator => "fator" | .piso => "piso" | .semAnuncio => "sem_anuncio"

def decisaoJ : Decisao → J
  | .preco p r => .obj [("preco", .num p), ("regra", .str (regraJ r))]
  | .semRefNemCusto => .obj [("motivo", .str "sem_referencia_nem_custo")]
  | .semCusto => .obj [("motivo", .str "sem_custo")]
  | .custoAcimaDaRef => .obj [("motivo", .str "custo_acima_da_referencia")]

def guarda (origem : String) (p c ml : Int) : J :=
  .obj [("origem", .str origem), ("preco", .num p), ("custo", .num c), ("ml", .num ml),
        ("abaixo_do_custo", .bool (abaixoDoCusto p c)), ("muito_abaixo_do_ml", .bool (muitoAbaixoDoML p ml))]

def irmaos (origem : String) (preco menor maior : Int) : J :=
  .obj [("origem", .str origem), ("preco", .num preco), ("ml_menor", .num menor), ("ml_maior", .num maior),
        ("irmao_com_mesmo_preco", .bool (irmaosSuspeitos menor maior))]

def site (origem : String) (ref : Option Int) (c : Int) : J :=
  .obj [("origem", .str origem), ("referencia", match ref with | some r => .num r | none => .null),
        ("custo", .num c), ("esperado", decisaoJ (precoDoSite ref c))]

def bordaGuarda : List J := Id.run do
  let mut out := #[]
  for ml in [1000, 49990, 12345, 99999, 250000] do
    -- 80% do anúncio, um centavo abaixo e acima (10·p = 8·ml quando ml é múltiplo de 5)
    for p in [ml * 8 / 10 - 1, ml * 8 / 10, ml * 8 / 10 + 1] do
      out := out.push (guarda "borda: 80% do Mercado Livre" p 0 ml)
  for c in [1, 100, 23470, 99999] do
    for p in [c - 1, c, c + 1] do
      out := out.push (guarda "borda: custo" p c 0)
  for (p, c, ml) in [((0 : Int), (100 : Int), (100 : Int)), (-5, 100, 100), (50, -1, 0), (50, 0, -3), (32990, 23470, 49634)] do
    out := out.push (guarda "borda: não positivos e o Bluey 21038" p c ml)
  return out.toList

def bordaIrmaos : List J := Id.run do
  let mut out := #[]
  for menor in [1000, 2000, 33333, 49634, 100000] do
    -- 15% exatos: maior = 1,15 × menor
    for d in [-1, 0, 1] do
      out := out.push (irmaos "borda: 15% entre irmãos" 32990 menor (menor * 115 / 100 + d))
  out := out.push (irmaos "borda: o Bluey (45%)" 32990 34234 49634)
  return out.toList

def bordaSite : List J := Id.run do
  let mut out := #[]
  -- empates do arredondamento: ref ≡ 20 (mod 40) dá ref × 0,925 com meio centavo
  for k in [10, 99, 1234, 4999] do
    out := out.push (site "borda: meio centavo em 92,5%" (some (40 * k + 20)) 1000)
  -- custo ≡ 5 (mod 10) dá custo × 1,3 com meio centavo
  for k in [1, 6, 69, 1239, 2347] do
    out := out.push (site "borda: meio centavo no piso" (some 900000) (10 * k + 5))
    out := out.push (site "borda: meio centavo no piso, sem folga" (some (piso (10 * k + 5) + 1)) (10 * k + 5))
  -- piso encostado na referência, fator encostado no piso, referência pequena
  for c in [100, 1000, 23470] do
    for d in [-1, 0, 1, 2] do
      out := out.push (site "borda: piso encostado na referência" (some (piso c + d)) c)
  for r in [1, 490, 491, 540, 1000, 4003, 4004, 49634] do
    out := out.push (site "borda: referência pequena" (some r) 1)
  for c in [-1, 0, 1, 100, 124, 125, 126, 23470] do
    out := out.push (site "borda: sem anúncio" none c)
    out := out.push (site "borda: sem custo" (some 49634) c)
  out := out.push (site "borda: sem nada" none 0)
  return out.toList

def aleatorio (n : Nat) (g : Rng) : List J × Rng := Id.run do
  let mut g := g
  let mut out := #[]
  for _ in [0:n] do
    let (ml, g1) := g.entre 1 300000
    let (p, g2) := g1.entre 1 300000
    let (c, g3) := g2.entre (-10) 200000
    let (ref, g4) := g3.entre 1 300000
    let (semRef, g5) := g4.entre 0 9
    let (maior, g6) := g5.entre ml (ml * 3 / 2)
    out := out.push (guarda "aleatório" p c ml)
    out := out.push (irmaos "aleatório" p ml maior)
    out := out.push (site "aleatório" (if semRef = 0 then none else some ref) c)
    g := g6
  return (out.toList, g)

def arquivo (g : Rng) : String :=
  let (alea, _) := aleatorio 400 g
  let casos := bordaGuarda ++ bordaIrmaos ++ bordaSite ++ alea
  let guardaC := casos.filter fun j => match j with | .obj kv => kv.any (·.1 == "abaixo_do_custo") | _ => false
  let irmaosC := casos.filter fun j => match j with | .obj kv => kv.any (·.1 == "irmao_com_mesmo_preco") | _ => false
  let siteC := casos.filter fun j => match j with | .obj kv => kv.any (·.1 == "esperado") | _ => false
  "{\n\"fonte\": \"thiagopatzdorf/james-theorems Regras/Preco.lean (lake exe vetores)\",\n" ++
  "\"unidade\": \"centavos\",\n" ++
  "\"guarda\": " ++ linhas guardaC ++ ",\n\"irmaos\": " ++ linhas irmaosC ++ ",\n\"preco_do_site\": " ++ linhas siteC ++
  "\n}\n"

end Preco

/-! ## Etiqueta -/

namespace Etiqueta
open Regras.Etiqueta

def statusJ : Status → String
  | .pago => "paid" | .cancelado => "cancelled" | .reembolsado => "refunded"

def pacoteJ (origem : String) : Pacote → J
  | .livre q => .obj [("origem", .str origem), ("estado", .str "livre"), ("cotacao", .num q)]
  | .comprado p => .obj [("origem", .str origem), ("estado", .str "comprado"), ("preco", .num p)]
  | .comprandoRecente q => .obj [("origem", .str origem), ("estado", .str "comprando_recente"), ("cotacao", .num q)]
  | .comprandoVencida q none => .obj [("origem", .str origem), ("estado", .str "comprando_vencida"), ("cotacao", .num q),
      ("pago_na_loja", .null)]
  | .comprandoVencida q (some p) => .obj [("origem", .str origem), ("estado", .str "comprando_vencida"),
      ("cotacao", .num q), ("pago_na_loja", .num p)]

def resultadoJ : Resultado → J
  | .jaFeito => .str "ja_feito"
  | .comprada p => .obj [("comprada", .num p)]
  | .recuperada p => .obj [("recuperada", .num p)]
  | .teto => .str "teto"
  | .saldo => .str "saldo"
  | .emAndamento => .str "em_andamento"
  | .naoTentado => .str "nao_tentado"
  | .pulado => .str "pulado"

def origens : List String := ["palhoca", "rio"]

def pedidoJ (pd : Pedido) : J :=
  .obj [("status", .str (statusJ pd.status)), ("frete", .num pd.frete), ("total", .num pd.total),
        ("pacotes", .arr ((origens.zip pd.pacotes).map fun (o, pk) => pacoteJ o pk))]

def caso (origem : String) (saldo : Option Int) (pds : List Pedido) : J :=
  .obj [("origem", .str origem), ("saldo", match saldo with | some s => .num s | none => .null),
        ("pedidos", .arr (pds.map pedidoJ)),
        ("teto", .arr (pds.map fun pd => .num (teto pd.frete pd.total))),
        ("esperado", .arr ((rodada saldo pds).map fun rs => .arr (rs.map resultadoJ)))]

def pago (frete total : Int) (pks : List Pacote) : Pedido := ⟨.pago, frete, total, pks⟩

def borda : List J := [
  caso "borda: teto exato (frete 20 + 5)" (some 100000) [pago 2000 22000 [.livre 2500]],
  caso "borda: um centavo acima do teto" (some 100000) [pago 2000 22000 [.livre 2501]],
  caso "borda: frete grátis, 15% de R$ 220" (some 100000) [pago 0 22000 [.livre 3300], pago 0 22000 [.livre 3301]],
  caso "borda: frete grátis, meio centavo para o par" (some 100000) [pago 0 10010 [.livre 1502], pago 0 10030 [.livre 1504]],
  caso "borda: frete grátis, teto de R$ 100" (some 100000) [pago 0 200000 [.livre 10000], pago 0 200000 [.livre 10001]],
  caso "borda: dois pacotes passam do teto somados" (some 100000) [pago 3000 20000 [.livre 2400, .livre 1101]],
  caso "borda: dois pacotes, o segundo cabe exato" (some 100000) [pago 3000 20000 [.livre 2400, .livre 1100]],
  caso "borda: um já pago conta no teto" (some 100000) [pago 3000 20000 [.comprado 2400, .livre 1101]],
  caso "borda: um já pago, o outro cabe" (some 100000) [pago 3000 20000 [.comprado 2400, .livre 1100]],
  caso "borda: os dois já pagos" (some 100000) [pago 3000 20000 [.comprado 2400, .comprado 1100]],
  caso "borda: saldo exato" (some 2400) [pago 3000 20000 [.livre 2400]],
  caso "borda: saldo um centavo curto" (some 2399) [pago 3000 20000 [.livre 2400]],
  caso "borda: saldo acaba no segundo pacote e para a rodada" (some 3000)
    [pago 5000 20000 [.livre 2400, .livre 1000], pago 5000 20000 [.livre 100]],
  caso "borda: saldo acaba no primeiro pedido, o segundo nem é tentado" (some 500)
    [pago 5000 20000 [.livre 2400], pago 5000 20000 [.livre 100]],
  caso "borda: saldo negativo lido não tenta nada" (some (-1)) [pago 5000 20000 [.livre 100]],
  caso "borda: saldo zero" (some 0) [pago 5000 20000 [.livre 0], pago 5000 20000 [.livre 1]],
  caso "borda: saldo desconhecido não trava" none [pago 5000 20000 [.livre 2400, .livre 2000]],
  caso "borda: teto bloqueia antes do saldo" (some 100) [pago 1000 20000 [.livre 1600], pago 1000 20000 [.livre 50]],
  caso "borda: cancelado não compra" (some 100000) [⟨.cancelado, 2000, 22000, [.livre 100]⟩, pago 2000 22000 [.livre 100]],
  caso "borda: reembolsado não compra" (some 100000) [⟨.reembolsado, 2000, 22000, [.livre 100, .livre 100]⟩],
  caso "borda: compra em andamento não compra de novo" (some 100000) [pago 3000 20000 [.comprandoRecente 2400]],
  caso "borda: compra vencida já paga na loja é recuperada" (some 100000)
    [pago 3000 20000 [.comprandoVencida 2400 (some 2600), .livre 100]],
  caso "borda: compra vencida sem envio na loja compra" (some 100000) [pago 3000 20000 [.comprandoVencida 2400 none]],
  caso "borda: recuperada desconta do saldo da rodada" (some 3000)
    [pago 9000 20000 [.comprandoVencida 2400 (some 2600)], pago 9000 20000 [.livre 500]]
]

def estado (g : Rng) : Pacote × Rng :=
  let (k, g) := g.entre 0 9
  let (q, g) := g.entre 0 6000
  let (p, g) := g.entre 0 6000
  let (achou, g) := g.entre 0 1
  let pk := if k ≤ 4 then .livre q else if k ≤ 6 then .comprado p else if k = 7 then .comprandoRecente q
    else .comprandoVencida q (if achou = 0 then none else some p)
  (pk, g)

def pedidoAleatorio (g : Rng) : Pedido × Rng :=
  let (st, g) := g.entre 0 9
  let (gratis, g) := g.entre 0 3
  let (frete, g) := g.entre 1 6000
  let (total, g) := g.entre 0 90000
  let (n, g) := g.entre 1 2
  let (p1, g) := estado g
  let (p2, g) := estado g
  let status := if st = 0 then .cancelado else if st = 1 then .reembolsado else .pago
  (⟨status, if gratis = 0 then 0 else frete, total, if n = 1 then [p1] else [p1, p2]⟩, g)

def aleatorio (n : Nat) (g : Rng) : List J × Rng :=
  repetir n g fun g =>
    let (np, g) := g.entre 1 3
    let (conhecido, g) := g.entre 0 5
    let (s, g) := g.entre (-200) 12000
    let (a, g) := pedidoAleatorio g
    let (b, g) := pedidoAleatorio g
    let (c, g) := pedidoAleatorio g
    let pds := [a, b, c].take np.toNat
    (caso "aleatório" (if conhecido = 0 then none else some s) pds, g)

def arquivo (g : Rng) : String :=
  let (alea, _) := aleatorio 200 g
  "{\n\"fonte\": \"thiagopatzdorf/james-theorems Regras/Etiqueta.lean (lake exe vetores)\",\n" ++
  "\"unidade\": \"centavos\",\n\"casos\": " ++ linhas (borda ++ alea) ++ "\n}\n"

end Etiqueta

def main (args : List String) : IO Unit := do
  match args with
  | [preco, etiqueta] =>
    IO.FS.writeFile preco (Preco.arquivo ⟨20261126⟩)
    IO.FS.writeFile etiqueta (Etiqueta.arquivo ⟨20251125⟩)
  | _ => IO.eprintln "uso: lake exe vetores <preco.json> <etiqueta.json>"; IO.Process.exit 2
