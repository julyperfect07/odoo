# Starts the database (if needed) and then Odoo.
# Open http://localhost:8069 in your browser. Press Ctrl+C here to stop Odoo.
# Extra arguments are passed to Odoo, e.g.:  .\start-odoo.ps1 -u estate --dev=all

& "$PSScriptRoot\pgsql\bin\pg_isready.exe" -h localhost -p 5432 -q
if ($LASTEXITCODE -ne 0) {
    & "$PSScriptRoot\pgsql\bin\pg_ctl.exe" -D "$PSScriptRoot\pgdata" -l "$PSScriptRoot\pgdata\postgres.log" -o "-p 5432 -c listen_addresses=localhost" start
}

& "$PSScriptRoot\venv\Scripts\python.exe" "$PSScriptRoot\odoo\odoo-bin" -c "$PSScriptRoot\odoo.conf" @args
