# Relatório final

Data: 2026-10-01. Tudo abaixo está em `research/preco-da-impossibilidade/` e é reproduzível pelo `README.md`. `75 passed, 0 skipped` com os binários construídos.

## 1. O que sobreviveu

- **As 8 construções (K5(7,2)≤500, K4(10,4)≤192, K5(9,3)≤1250, K5(10,4)≤625, K5(9,5)≤50, K5(9,4)≤250, K7(8,3)≤1893, K7(9,4)≤1351)** cobrem o espaço inteiro: verificado por dois verificadores independentes (marcação de bolas em Python; vizinho mais próximo exaustivo em C). Tamanho ≥ ceil(S) em todas.
- **Todos os números de literatura** (Kéri; Gijswijt–Polak; Marosi) foram conferidos contra os PDFs primários; 21 LITERATURE_CLAIM com fonte.
- **Aritmética exata** (V, S, ceil S, α, lacuna aditiva, intervalos) recalculada do zero; sem floats na decisão. Oráculo exaustivo reproduz K_2(n,1) conhecidos.
- **Estrutura epistêmica**: 6 status com "elo mais fraco", certificados com hash canônico, α e Π₊ sempre como intervalo `[melhor lb, melhor ub verificado]`.
- **Hipótese H4** (α<2 em binário) e **H6** (V divide q^n ⇒ perfeito) sobrevivem à grade de células pequenas (q^n ≤ 1024). **Sem valor de evidência**: H6 é falsa em (2,90,2) segundo a literatura.

## 2. O que foi refutado (preservado em `hypotheses/registry.json`)

| id | afirmação | contraexemplo exato |
|---|---|---|
| H1 | α não crescente em n | `(q,n,R)=(2,3,1)→(2,4,1)`: α 1 → 5/4 |
| H2 | lacuna aditiva não decrescente em n | `(2,6,1)→(2,7,1)`: 2 → 0 |
| H3 | α < 2 sempre | `(3,3,2)`: K=3, V=19, α=19/9 |
| H5 | `K=ceil S` ⇔ `V` divide `q^n` | `(2,2,1)`: K=2=ceil(4/3) e V=3 não divide 4 (**hipótese mal formulada**: confunde ceil com igualdade exata; mantida como exemplo de enunciado ruim) |
| — | "Preço da impossibilidade" como quantidade intrínseca e monótona | refutado por H1+H2; ver `PRICE_OF_IMPOSSIBILITY.md` §6 |

Controles (teoremas que o harness **não** deve refutar): K monótono em n, K monótono em q, K(n+1,R+1) ≤ K(n,R). Os três passaram; se algum falhasse seria bug do harness.

## 3. Erros encontrados (meus e de premissas)

1. **V_7(8,3) citado de memória errado**: 13161 e S=438,03; os valores corretos são 13153 e 438,29 (ceil 439). Os testes agora usam aritmética à mão. **Regra: números de memória precisam ser recomputados.**
2. **Premissa antiga incorreta**: "K4(7,3) ≤ 31" aparecia como fato numa fase anterior; foi derrubada na verificação.
3. **Hash fabricado**: um sha256 de preenchimento digitado à mão foi pego e substituído por hash calculado. Regra: hash só sai de código.
4. **Semântica das chaves de Kéri** lida errada no modo `-layout` do pdftotext; o modo `-raw` está correto (o=1999, m=1991 no arquivo 4–5).
5. **Teste tautológico** (α "não limitado") substituído pela identidade exata K_q(n,n−1)=q.
6. **Força bruta em Python travou** em K2(6,1); Python só para n ≤ 5, oráculo em C para n ≥ 6.
7. **K7(8,3)**: histórico 2290 → 2058/2001 → 1893; só 1893 tem certificado verificado; os anteriores não são citados como resultado.
8. **K4(10,4)**: o lb de GP (62) supera o de Kéri (59); a tabela usa o melhor e guarda os dois.
9. Esta sessão: um teste meu continha um comentário de rascunho e `or True`; foi removido antes de entrar (agora compara frações exatas).

## 4. Afirmações ainda não verificadas

- **Novidade** das 8 construções: UNKNOWN. Cada uma está abaixo do ub registrado nas tabelas que li, mas não foram checadas versões novas das tabelas, tabelas de códigos lineares de cobertura nem a literatura posterior. Marosi registra K7(9,4) ≤ 1475; nossa construção dá 1351 (menor), ainda assim sem afirmar novidade.
- Golay (2,90,2) e as linhas de `GENERALIZATION_MATRIX.md` fora do laboratório: conhecimento geral, sem citação.
- Valor de C(ε) para ε>0: não calculado em nenhuma célula.
- O gerador dos 8 códigos não está neste repositório (referência: `coldcase` 56a8cce…); a busca não é reproduzível daqui.

## 5. Resposta curta à pergunta central

"Preço matemático da impossibilidade" é em essência **gap, razão de aproximação, função valor e taxa–distorção** sob outro nome; não há teorema novo. O que sobrevive é o protocolo de auditoria (intervalos, proveniência, certificados, refutações preservadas). Detalhe e justificativa: `PRICE_OF_IMPOSSIBILITY.md` §11.

## 6. Próxima experiência de maior informação por custo

**Busca de prior art das 8 células contra as tabelas atuais** (Kéri, versão mais nova; tabelas de cobertura lineares; arXiv posterior). Custo: leitura, zero computação pesada. Informação: converte `novelty_status` de UNKNOWN para um valor decidível em 8 afirmações de uma vez, e decide se a opção A (novo upper bound) é publicável. Sem isso, qualquer busca nova de construção é gasto às cegas.

Só depois, e só se ao menos uma célula for nova, escolher **uma** célula para atacar. Hipótese (não medida, sem probabilidade): K5(10,4), porque é onde a nossa construção mais se afasta do ub registrado (875 → 625, −29%), o que sugere que o ub da literatura ali está menos otimizado; K7(8,3) (2337 → 1893, −19%) é a seguinte.

## 7. Decisões que tomei sozinho

- Usar **o melhor lb registrado** (GP onde ≥ Kéri) e guardar ambos.
- Manter H5 mesmo mal formulada, como exemplo de enunciado refutado.
- Tratar H4/H6 como "sobrevive à grade", nunca como suporte.
- Não gastar computação pesada; células abertas do oráculo ficam abertas.
- Não afirmar novidade em nenhuma linha.
- Usar português nos entregáveis, porque o pedido foi em português.
