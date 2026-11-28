# Odoo 17 Course Log

An ordered record of what I learned in each lesson while building the `app_one` module (a Real Estate app).
Used later to:

1. build a mind-map summary for studying
2. generate practice tasks in a new project

Claude keeps this file up to date: add a new lesson entry at the end after each lesson/commit.

---

## Lesson 1: Project setup (`eda829e` First commit, 2026-10-26)

- Workspace layout:
  - `odoo/`: Odoo 17 source
  - `custom-addons/`: my modules
  - `venv/`, `pgsql/`, `pgdata/`: Python environment and the database
- `odoo.conf`: `addons_path`, `db_name = odoo17`, `db_user = odoo`, port 8069
- A module needs two files at minimum:
  - `__init__.py`: imports the `models` package
  - `__manifest__.py`: `name`, `author`, `version` (`17.0.x.y.z`), `depends: ['base']`, `data: []`, `application: True`
- Start the app with `start-odoo.ps1`

## Lesson 2: Model types and log access (`a375f04`, 2026-10-31)

- `models.Model`: a normal model, stored in a database table
- `models.TransientModel`: temporary records that get cleaned up automatically (used for wizards)
- `models.AbstractModel`: no table; a base other models inherit from (mixin)
- `_name`: the technical name of the model (`model.a`), which becomes the table name (`model_a`)
- `_log_access = False`: turns off the automatic `create_uid`, `create_date`, `write_uid` and `write_date` fields
  - This lesson's code wrote `_log_access : False`. That's a type hint, not an assignment, so the setting does nothing.
- (These example models were deleted later, in Lesson 6.)

## Lesson 3: The property model (`8826d57`, 2026-10-31)

- `models/__init__.py` has to import every model file
- Basic field types:
  - text: `Char`, `Text`
  - date: `Date`
  - numbers: `Float`, `Integer`
  - true/false: `Boolean`
  - fixed list of choices: `Selection`
- Field options: `required`, `default`, `size`, `digits=(precision, scale)`

## Lesson 4: Views, menus, security ("Sheet record", `1e270ae`, 2026-10-31)

- Manifest `data` list: each XML or CSV file is loaded in the order listed
- Security, `security/ir.model.access.csv`:
  - columns: `id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink`
  - `model_id:id` is `model_` + the model's name with dots replaced by `_`
  - Without this file, the model is invisible to users
- Menus:
  - `<menuitem>` uses `id`, `name`, `parent`, `action`
  - The root menu has no parent and appears as the app on the home screen
- Views are `<record model="ir.ui.view">` with `name`, `model` and `arch type="xml"`
  - Tree (list) view: `<tree>`
  - Form view: `<form><sheet>` with `<div class="oe_title">`, `<label for>`, `<h1>` and nested `<group string="">`
- Action: `<record model="ir.actions.act_window">` with `res_model`; the menu item links to it

## Lesson 5: CRUD operations and the search view (`029f2a0`, 2026-11-02)

- Overriding the ORM methods, always calling `super()`:
  - create: `@api.model_create_multi def create(self, vals)`
  - read: `_search(self, domain, offset, limit, order, ...)`
  - update: `write(self, vals)`
  - delete: `unlink(self)`
- Search view `<search>`:
  - `<field>`: what the search box can search by
  - `<filter domain="[('garden','=',True)]">`: a predefined filter
  - `<filter context="{'group_by': 'garden'}">`: a "group by" option
- Domains are written as `[('field', 'operator', value)]`
- View attribute `required="1"` makes a field required in this view only

## Lesson 6: One2many and Many2one relations (`8a4547b`, 2026-11-02)

- New model `owner` (fields `name`, `phone`, `address`) with its own view file, menu entry and access row
- `Many2one`: on `property`, `owner_id = fields.Many2one('owner')`
  - Many properties point to one owner
  - Stored as a database column
- `One2many`: on `owner`, `property_ids = fields.One2many('property', 'owner_id')` (my code spells it `propery_ids`)
  - It's the reverse side: it needs the matching Many2one field's name
  - It is not stored as a column
- A "Configuration" submenu was added to group setup screens

## Lesson 7: Many2many (`622ed4f` "1 to many, many 2 many", 2026-11-12)

- New model `tag`, with view, menu and access row
- `Many2many`: `tag_ids = fields.Many2many('tag')`
  - Odoo creates a relation table automatically
- Widget `many2many_tags` shows the tags as chips in the form view

## Lesson 8: App icon (`cb1d8e5` "add icon", 2026-11-12)

- The root menu takes `web_icon="app_one,static/description/<file>.svg"`
- The icon file lives in the module's `static/description/` folder

## Lesson 9: Selection field and statusbar (`c4eeaeb` "Selection", 2026-11-12)

- `state = fields.Selection([('draft','Draft'), ('pending','Pending'), ('sold','Sold')], default='draft')`
- Form view `<header>` with `<field name="state" widget="statusbar"/>`
  - `options="{'clickable': 1}"` lets users click a stage to change it (I removed this in Lesson 10)

## Lesson 10: Header buttons, computed fields, depends vs onchange (`f1415eb`, 2026-11-19)

- Buttons in the `<header>`: `<button name="action_draft" type="object" class="btn-primary" string="..."/>`
  - `type="object"` calls the Python method with that `name`
  - `invisible="state == 'draft'"` is the Odoo 17 way to hide something with a condition (the old `attrs` is gone)
- Action methods loop over records: `for rec in self: rec.state = 'sold'`
- Constraints:
  - `@api.constrains('bedrooms')`: check the value and raise `ValidationError`
  - `_sql_constraints = [('unique_name', 'unique(name)', 'message')]`
- Computed field: `diff = fields.Float(compute='_compute_diff', store=1, readonly=0)`
  - `@api.depends('expected_price', 'selling_price', 'owner_id.phone')`
    - These are the fields that trigger a recompute
    - A dotted path like `owner_id.phone` follows a relation
  - `store=True`: the value is saved in the database, so you can search and group by it
  - `readonly=False`: the user can edit the computed value
- `@api.onchange('expected_price')` compared with `@api.depends`:
  - `depends` (computed fields):
    - Runs whenever a listed field changes, whether from the form, the code or a related record (`owner_id.phone`)
    - Works on real saved records
  - `onchange`:
    - Runs only while the user edits that field in the form (local fields of the view)
    - Works on a temporary "pseudo-record" that isn't saved yet
    - Can return `{'warning': {'title': ..., 'message': ..., 'type': 'notification'}}` to show a pop-up
- Controlling the state flow with buttons instead of letting the user click the statusbar (`clickable` removed)

## Lesson 11: Custom CSS with assets (`988f5ee`, 2026-11-19)

- Put CSS files in `static/src/css/` inside the module
- Register them in the manifest with an `assets` bundle:
  - `"assets": {"web.assets_backend": ["app_one/static/src/css/property.css"]}`
  - `web.assets_backend` is the bundle used by the backend (the normal Odoo UI)
  - Write paths with forward slashes, starting with the module name
- Give a view a CSS class, e.g. `<tree class="header_custom">`, and target it from the CSS
  - `.header_custom table thead > tr > th { ... }` styles the list's header cells
  - `th:nth-child(2)` targets one specific column, e.g. to set its width
  - Odoo's own styles are strong, so `!important` is often needed to override them
- Changing the manifest (adding `assets`) needs `-u app_one`
- After CSS changes, hard-refresh the browser (Ctrl+Shift+R), or open the UI with `?debug=assets` in the URL so assets are not minified or cached (slower, so only use it while working on CSS). Note: `--dev=assets` is not an Odoo 17 option and does nothing

## Lesson 12: Model inheritance and view inheritance (`f2c0dc3`, 2026-11-19)

- Depending on other apps: `"depends": ["base", "sale_management", "account"]`
  - Odoo 17 Community has no `account_accountant` (that module is Enterprise only)
- Model inheritance (Odoo's own kind; a model class always extends `models.Model` in Python, but that part isn't the inheritance being taught here):
  - **Extension**: `_inherit = "sale.order"` with no `_name`
    - Adds fields and methods to the existing model and its table
    - `property_id = fields.Many2one("property")` adds a `property_id` column (integer + foreign key) to `sale_order`
  - **Classical (prototype)**: `_name = "client"` + `_inherit = "owner"`
    - Creates a new model with its own table that copies the parent's fields and methods
  - **Delegation**: `_inherits = {"sale.order": "order_id"}` links to a parent record and shows its fields
- Overriding a method and calling the original with `super()`:
  - `def action_confirm(self): res = super().action_confirm(); ...; return res`
  - Always return what `super()` returned
  - `print()` output goes to the server terminal, not the browser
- Import every new model file in `models/__init__.py`, or Odoo never loads it
- View inheritance: an `ir.ui.view` record with `inherit_id` pointing at the parent view
  - `<field name="inherit_id" ref="sale.view_order_form" />` (`module.xml_id`)
  - Inside `arch`, find an element and set `position`: `<field name="partner_id" position="after">`
  - `position` can be `after`, `before`, `inside`, `replace` or `attributes`
- A new XML file in `data` (or a new field) needs `-u app_one`; `--dev=xml` alone doesn't load it

## Lesson 13: Related fields (`f41b2f3`, 2026-11-28)

- A related field shows a field of a linked record directly on this model:
  - `owner_phone = fields.Char(related="owner_id.phone")`
  - `owner_address = fields.Char(related="owner_id.address")`
  - The path starts with a Many2one on this model (`owner_id`), then the field on the other model (`phone`)
  - The field type must match the target field (`phone` is a `Char`, so `owner_phone` is a `Char`)
- Pick the owner in the form and the phone and address fill in at once, before you save
- By default a related field:
  - is **not stored** (`store=False`): no column of its own, and the value is read from the owner each time
    - Turning a plain field into a related field leaves its old column in the database. Odoo never drops columns; it just stops using them.
  - is **read-only**
- With `readonly=False` (my code writes `readonly=0`), editing the phone on the property **writes it back to the owner record**, so every property of that owner changes too
- Add `store=True` if you need to search, group or sort by it
- Changing a field to a related field is a Python change, so restart with `-u app_one`

## Lesson 14: SQL constraint on the owner (`64fb0d6`, 2026-11-28)

- `_sql_constraints = [("unique_name", "unique(name)", "This name exists")]` on `owner`
  - Each tuple is (constraint name, SQL constraint, error message shown to the user)
  - PostgreSQL enforces it, and Odoo names it `<table>_<name>`: `owner_unique_name`
  - It's added to the database during `-u app_one`
- If records that break it already exist, Odoo can't add it:
  - The log says `Table 'owner': unable to add constraint 'owner_unique_name' as unique(name)`, as a warning
  - The module still loads, but nothing is checked
  - Fix: remove or rename the duplicates, then run `-u app_one` again
- Compared with `@api.constrains` (Lesson 10):
  - `_sql_constraints` is checked by the database; a Python constraint is checked by Odoo
  - A Python constraint only runs on create and write, and never checks the records that already exist

## Lesson 15: Chatter and field tracking (2026-11-28)

- Add `"mail"` to `depends` in the manifest
- Inherit two mixins on the model: `_inherit = ["mail.thread", "mail.activity.mixin"]`
  - `_name = "property"` stays, so this extends my own model with the mixins' fields and methods (Odoo allows several parents in a list)
  - `mail.thread`: messages, followers, tracking
  - `mail.activity.mixin`: scheduled activities (to-dos, calls, meetings)
  - Ruff warns `RUF012` about the list; Odoo only reads it once at startup, so silence it with `# noqa: RUF012`
- Chatter in the form view, after `</sheet>` and inside `<form>`:
  - `<div class="oe_chatter">` with `<field name="message_follower_ids"/>`, `<field name="activity_ids"/>`, `<field name="message_ids"/>`
  - Those fields come from the mixins, not from my model
- `tracking=True` on a field (`description`, `date_availability`; my code writes `tracking=1`) logs every change in the chatter, e.g. `Date Availability: old → new`
  - Logged only when the record is saved
- `_description = "Property Record"` gives the model a readable name, which the chatter uses in its messages
- New mixins and `tracking` are Python changes, so restart with `-u app_one`

---

## Dev workflow lessons (from working with Claude)

- Views live in the database: after editing XML, upgrade with `-u app_one`, or run with `--dev=xml`
  - `--dev=xml` only re-reads views that are already installed; a new XML file or a new view record needs `-u app_one` (adding new fields needs it too)
- New or changed fields need a module upgrade
  - Otherwise you get `psycopg2.errors.UndefinedColumn: column ... does not exist`
- Dev mode command: `.\start-odoo.ps1 -u app_one '--dev=xml,reload'`
  - Keep the quotes in PowerShell
  - `reload` restarts Odoo when a `.py` file changes, but it does not upgrade the module
- Use `required=True`, not `required=1`, in Python
- Give each model a `_description` to avoid warnings
- Formatting:
  - Prettier formats XML and Markdown (`npm run format`)
  - Ruff formats Python on save
- Depending on other modules (`"depends": [...]` in the manifest):
  - This setup is Odoo 17 Community, so Enterprise-only modules like `account_accountant` don't exist; use `account` instead
  - If a dependency is missing, Odoo skips the whole module and the UI breaks with "Missing model ..."
  - "Update Apps List" only finds modules; upgrading the module (`-u app_one`) installs the new dependencies
  - Run that upgrade without `reload` (`.\start-odoo.ps1 -u app_one '--dev=xml'`), or the auto-reload restarts Odoo mid-install and drops `-u`
