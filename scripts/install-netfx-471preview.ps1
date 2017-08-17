$url = "https://download.microsoft.com/download/1/A/D/1ADF1377-FE9D-49B7-BD8B-2FE63D4A381E/NDP471-KB4020196-x86-x64-AllOS-ENU.exe"

Invoke-WebRequest -Uri $url -OutFile netfx.exe

& netfx.exe /q /norestart