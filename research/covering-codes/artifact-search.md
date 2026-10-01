# Original artifact recovery — bounded search, 2026-10-01

Outcome: **ALL EIGHT ORIGINAL-SOURCE FILES RECOVERED** from Factory branch
`research/preco-da-impossibilidade`, commit `e7f3ed9c52e6992eaa244fc75a04ed4abed89fd1`.
The initial missing-artifact diagnosis was superseded after deterministic enumeration
of 506 remote refs found that research branch. `audit/recovered/index.json` records
Git blob identities and exact byte hashes; all candidate files are preserved twice
(original-source archive and canonical certificate directory). No replacement code
was searched for or generated.

For the principal original-order LF bytes, SHA-256 is
`6d1b0e1abb8079df06a28d5301607d3d5247e0f2005d72e13f695ce26f6e6b52`.
Converting those bytes to CRLF reproduces the previous raw-file hash
`c644bdfe354d74941eb6276d16f6a361544e4db2d97005977df2ffd8ea1a5fae`;
sorting LF lines reproduces the old certificate hash
`54dbdade1337432303847d2fd0d1c13b506de08ba518e1694c5fb37ed0e81162`.
These comparisons establish consistency with the archived report. The reconstructed
CRLF/sorted variants are not substituted for the canonical file. Original generator
revision and seed remain unknown for the principal code.

## Initial negative searches (retained as search provenance)

## Sources checked

1. Entire `research/covering-codes/` at initial commit
   `c2806d9af1864ffea519c0a6f4bb9bccc21a5c94`: only status, certificate placeholder,
   candidate adapters and preprint README. No `.tex`, PDF, construction or external
   certificate was versioned. The prior draft says a PDF existed elsewhere; that
   sentence is not a PDF artifact.
2. Both primary repository branches fetched (`main` and the research branch),
   all nine reachable initial commits and their changed-file paths. No code file.
   Primary Actions API reported zero workflow runs. No original Actions artifact
   exists in that inspected run collection.
3. Connected GitHub code searches for `pp1` and `1351`, and commit searches for
   `covering`, `1351`, `pp1` in the principal and Factory repositories. Search
   indexing and query scope limit negative results. Returned unrelated shopping
   product/old merge names are not construction evidence.
4. Full untruncated current Factory tree; default trees of connected `james`,
   `JamesCoder`, `James.V1` repositories. No relevant filenames. Remote Factory
   ref names were separately enumerated for research/covering names; this is not
   a content audit of every remote branch.
5. Local `/workspace`, `/tmp`, `/home/agent` filename searches. This workspace
   contains the previous Genesis task, not a covering-code search run.
6. Live MCP read-only access to **factory-01**, user worker: Python filesystem
   walk of `/tmp`, `/var/tmp`, `/home/worker`, `/opt`, `/srv`, `/workspace`, pruning
   dependency/cache directories; deterministic basename search for pp1, 1351,
   covering, q7/n9 and chk. Only unrelated browser checks/plugin documentation
   and a cache hash matched. No original code.
7. Factory's locally reachable Git refs/history/path search, then targeted
   transcript/text search. Final scan checked five Codex session files, two
   Claude project files, eight Factory state files and 14,882 files in `/tmp`.
   Two Factory state matches are this audit's own MCP command logging; they
   are not earlier generator output. Final command stderr was empty.

The first host transcript command used `rg`, which is unavailable there. Its
negative output is **discarded**; the replacement uses Python and grep. The
first broad path search was noisy with pnpm cache hashes and bounded at 250
hits/root; the pruned deterministic replacement is the useful evidence.

## Limits and provenance

See `audit/github-recovery.json`, `factory-path-search.json`,
`factory-recovery-final.json` and `factory-remote-refs.json` for evidence.
We did not claim a search of inaccessible home directories, deleted temporary
files, expired Actions artifacts, every historical branch in every connected
repository, or unidentified machines. No generation host, run ID, exact pp1
filename, seed or generator was present in the audited initial files.

## Resolution

See audit/factory-remote-refs.json and audit/recovered/index.json. Negative default-branch, host and transcript searches did not justify a final absence claim; the remote research ref contained all eight artifacts.
