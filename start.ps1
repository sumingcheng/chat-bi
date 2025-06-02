# 从 .env 读其它变量...
$envFile = Get-Content .env -ErrorAction SilentlyContinue
if ($envFile) {
    foreach ($line in $envFile) {
        if ($line.Trim() -and $line.Trim() -notmatch '^#') {
            $kv = $line.Split('=',2)
            if ($kv.Length -eq 2) {
                [Environment]::SetEnvironmentVariable($kv[0].Trim(), $kv[1].Trim(), "Process")
                Write-Host "Set environment variable: $($kv[0].Trim())"
            }
        }
    }
}

# 代理设置
$env:HTTP_PROXY  = "http://127.0.0.1:7890"
$env:HTTPS_PROXY = "http://127.0.0.1:7890"

$env:NO_PROXY = "localhost,127.0.0.1,172.19.221.125"

# Python 无缓冲输出
$env:PYTHONUNBUFFERED   = "1"
$env:PYTHONHTTPSVERIFY  = "0"
$env:SSL_CERT_FILE      = ""
$env:SSL_CERT_DIR       = ""

# 启用 Ctrl+C
$host.UI.RawUI.FlushInputBuffer()

try {
    python -u main.py
}
finally {
    Write-Host "Script terminated."
}