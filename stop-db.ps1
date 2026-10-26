# Stops the PostgreSQL database server (run after you stop Odoo).
& "$PSScriptRoot\pgsql\bin\pg_ctl.exe" -D "$PSScriptRoot\pgdata" stop
