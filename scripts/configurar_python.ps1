# configurar_python.ps1 - deixa `python` e `py` funcionando em qualquer terminal (PowerShell, Git Bash, agentes).
#
# O problema (visto em 2026-10-19): a pasta do Python nao estava no PATH do usuario, e
# C:\Users\<voce>\AppData\Local\Microsoft\WindowsApps\python.exe (o atalho da Microsoft Store) respondia
# no lugar dele - abre a loja ou diz "Python was not found". Cada modelo tinha de descobrir o caminho completo.
#
# O que faz: acha o Python mais novo em %LOCALAPPDATA%\Programs\Python e poe na FRENTE do PATH do usuario
# a pasta dele, a pasta Scripts e o Launcher (py.exe). Antes de mudar, guarda o PATH antigo num arquivo.
# Mexe so no PATH do USUARIO (nao precisa de administrador; nao toca no PATH da maquina).
#
# Uso:
#   powershell -ExecutionPolicy Bypass -File scripts\configurar_python.ps1            # so mostra o que faria
#   powershell -ExecutionPolicy Bypass -File scripts\configurar_python.ps1 -Aplicar   # aplica
# Desfazer: o caminho do backup e impresso ao aplicar; restaure com
#   [Environment]::SetEnvironmentVariable('Path', (Get-Content <backup>), 'User')
# Depois de aplicar, FECHE e reabra o terminal / o app (processos abertos guardam o PATH antigo).
param([switch]$Aplicar)

$base = Join-Path $env:LOCALAPPDATA 'Programs\Python'
$python = Get-ChildItem $base -Directory -Filter 'Python3*' -ErrorAction SilentlyContinue |
    Where-Object { Test-Path (Join-Path $_.FullName 'python.exe') } |
    Sort-Object { [int]($_.Name -replace '\D', '') } -Descending | Select-Object -First 1
if (-not $python) {
    Write-Host "Nenhum Python em $base. Instale o Python 3.10+ de python.org (marcando 'Add to PATH') e rode de novo."
    exit 1
}
$novos = @($python.FullName, (Join-Path $python.FullName 'Scripts'))
$launcher = Join-Path $base 'Launcher'
if (Test-Path (Join-Path $launcher 'py.exe')) { $novos += $launcher }

$atual = [Environment]::GetEnvironmentVariable('Path', 'User')
$partes = @($atual -split ';' | Where-Object { $_ -and ($novos -notcontains $_.TrimEnd('\')) -and ($novos -notcontains $_) })
$final = ($novos + $partes) -join ';'

Write-Host "Python encontrado: $($python.FullName)"
Write-Host "Vai para a frente do PATH do usuario:"
$novos | ForEach-Object { Write-Host "  $_" }
if ($final -eq $atual) { Write-Host "Nada a fazer: o PATH do usuario ja esta assim."; exit 0 }
if (-not $Aplicar) { Write-Host "`nSimulacao. Para aplicar: rode de novo com -Aplicar."; exit 2 }

$backup = Join-Path $env:LOCALAPPDATA ("path_usuario_backup_{0:yyyyMMdd_HHmmss}.txt" -f (Get-Date))
Set-Content -Path $backup -Value $atual -Encoding UTF8
[Environment]::SetEnvironmentVariable('Path', $final, 'User')
Write-Host "`nAplicado. Backup do PATH antigo: $backup"
Write-Host "Feche e reabra o terminal e o app. Confira com:  python --version   e   py --version"
Write-Host "Opcional: Configuracoes > Aplicativos > Configuracoes avancadas > Aliases de execucao de aplicativo"
Write-Host "          > desligue 'Instalador de aplicativo python.exe' e 'python3.exe'."
exit 0
