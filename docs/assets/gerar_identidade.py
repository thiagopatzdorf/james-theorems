#!/usr/bin/env python3
"""Gera a identidade visual do repositório em docs/assets/.

Adaptado do gerador do repositório Matematica (mesma paleta, mesma tipografia, mesmo método), para que os
dois repositórios se leiam como uma família. Duas famílias de peça:

* Diagramas em SVG (a fita de von Neumann e a equação do James): nítidos em qualquer tela. O texto vira
  contorno (path), porque SVG dentro de <img> no GitHub não carrega webfont; cada glifo é definido uma vez
  em <defs> e reaproveitado com <use>, o que mantém cada arquivo < 60 KB. Cada SVG tem <title> e <desc>.
* Banner (claro e escuro) e social preview em PNG: uma cena WebGL (three.js) em cena/fita.html, em que
  símbolos soltos pousam nas células de uma fita luminosa que se enrola numa espiral até um único ponto de
  ouro (o log que se dobra em estado), retratada no Chromium headless e quantizada para 256 cores.

Fontes: Cormorant Garamond e, só para as letras gregas, EB Garamond (as duas SIL Open Font License 1.1),
dos pacotes @fontsource; three.js (MIT) do pacote npm `three`. Tudo é baixado num cache temporário, fixado
por versão; nada entra no repositório. Converter glifos em contorno é uso permitido pela OFL.

Uso (precisa de rede na primeira vez):

    pip install fonttools uharfbuzz cairosvg playwright pillow
    python3 docs/assets/gerar_identidade.py              # escreve todas as peças de SAIDAS
    python3 docs/assets/gerar_identidade.py --so-svg     # só os SVG (sem navegador)
    python3 docs/assets/gerar_identidade.py --previa D   # também renderiza PNG de cada SVG em D

O navegador é o Chromium do Playwright; se a versão instalada do Playwright não casar com a do navegador
baixado, aponte o executável em CHROMIUM_PATH.

Inversa: os arquivos gerados são só os listados em SAIDAS; apagar é `git rm` deles.
"""

from __future__ import annotations

import argparse
import os
import random
import tempfile
import urllib.request
from pathlib import Path

AQUI = Path(__file__).resolve().parent
VERSAO_FONTE = "5.3.0"
URL_FONTE = ("https://cdn.jsdelivr.net/npm/@fontsource/cormorant-garamond@{v}/files/"
             "cormorant-garamond-latin-{peso}-{estilo}.woff")
# Cormorant Garamond não tem grego; Φ, Δ e δ vêm do subconjunto grego da EB Garamond (mesma família
# tipográfica, OFL 1.1), escolhida caractere a caractere pela cobertura da fonte, nunca à mão.
URL_GREGO = ("https://cdn.jsdelivr.net/npm/@fontsource/eb-garamond@{v}/files/"
             "eb-garamond-greek-{peso}-{estilo}.woff")
PESOS = {"r": ("400", "normal"), "m": ("500", "normal"), "sb": ("600", "normal"),
         "i": ("400", "italic"), "mi": ("500", "italic"),
         "gr": ("400", "normal", "grego"), "gi": ("400", "italic", "grego")}
RESERVA = {"r": "gr", "m": "gr", "sb": "gr", "i": "gi", "mi": "gi"}
SAIDAS = ("fita-von-neumann.svg", "equacao.svg", "banner-claro.png", "banner-escuro.png", "social-preview.png")
VERSAO_THREE = "0.170.0"
ARQUIVOS_THREE = ["build/three.module.js"] + [f"examples/jsm/postprocessing/{n}.js" for n in (
    "EffectComposer", "RenderPass", "UnrealBloomPass", "OutputPass", "Pass", "ShaderPass", "MaskPass")] + [
    f"examples/jsm/shaders/{n}.js" for n in ("CopyShader", "LuminosityHighPassShader", "OutputShader")]

# Os contornos são gravados em múltiplos de QUANTUM unidades da fonte (1000 por em), o que encurta
# cada número. Títulos (peso m) usam 3 unidades: 0,4 px no maior (132 px, só no PNG). Texto (r, i) nunca
# passa de ~40 px e usa 6 unidades: 0,24 px nesse tamanho, invisível.
QUANTUM = {"r": 6, "i": 6, "m": 3, "mi": 3, "sb": 3, "gr": 3, "gi": 3}

# Paleta idêntica à do repositório Matematica (e da página genesisinnovation.io/matematica): marfim #F6F1E7, grafite #141414, ouro #B8975A.
# "ouro" é o fio fino (traços e esferas); "ourotx" é o mesmo ouro escurecido/clareado para texto pequeno,
# porque #B8975A sobre marfim dá só ~2,4:1 de contraste e legenda precisa de >= 4,5:1.
TEMAS = {
    "claro": {"fundo": "#F6F1E7", "tinta": "#141414", "suave": "#5C564C", "fraco": "#E0D7C4",
              "ouro": "#B8975A", "ouro2": "#B8975A", "ourotx": "#7A5F2F"},
    "escuro": {"fundo": "#141414", "tinta": "#F6F1E7", "suave": "#A9A193", "fraco": "#2B2926",
               "ouro": "#B8975A", "ouro2": "#B8975A", "ourotx": "#C9AB72"},
}

# --------------------------------------------------------------------------------------------
# Tipografia: texto -> contornos reaproveitáveis
# --------------------------------------------------------------------------------------------

def _cache_fontes() -> Path:
    # mesmo cache do gerador do Matematica: quem já gerou lá não baixa de novo
    d = Path(os.environ.get("MATEMATICA_CACHE_FONTES", Path(tempfile.gettempdir()) / "matematica-fontes"))
    d.mkdir(parents=True, exist_ok=True)
    return d


def _baixar(peso: str, estilo: str, familia: str = "cg") -> Path:
    destino = _cache_fontes() / f"{'ebg' if familia == 'grego' else 'cg'}-{VERSAO_FONTE}-{peso}-{estilo}.woff"
    if not destino.exists():
        url = (URL_GREGO if familia == "grego" else URL_FONTE).format(v=VERSAO_FONTE, peso=peso, estilo=estilo)
        with urllib.request.urlopen(url, timeout=60) as r:  # noqa: S310 (URL fixa)
            destino.write_bytes(r.read())
    return destino


class Tipografo:
    """Converte texto em <use> de glifos definidos uma vez por documento."""

    def __init__(self) -> None:
        import uharfbuzz as hb
        from fontTools.ttLib import TTFont

        self.hb = hb
        self.fontes = {}
        for chave, (peso, estilo, *familia) in PESOS.items():
            caminho = _baixar(peso, estilo, *familia)
            tt = TTFont(str(caminho))
            tt.flavor = None
            import io
            buf = io.BytesIO()
            tt.save(buf)
            dados = buf.getvalue()
            face = hb.Face(dados)
            fonte = hb.Font(face)
            self.fontes[chave] = (tt, fonte, tt.getGlyphSet(), tt["head"].unitsPerEm, tt.getGlyphOrder())
        self.mapas = {k: v[0].getBestCmap() for k, v in self.fontes.items()}
        self.usados: dict[str, str] = {}
        self.ids: dict[tuple[str, int], str] = {}

    def _gid(self, chave: str, gid: int) -> str:
        from fontTools.pens.recordingPen import DecomposingRecordingPen

        chave_glifo = (chave, gid)
        if chave_glifo in self.ids:
            return self.ids[chave_glifo]
        # id curto (a, b, ..., Z, aa, ab...): cada glifo é referido centenas de vezes por arquivo
        nome = _id_curto(len(self.ids))
        self.ids[chave_glifo] = nome
        if nome not in self.usados:
            tt, _f, gs, _u, ordem = self.fontes[chave]
            pen = DecomposingRecordingPen(gs)
            gs[ordem[gid]].draw(pen)
            self.usados[nome] = _caminho_compacto(pen.value, QUANTUM[chave])
        return nome

    def _shape(self, texto: str, chave: str, tracking: float = 0.0):
        _tt, fonte, _gs, upem, _o = self.fontes[chave]
        buf = self.hb.Buffer()
        buf.add_str(texto)
        buf.guess_segment_properties()
        self.hb.shape(fonte, buf, {"kern": True, "liga": True, "lnum": True})
        glifos, x = [], 0.0
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            glifos.append((info.codepoint, x + pos.x_offset))
            x += pos.x_advance + tracking * upem
        if glifos and tracking:
            x -= tracking * upem
        return glifos, x, upem

    def largura(self, texto: str, tamanho: float, chave: str = "r", tracking: float = 0.0) -> float:
        partes = self._partes(texto, chave)
        total = 0.0
        for t, k in partes:
            _g, x, upem = self._shape(t, k, tracking)
            total += x * tamanho / upem
        return total

    def _partes(self, texto: str, chave: str):
        """`*itálico*` troca para o itálico do peso; caractere que a fonte não tem cai na fonte de reserva."""
        saida = []
        for t, k in self._partes_italico(texto, chave):
            for ch in t:
                kk = k if ord(ch) in self.mapas[k] or ch == " " else RESERVA.get(k, k)
                if saida and saida[-1][1] == kk:
                    saida[-1] = (saida[-1][0] + ch, kk)
                else:
                    saida.append((ch, kk))
        return saida

    @staticmethod
    def _partes_italico(texto: str, chave: str):
        ital = {"r": "i", "m": "mi", "sb": "mi", "i": "r", "mi": "m", "gr": "gi", "gi": "gr"}[chave]
        partes, atual, em = [], "", False
        for c in texto:
            if c == "*":
                if atual:
                    partes.append((atual, ital if em else chave))
                atual, em = "", not em
            else:
                atual += c
        if atual:
            partes.append((atual, ital if em else chave))
        return partes

    def texto(self, texto: str, x: float, y: float, tamanho: float, chave: str = "r",
              cor: str = "currentColor", ancora: str = "start", tracking: float = 0.0,
              opacidade: float | None = None, extra: str = "") -> str:
        w = self.largura(texto, tamanho, chave, tracking)
        if ancora == "middle":
            x -= w / 2
        elif ancora == "end":
            x -= w
        # um grupo por trecho (redondo / itálico): cada fonte tem o seu QUANTUM e, portanto, a sua escala
        grupos, cursor = [], 0.0
        for t, k in self._partes(texto, chave):
            glifos, avanco, upem = self._shape(t, k, tracking)
            q = QUANTUM[k]
            usos = [f'<use href="#{self._gid(k, gid)}" x="{round(gx / q)}"/>'.replace(' x="0"', '')
                    for gid, gx in glifos if self.fontes[k][4][gid] not in ("space", "uni00A0", ".notdef")]
            if usos:
                s = tamanho / upem * q
                gx0 = x + cursor * tamanho / upem
                grupos.append(f'<g transform="translate({gx0:.1f} {y:.1f}) scale({s:.4f} {-s:.4f})">'
                              + "".join(usos) + "</g>")
            cursor += avanco
        if not grupos:
            return ""
        op = f' opacity="{opacidade:g}"' if opacidade is not None else ""
        return f'<g fill="{cor}"{op}{extra}>' + "".join(grupos) + "</g>"

    def paragrafo(self, texto: str, x: float, y: float, largura_max: float, tamanho: float,
                  entrelinha: float, **kw) -> tuple[str, float]:
        """Quebra por largura medida (não por número de caracteres) e devolve (svg, y_final)."""
        palavras, linhas, atual = texto.split(), [], ""
        chave = kw.get("chave", "r")
        for p in palavras:
            cand = f"{atual} {p}".strip()
            # o asterisco é marcação; medir com ele aberto/fechado dá a largura certa por parte
            if self.largura(_fecha(cand), tamanho, chave) <= largura_max or not atual:
                atual = cand
            else:
                linhas.append(atual)
                atual = p
        if atual:
            linhas.append(atual)
        # reabre itálico que atravessa a quebra de linha
        out, aberto = [], False
        for linha in linhas:
            if aberto:
                linha = "*" + linha
            aberto = linha.count("*") % 2 == 1
            out.append(_fecha(linha))
        svg = "".join(self.texto(linha, x, y + i * entrelinha, tamanho, **kw) for i, linha in enumerate(out))
        return svg, y + (len(out) - 1) * entrelinha

    def defs(self) -> str:
        return "".join(f'<path id="{k}" d="{d}"/>' for k, d in sorted(self.usados.items()))

    def reiniciar(self) -> None:
        self.usados, self.ids = {}, {}


_LETRAS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _id_curto(n: int) -> str:
    if n < len(_LETRAS):
        return _LETRAS[n]
    return _id_curto(n // len(_LETRAS) - 1) + _LETRAS[n % len(_LETRAS)]


def _num(v: float) -> str:
    return str(round(v))


def _par(dx: float, dy: float) -> str:
    a, b = _num(dx), _num(dy)
    return a + ("" if b.startswith("-") else " ") + b


def _caminho_compacto(cmds, q: int) -> str:
    """Serializa os contornos em comandos relativos e inteiros: ~40% menor que o SVGPathPen absoluto.

    Quadráticas encadeadas do TrueType (vários pontos fora da curva) viram uma sequência de q com o ponto
    médio implícito explicitado, que é o que a especificação do formato define.
    """
    out, cx, cy, sx, sy = [], 0, 0, 0, 0
    for op, pts in cmds:
        # arredonda no absoluto antes de diferenciar: assim o erro não se acumula ao longo do contorno
        pts = tuple(None if p is None else (round(p[0] / q), round(p[1] / q)) for p in pts)
        if op == "moveTo":
            (x, y), = pts
            out.append("m" + _par(x - cx, y - cy))
            cx, cy, sx, sy = x, y, x, y
        elif op == "lineTo":
            (x, y), = pts
            out.append("l" + _par(x - cx, y - cy))
            cx, cy = x, y
        elif op == "qCurveTo":
            pts = list(pts)
            if pts[-1] is None:  # contorno só de pontos fora da curva
                pts = pts[:-1]
                pts.append((round((pts[-1][0] + pts[0][0]) / 2), round((pts[-1][1] + pts[0][1]) / 2)))
            controles, fim = pts[:-1], pts[-1]
            for k, c in enumerate(controles):
                if k + 1 < len(controles):
                    n = controles[k + 1]
                    e = (round((c[0] + n[0]) / 2), round((c[1] + n[1]) / 2))
                else:
                    e = fim
                out.append("q" + _par(c[0] - cx, c[1] - cy) + " " + _par(e[0] - cx, e[1] - cy))
                cx, cy = e
        elif op == "curveTo":
            c1, c2, e = pts
            out.append("c" + " ".join(_par(p[0] - cx, p[1] - cy) for p in (c1, c2, e)))
            cx, cy = e
        elif op in ("closePath", "endPath"):
            out.append("z")
            cx, cy = sx, sy
    return "".join(out).replace(" -", "-")


def _fecha(s: str) -> str:
    return s + "*" if s.count("*") % 2 else s


def documento(tip: Tipografo, w: int, h: int, titulo: str, desc: str, corpo: str, defs: str = "") -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="titulo descricao">'
            f'<title id="titulo">{titulo}</title><desc id="descricao">{desc}</desc>'
            f'<defs>{tip.defs()}{defs}</defs>{corpo}</svg>\n')



def _cartao(W: int, H: int, c: dict) -> str:
    return (f'<rect width="{W}" height="{H}" rx="20" fill="{c["fundo"]}"/>'
            f'<rect x="12.5" y="12.5" width="{W - 25}" height="{H - 25}" rx="12" fill="none" '
            f'stroke="{c["fraco"]}"/>')


def _seta(x1: float, y: float, x2: float, cor: str) -> str:
    """Seta horizontal fina, ponta aberta (a fonte não tem os glifos de seta)."""
    return (f'<path d="M{x1:.0f} {y:.0f} H{x2:.0f} m-7 -5 l7 5 l-7 5" fill="none" stroke="{cor}" '
            f'stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>')


# --------------------------------------------------------------------------------------------
# Peças em SVG
# --------------------------------------------------------------------------------------------

# Conferido contra a tabela da §3.2 e da §3.3 do MANIFESTO.md: (símbolo, componente, função, papel, artefato)
COMPONENTES = [
    ("A", "construtor universal", "dada uma descrição Φ(X), constrói X", "núcleo", "factory-maquina.py"),
    ("B", "copiador", "copia Φ(X) sem interpretar", "replicação", "git"),
    ("C", "controle", "coordena A e B", "coordenação", "James · Maestro · fila"),
    ("Φ", "fita", "a descrição, fora do construtor", "descrição versionada",
     "factory.manifest.json, código, testes, CLAUDE.md, memória"),
]


def fita_von_neumann(tip: Tipografo) -> str:
    tip.reiniciar()
    c = TEMAS["claro"]
    W, H = 1280, 740
    t = [_cartao(W, H, c)]
    t.append(tip.texto("A MÁQUINA E A FITA", 72, 82, 14, "m", c["ourotx"], tracking=0.24))
    t.append(tip.texto("Construtor, copiador, controle e fita", 72, 128, 44, "r", c["tinta"]))
    t.append(tip.texto("Von Neumann (1966) à esquerda, a Factory à direita: uma correspondência de arquitetura, "
                       "não um teorema.", 72, 162, 18, "r", c["suave"]))
    xd = 744
    t.append(tip.texto("VON NEUMANN", 72, 222, 13, "m", c["ourotx"], tracking=0.24))
    t.append(tip.texto("FACTORY", xd, 222, 13, "m", c["ourotx"], tracking=0.24))
    t.append(f'<line x1="72" y1="238" x2="{W - 72}" y2="238" stroke="{c["fraco"]}" stroke-width="1"/>')
    y0, dy = 284, 80
    for k, (simb, nome, funcao, papel, artefato) in enumerate(COMPONENTES):
        y = y0 + k * dy
        t.append(tip.texto(f"*{simb}*", 96, y + 8, 40, "r", c["ourotx"], ancora="middle"))
        t.append(tip.texto(nome, 140, y, 25, "r", c["tinta"]))
        t.append(tip.texto(f"*{funcao}*" if k < 3 else funcao, 140, y + 27, 17, "r", c["suave"]))
        t.append(f'<line x1="560" y1="{y - 2}" x2="{xd - 40}" y2="{y - 2}" stroke="{c["fraco"]}" '
                 f'stroke-width="1.2" stroke-dasharray="3 5"/>')
        t.append(f'<circle cx="560" cy="{y - 2}" r="2.6" fill="{c["ouro"]}"/>')
        t.append(_seta(xd - 52, y - 2, xd - 24, c["ouro"]))
        t.append(tip.texto(papel, xd, y, 25, "r", c["tinta"]))
        t.append(tip.texto(artefato, xd, y + 27, 17, "r", c["suave"]))
    # a fita: uma tira de células com símbolos; uma célula em ouro é a mutação Δ (um PR mergeado)
    yf, hf, x0, n = 616, 44, 72, 26
    wc = (W - 2 * x0) / n
    rnd = random.Random(1966)
    muta = 17
    simbolos = "".join(rnd.choice("0101010101eSFXLK") for _ in range(n))
    t.append(f'<rect x="{x0}" y="{yf}" width="{W - 2 * x0}" height="{hf}" fill="{c["fraco"]}" opacity=".35"/>')
    t.append(f'<rect x="{x0 + muta * wc:.1f}" y="{yf}" width="{wc:.1f}" height="{hf}" fill="{c["ouro"]}" '
             f'opacity=".28"/>')
    t.append(f'<g stroke="{c["tinta"]}" stroke-width="1" fill="none">'
             f'<rect x="{x0}" y="{yf}" width="{W - 2 * x0}" height="{hf}"/>'
             + "".join(f'<line x1="{x0 + i * wc:.1f}" y1="{yf}" x2="{x0 + i * wc:.1f}" y2="{yf + hf}"/>'
                       for i in range(1, n)) + "</g>")
    t.append(f'<rect x="{x0 + muta * wc:.1f}" y="{yf}" width="{wc:.1f}" height="{hf}" fill="none" '
             f'stroke="{c["ourotx"]}" stroke-width="2"/>')
    for i, s in enumerate(simbolos):
        txt = f"*{s}*" if s.isalpha() else s
        t.append(tip.texto(txt, x0 + (i + .5) * wc, yf + 30, 22, "r", c["ourotx"] if i == muta else c["tinta"],
                           ancora="middle"))
    xm = x0 + (muta + .5) * wc
    t.append(tip.texto("Δ · uma mutação da fita = um PR mergeado", xm, yf - 14, 16, "r", c["ourotx"],
                       ancora="middle"))
    t.append(tip.texto("*Φ*", x0 - 26, yf + 31, 26, "r", c["ourotx"], ancora="middle"))
    t.append(tip.texto("Uso duplo: a fita é interpretada para construir e copiada sem interpretação. "
                       "O James não evolui trocando de host; evolui editando a fita.", W / 2, 696, 18, "r",
                       c["tinta"], ancora="middle", opacidade=0.85))
    desc = ("Tabela ilustrada da correspondência entre o autômato autorreprodutor de von Neumann e a Factory. "
            + " ".join(f"{s} · {n}: {f}. Na Factory: {p}, {a}." for s, n, f, p, a in COMPONENTES)
            + " Embaixo, a fita Φ desenhada como uma tira de células com zeros, uns e letras; uma célula em ouro "
              "marca uma mutação Δ, isto é, um PR mergeado. Legenda: a fita é interpretada para construir e "
              "copiada sem interpretação; o James não evolui trocando de host, evolui editando a fita. "
              "É uma correspondência de arquitetura, não um teorema.")
    return documento(tip, W, H, "A máquina e a fita: von Neumann e a Factory", desc, "".join(t))


def _chave_horizontal(x1: float, x2: float, y: float, h: float, cor: str) -> str:
    """Chave '}' deitada sob um termo, de x1 a x2, com a ponta para baixo em y + h."""
    m = (x1 + x2) / 2
    q = h / 2
    d = (f"M{x1:.1f} {y:.1f} q0 {q:.1f} {q:.1f} {q:.1f} H{m - q:.1f} q{q:.1f} 0 {q:.1f} {q:.1f} "
         f"q0 -{q:.1f} {q:.1f} -{q:.1f} H{x2 - q:.1f} q{q:.1f} 0 {q:.1f} -{q:.1f}")
    return f'<path d="{d}" fill="none" stroke="{cor}" stroke-width="1.4" stroke-linecap="round"/>'


def equacao(tip: Tipografo) -> str:
    tip.reiniciar()
    c = TEMAS["claro"]
    W, H = 1280, 600
    t = [_cartao(W, H, c)]
    t.append(tip.texto("A EQUAÇÃO DO JAMES", 72, 82, 14, "m", c["ourotx"], tracking=0.24))
    t.append(tip.texto("Minimizar, continuamente, o que a fita sabe mais o que ela não explica", 72, 122, 30,
                       "r", c["tinta"]))
    tam, yb = 96, 290
    termo1, mais, termo2 = "*L*(*F*)", "  +  ", "*L*(*X* | *F*)"
    w1, wm, w2 = (tip.largura(s, tam) for s in (termo1, mais, termo2))
    x = W / 2 - (w1 + wm + w2) / 2
    t.append(f'<rect x="{x - 44:.0f}" y="{yb - 104}" width="{w1 + wm + w2 + 88:.0f}" height="148" fill="none" '
             f'stroke="{c["ouro"]}" stroke-width="1.4"/>')
    t.append(tip.texto(termo1, x, yb, tam, "r", c["tinta"]))
    t.append(tip.texto("+", x + w1 + wm / 2, yb, tam, "r", c["ourotx"], ancora="middle"))
    t.append(tip.texto(termo2, x + w1 + wm, yb, tam, "r", c["tinta"]))
    yc = yb + 76
    t.append(_chave_horizontal(x, x + w1, yc, 22, c["ouro"]))
    t.append(_chave_horizontal(x + w1 + wm, x + w1 + wm + w2, yc, 22, c["ouro"]))
    m1, m2 = x + w1 / 2, x + w1 + wm + w2 / 2
    t.append(tip.texto("o tamanho da fita", m1, yc + 62, 24, "r", c["tinta"], ancora="middle"))
    t.append(tip.texto("tudo o que o sistema sabe", m1, yc + 90, 17, "r", c["suave"], ancora="middle"))
    t.append(tip.texto("o que a fita não explica", m2, yc + 62, 24, "r", c["tinta"], ancora="middle"))
    t.append(tip.texto("o trabalho que ainda depende de um humano lembrar", m2, yc + 90, 17, "r", c["suave"],
                       ancora="middle"))
    t.append(f'<line x1="{W / 2 - 36:.0f}" y1="508" x2="{W / 2 + 36:.0f}" y2="508" stroke="{c["ouro"]}" '
             f'stroke-width="1.5"/>')
    t.append(tip.texto("Uma mutação Δ só entra na fita se o custo de aprender for menor que o trabalho eliminado, "
                       "e se passar pela verificação.", W / 2, 546, 18, "r", c["tinta"], ancora="middle",
                       opacidade=0.85))
    t.append(tip.texto("Modelo proposto no manifesto (§5), com *F* a fita e *X* a realidade da operação. Não é teorema.",
                       W / 2, 572, 15, "r", c["suave"], ancora="middle"))
    desc = ("A equação do James, em destaque dentro de um retângulo de ouro: L(F) mais L(X dado F). Uma chave sob "
            "L(F) diz: o tamanho da fita, tudo o que o sistema sabe. Uma chave sob L(X dado F) diz: o que a fita "
            "não explica, o trabalho que ainda depende de um humano lembrar. Abaixo: uma mutação Δ só entra na "
            "fita se o custo de aprender for menor que o trabalho eliminado e se passar pela verificação. "
            "É um modelo proposto no manifesto, seção 5, não um teorema.")
    return documento(tip, W, H, "A equação do James: L(F) + L(X | F)", desc, "".join(t))


# --------------------------------------------------------------------------------------------
# Peças em PNG: a cena WebGL retratada no Chromium headless
# --------------------------------------------------------------------------------------------

def _preparar_cena(destino: Path) -> None:
    """Monta o diretório servido: a cena, o three.js e as duas fontes que o título usa."""
    import shutil

    shutil.copy(AQUI / "cena" / "fita.html", destino / "fita.html")
    cache = _cache_fontes() / f"three-{VERSAO_THREE}"
    for rel in ARQUIVOS_THREE:
        alvo = cache / rel
        if not alvo.exists():
            alvo.parent.mkdir(parents=True, exist_ok=True)
            url = f"https://cdn.jsdelivr.net/npm/three@{VERSAO_THREE}/{rel}"
            with urllib.request.urlopen(url, timeout=60) as r:  # noqa: S310 (URL fixa)
                alvo.write_bytes(r.read())
        (destino / "three" / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(alvo, destino / "three" / rel)
    (destino / "fontes").mkdir()
    for peso, estilo in (("500", "normal"), ("400", "italic")):
        shutil.copy(_baixar(peso, estilo), destino / "fontes" / f"cg-{peso}-{estilo}.woff")


def renderizar_cena() -> dict[str, bytes]:
    import functools
    import http.server
    import io
    import threading

    from PIL import Image
    from playwright.sync_api import sync_playwright

    pecas = {"banner-claro.png": ("claro", "banner", 1280, 400, 2),
             "banner-escuro.png": ("escuro", "banner", 1280, 400, 2),
             "social-preview.png": ("escuro", "social", 1280, 640, 1)}
    saida = {}
    with tempfile.TemporaryDirectory() as tmp:
        _preparar_cena(Path(tmp))

        class Silencioso(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *a, **k) -> None:  # o log de cada GET só esconde o que importa
                pass

        handler = functools.partial(Silencioso, directory=tmp)
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        try:
            with sync_playwright() as p:
                exe = os.environ.get("CHROMIUM_PATH") or None
                nav = p.chromium.launch(executable_path=exe,
                                        args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader"])
                for nome, (tema, peca, w, h, escala) in pecas.items():
                    pg = nav.new_page(viewport={"width": w, "height": h}, device_scale_factor=escala)
                    erros: list[str] = []
                    pg.on("pageerror", lambda e, erros=erros: erros.append(str(e)))
                    pg.goto(f"http://127.0.0.1:{srv.server_port}/fita.html?tema={tema}&peca={peca}")
                    try:
                        pg.wait_for_function("document.title === 'pronto'", timeout=120_000)
                    except Exception as e:  # sem o título, o erro de JS é o que explica
                        raise SystemExit(f"{nome}: a cena não terminou: {erros or e}") from e
                    if erros:
                        raise SystemExit(f"{nome}: erro na cena: {erros}")
                    bruto = pg.screenshot()
                    pg.close()
                    # 256 cores com difusão: a cena é quase monocromática + ouro
                    im = Image.open(io.BytesIO(bruto)).convert("RGB").quantize(
                        colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
                    buf = io.BytesIO()
                    im.save(buf, format="PNG", optimize=True)
                    saida[nome] = buf.getvalue()
                nav.close()
        finally:
            srv.shutdown()
    return saida


# --------------------------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--previa", type=Path, help="diretório onde renderizar PNG de cada SVG para conferência")
    ap.add_argument("--so-svg", action="store_true", help="não abre o navegador: gera só os SVG")
    a = ap.parse_args()

    tip = Tipografo()
    pecas = {"fita-von-neumann.svg": fita_von_neumann(tip), "equacao.svg": equacao(tip)}
    for nome, svg in pecas.items():
        (AQUI / nome).write_text(svg, encoding="utf-8")
        print(f"{nome}: {len(svg.encode()) / 1000:.1f} KB")
    if not a.so_svg:
        for nome, png in renderizar_cena().items():
            (AQUI / nome).write_bytes(png)
            print(f"{nome}: {len(png) / 1000:.1f} KB")
    if a.previa:
        import cairosvg

        a.previa.mkdir(parents=True, exist_ok=True)
        for nome, svg in pecas.items():
            cairosvg.svg2png(bytestring=svg.encode(), write_to=str(a.previa / nome.replace(".svg", ".png")))


if __name__ == "__main__":
    main()
