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

## Lesson 10: Header buttons, computed fields, depends vs onchange (2026-11-19)

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

---

## Dev workflow lessons (from working with Claude)

- Views live in the database: after editing XML, upgrade with `-u app_one`, or run with `--dev=xml`
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
