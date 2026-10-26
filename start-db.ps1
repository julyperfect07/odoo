# Starts the PostgreSQL database server if it isn't already running.
& "$PSScriptRoot\pgsql\bin\pg_isready.exe" -h localhost -p 5432 -q
if ($LASTEXITCODE -ne 0) {
    & "$PSScriptRoot\pgsql\bin\pg_ctl.exe" -D "$PSScriptRoot\pgdata" -l "$PSScriptRoot\pgdata\postgres.log" -o "-p 5432 -c listen_addresses=localhost" start
}
exit 0
