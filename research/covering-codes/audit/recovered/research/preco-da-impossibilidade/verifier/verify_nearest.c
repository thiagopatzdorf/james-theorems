/* Verifier B (C): exhaustive nearest-codeword check, straight from the definition.
 *
 * For EVERY word w in Z_q^n (odometer enumeration) we look for a codeword at
 * Hamming distance <= R.  The last successful codeword is tried first (pure
 * speed heuristic; it cannot produce a false VERIFIED, since a hit is an
 * explicit witness).  Different algorithm and language from verify_cover.py.
 *
 * build: gcc -O2 -o verify_nearest verify_nearest.c
 * usage: verify_nearest Q N R CODEFILE      (exit 0 iff VERIFIED)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 24
#define MAXM 200000

static unsigned char C[MAXM][MAXN];

static int cmp_rows(const void *a, const void *b) { return memcmp(a, b, MAXN); }

int main(int argc, char **argv) {
    if (argc != 5) { fprintf(stderr, "usage: %s Q N R FILE\n", argv[0]); return 3; }
    int q = atoi(argv[1]), n = atoi(argv[2]), R = atoi(argv[3]);
    if (q < 2 || q > 10 || n < 1 || n > MAXN) { fprintf(stderr, "bad params\n"); return 3; }
    FILE *f = fopen(argv[4], "r");
    if (!f) { perror("open"); return 3; }
    char buf[256];
    int m = 0;
    while (fscanf(f, "%255s", buf) == 1) {
        if ((int)strlen(buf) != n) { printf("FAILED: bad length at word %d\n", m); return 2; }
        if (m >= MAXM) { printf("FAILED: too many words\n"); return 2; }
        memset(C[m], 0, MAXN);
        for (int j = 0; j < n; j++) {
            int d = buf[j] - '0';
            if (d < 0 || d >= q) { printf("FAILED: digit out of range at word %d\n", m); return 2; }
            C[m][j] = (unsigned char)d;
        }
        m++;
    }
    fclose(f);
    /* distinctness: sorted copy */
    unsigned char (*S)[MAXN] = malloc((size_t)m * MAXN);
    memcpy(S, C, (size_t)m * MAXN);
    qsort(S, m, MAXN, cmp_rows);
    for (int i = 1; i < m; i++)
        if (!memcmp(S[i - 1], S[i], MAXN)) { printf("FAILED: duplicate word\n"); return 2; }
    free(S);

    unsigned char w[MAXN];
    memset(w, 0, sizeof w);
    unsigned long long total = 0, uncovered = 0;
    int last = 0;
    for (;;) {
        total++;
        int ok = 0;
        for (int t = 0; t < m && !ok; t++) {
            int i = t == 0 ? last : (t <= last ? t - 1 : t);
            int dist = 0;
            for (int j = 0; j < n; j++) dist += (C[i][j] != w[j]);
            if (dist <= R) { ok = 1; last = i; }
        }
        if (!ok) uncovered++;
        int j = 0;
        while (j < n && ++w[j] == q) { w[j] = 0; j++; }
        if (j == n) break;
    }
    printf("%s impl=nearest-c q=%d n=%d R=%d words=%d space=%llu uncovered=%llu\n",
           uncovered == 0 ? "VERIFIED" : "FAILED", q, n, R, m, total, uncovered);
    return uncovered == 0 ? 0 : 1;
}
