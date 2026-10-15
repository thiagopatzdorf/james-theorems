# Abre o draw.io local com o fluxo mais recente da pasta "fluxos". Windows, sem instalar nada.
# Feche esta janela para parar. Nada sai do seu computador (só localhost).
$ErrorActionPreference = 'Stop'
$raiz = Split-Path -Parent $MyInvocation.MyCommand.Path
$porta = 8765
$arq = Get-ChildItem -Path (Join-Path $raiz 'fluxos') -Filter *.drawio | Sort-Object LastWriteTime -Descending | Select-Object -First 1
$url = "http://localhost:$porta/abrir.html"
if ($arq) { $url += '?f=fluxos/' + [System.Uri]::EscapeDataString($arq.Name) }
$mime = @{ '.html'='text/html; charset=utf-8'; '.js'='application/javascript; charset=utf-8'; '.css'='text/css; charset=utf-8';
  '.json'='application/json'; '.svg'='image/svg+xml'; '.png'='image/png'; '.gif'='image/gif'; '.jpg'='image/jpeg'; '.ico'='image/x-icon';
  '.txt'='text/plain; charset=utf-8'; '.xml'='application/xml'; '.drawio'='application/xml'; '.woff2'='font/woff2'; '.woff'='font/woff';
  '.ttf'='font/ttf'; '.wasm'='application/wasm' }
$l = New-Object System.Net.HttpListener
$l.Prefixes.Add("http://localhost:$porta/")
$l.Start()
Start-Process $url
Write-Host "draw.io aberto em $url"
Write-Host "Deixe esta janela aberta enquanto usa o editor. Feche para encerrar."
while ($l.IsListening) {
  $c = $l.GetContext()
  try {
    $rel = [System.Uri]::UnescapeDataString($c.Request.Url.AbsolutePath).TrimStart('/')
    $f = [System.IO.Path]::GetFullPath((Join-Path $raiz $rel))
    if (-not $f.StartsWith($raiz) -or -not (Test-Path -LiteralPath $f -PathType Leaf)) { $c.Response.StatusCode = 404 }
    else {
      $ext = [System.IO.Path]::GetExtension($f).ToLower()
      $tipo = $mime[$ext]; if (-not $tipo) { $tipo = 'application/octet-stream' }
      $b = [System.IO.File]::ReadAllBytes($f)
      $c.Response.ContentType = $tipo
      $c.Response.ContentLength64 = $b.Length
      $c.Response.OutputStream.Write($b, 0, $b.Length)
    }
  } catch { $c.Response.StatusCode = 500 }
  finally { $c.Response.Close() }
}
