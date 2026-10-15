# Fluxo de renovação de seguros (AS IS) com o draw.io já pronto

Pasta de passagem: baixe, use e depois apague. O editor draw.io (versão 32.4.1, licença Apache 2.0, de github.com/jgraph/drawio)
vai junto, então **não depende de site nem de internet**.

## Como abrir
1. Baixe o zip da branch (GitHub: botão verde **Code > Download ZIP**) e extraia.
2. Entre na pasta `tmp-fluxo`.
   - **Windows:** dê duplo clique em `ABRIR-NO-WINDOWS.bat`.
   - **Mac:** duplo clique em `ABRIR-NO-MAC.command` (se pedir, botão direito > Abrir).
   - **Linux:** `./abrir.sh`.
3. O navegador abre o draw.io com o fluxo já desenhado. Mantenha a janela preta/terminal aberta enquanto usa; feche para encerrar.

Para salvar no seu computador: **Ficheiro > Guardar como** (ou Exportar como PNG/SVG/PDF).
Por que o launcher: o navegador não deixa o draw.io abrir direto do disco (`file://`), então o `abrir.*` sobe um servidor só seu, em localhost.

## O que tem aqui
- `fluxos/`: o fluxo em `.drawio` (editável), `.png` e `.svg` (só para ver) e o texto-fonte `.fluxo`.
- `drawio/`: o editor (podado: sem integrações online, modelos e idiomas extras).
- `abrir.html`, `abrir.ps1`, `abrir.sh`: os launchers.
