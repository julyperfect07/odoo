# Odoo 17 development setup

## Folders

- `odoo/` – Odoo 17 source code (don't edit)
- `custom-addons/` – **your modules go here** (e.g. the tutorial's `app_one` module)
- `venv/` – Python 3.11 environment with Odoo's libraries
- `pgsql/` – PostgreSQL 17 program files
- `pgdata/` – the database files (don't edit)
- `odoo.conf` – Odoo settings (database `odoo17`, port 8069)

## Daily use (in PowerShell)

Start Odoo (also starts the database):

    C:\Users\abdallah\odoo\start-odoo.ps1

Then open http://localhost:8069 and sign in with `admin` / `admin`.
Stop Odoo with Ctrl+C. To stop the database too:

    C:\Users\abdallah\odoo\stop-db.ps1

## VS Code

Open `C:\Users\abdallah\odoo` in VS Code. Press **F5** (or Run and Debug → "Odoo 17") to start the
database and Odoo with the debugger attached — click left of a line number in your module
to set a breakpoint. Use "Odoo 17 (upgrade app_one module)" after changing your module's
Python files or adding fields. Don't run `start-odoo.ps1` at the same time (both use port 8069).

## While doing the tutorial

After you change Python files in your module, restart Odoo and upgrade the module:

    C:\Users\abdallah\odoo\start-odoo.ps1 -u app_one

Auto-reload XML/Python changes while developing:

    C:\Users\abdallah\odoo\start-odoo.ps1 -u app_one --dev=all

Turn on Developer Mode in Odoo: Settings → scroll down → Activate the developer mode.
