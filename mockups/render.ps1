# Izriše vse mockupe izdelkov v img/products (1600 x 1600). Zahteva lokalni strežnik na :8080.
param([string[]]$Keys)
$chrome = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$root = Split-Path $PSScriptRoot -Parent
$out = Join-Path $root "img\products"
New-Item -ItemType Directory -Force $out | Out-Null
if (-not $Keys) {
  $Keys = "tee-logo-black","tee-logo-bone","tank-logo-black","tee-back-logo-black","tee-back-logo-bone",
          "leggings-black","set-black","set-stone","stay-stack-black","stay-circle-bone","stay-outline-black","stay-front-bone"
}
foreach ($k in $Keys) {
  $png = Join-Path $out "$k.png"
  & $chrome --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --window-size=1600,1600 `
    --virtual-time-budget=6000 --screenshot="$png" "http://localhost:8080/mockups/studio.html?p=$k" 2>$null | Out-Null
  python -c "from PIL import Image; im=Image.open(r'$png').convert('RGB'); im.save(r'$($png -replace '\.png$','.jpg')',quality=86,optimize=True,progressive=True)"
  Remove-Item $png
  Write-Output "OK $k"
}
