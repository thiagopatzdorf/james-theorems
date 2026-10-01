# Preço da impossibilidade: laboratório covering codes

Estrutura auditável: aritmética exata, proveniência, certificados com dois verificadores, harness de falsificação. Leia `REPORT.md` primeiro; o veredito está em `PRICE_OF_IMPOSSIBILITY.md` seção 11.

## Construir e rodar (a partir desta pasta)

```
gcc -O2 -o bin/verify_nearest verifier/verify_nearest.c
gcc -O2 -o bin/exact_K        verifier/exact_K.c
python scripts/certify.py            # roda os dois verificadores nos 8 códigos e escreve data/certificates/
python scripts/audit.py              # recalcula a tabela (AUDIT_TABLE.md, data/audit_table.json)
python hypotheses/search.py          # re-testa as hipóteses contra a tabela exata e escreve registry.json
python -m pytest -q                  # 75 testes
```

Em Windows os binários são `bin/*.exe`; os testes e scripts os localizam sozinhos. Sem os binários, os testes que dependem deles são **pulados** (skip), não aprovados: construa antes, senão "75 passed" não vale (confira que a contagem de skips é 0). `bin/` não é versionado.

Regenerar a tabela exata de células pequenas (leva minutos): `python hypotheses/build_exact_table.py [segundos_por_célula]`.

## Mapa

| caminho | o que é |
|---|---|
| `src/impossibility/covering.py` | `sphere_volume`, `sphere_bound`, `alpha`, `alpha_interval`, `additive_gap`, `additive_gap_interval` (inteiros/`Fraction`, sem float no caminho de decisão) |
| `src/impossibility/provenance.py` | 6 status, `Claim`, `effective_status` (elo mais fraco), `validate` (re-hash dos certificados) |
| `schema/claim.schema.json` | schema gerado dos enums Python |
| `verifier/verify_cover.py`, `verify_nearest.c` | verificadores A e B (algoritmos e linguagens distintos) |
| `verifier/exact_K.c` | oráculo exaustivo de K para q^n ≤ 1024 |
| `data/` | códigos, `cells.json`, certificados, claims, literatura, tabela de auditoria |
| `hypotheses/` | tabela exata, harness, registro (refutadas preservadas) |
| `tests/` | 75 testes |

Limite de escopo: este diretório **não** contém o gerador que produziu os 8 códigos (ele vive em `coldcase`, referenciado por `source_commit` em cada certificado). Os códigos se verificam, mas a busca não é reprodutível a partir daqui.
