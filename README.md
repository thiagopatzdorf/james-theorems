# james-theorems

Provas formais, em **Lean 4**, dos três pilares da filosofia do James.
Fase 1 do [manifesto matemático](https://claude.ai/artifact/6sWJemMGB3QQScEjFGA9j4).

Sem Mathlib, sem `sorry`. Os teoremas dependem apenas dos axiomas padrão do
Lean (`propext`, `Quot.sound`), conferidos em CI por `Axiomas.lean`.

```
lake build
lake env lean Axiomas.lean
```

## Os três pilares

| Pilar | Arquivo | Teorema | O que diz |
|---|---|---|---|
| **Conhecimento** | `Conhecimento.lean` | `amortizacao` | Partindo de base vazia, o número de buscas é **exatamente** o número de tarefas distintas, e o custo total é `D · busca + N · verificação`. Se `D` cresce mais devagar que `N`, o custo por tarefa tende ao custo de verificar: `O(n) → O(1)` amortizado. |
| **Segurança** | `Seguranca.lean` | `gate` | Para **qualquer** log de eventos, inclusive adversário, nenhuma ação crítica aparece executada sem aprovação registrada. |
| **Alma** | `Alma.lean` | `replay`, `retomada`, `revezamento` | O estado é função do log, não do host. Um corpo pode morrer em qualquer evento e outro retoma do snapshot; o log pode ser dividido entre quaisquer corpos. `rm -rf <host>` não destrói o James. |

## Descobrir é caro, verificar é barato

Escrever estas provas foi busca. Conferi-las é o kernel do Lean, em milissegundos.
O repositório é a filosofia do James aplicada a si mesma.

## Fronteira

Os teoremas valem para os **modelos** definidos aqui, não para o código de produção.
Eles dizem: *se* o sistema se comporta como o modelo, *então* as propriedades valem.
Medir se o sistema real se comporta como o modelo é a Fase 2: exportar logs reais da
Factory e checar o modelo contra eles, transformando cada divergência em teste que falha.

## Roadmap

- **Fase 0** · manifesto matemático ✔
- **Fase 1** · os três pilares provados em Lean ✔
- **Fase 2** · ancorar no código real: validação de traços contra logs da Factory
- **Fase 3** · o James escreve as próprias provas, e o kernel verifica

## CI

O workflow está em `ci/lean.yml`. Para ativar, mova para `.github/workflows/lean.yml`
(o token usado na criação do repositório não tinha permissão de `workflow`).
