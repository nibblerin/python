# Rooms & Students Report 

Loads `rooms.json` and `students.json` into a PostgreSQL database and
generates four required reports as JSON or XML. Every query
is SQL. Built with OOP and SOLID principles: each class has a single responsibility, and
high-level code depends only on abstractions (`Database`, `FileReader`,
`ReportExporter`). Every class has one reason to change (SRP).

## Data model

Many-to-one relationship: many students live in one room.

```
rooms (id PK, name)
students (id PK, name, birthday, sex, room_id FK -> rooms.id)
```

See [`sql/schema.sql`](sql/schema.sql).

### Business rules

- A room **cannot be deleted** while at least one student still lives
  in it (`ON DELETE RESTRICT` on the foreign key)
- A student **cannot exist without a room** (`room_id` is `NOT NULL`).
- `rooms.id` is the `PRIMARY KEY`, which automatically creates a
  unique index on it in PostgreSQL

## Architecture

```
project/
  main.py                    entry point 
  cli/
    __init__.py
    parser.py                  argparse: --students, --rooms, --format, --use-indexes, --export-only
  data/
    students.json                  input data
    rooms.json                     input data
  database/
    __init__.py
    interface.py                Database ABC (execute/executemany/fetchall/commit/rollback/close/enter/exit)
    postgres.py                  PostgresDatabase (psycopg)
  reader/
    __init__.py
    interface.py                 FileReader ABC
    json_reader.py                JsonFileReader
  exporters/
    __init__.py
    interface.py                 ReportExporter ABC
    json_exporter.py / xml_exporter.py
    factory.py                    picks the exporter by --format
  services/
    __init__.py
    schema_srv.py                 applies .sql files, drops tables
    import_srv.py                 loads rooms/students into the database
    report_srv.py                 the 4 required reports — all math done in SQL
  sql/
    schema.sql                    CREATE TABLE statements
    indexes.sql                   recommended indexes
  requirements.txt
  .gitignore
```

Every folder that contains Python modules and is imported has an
`__init__.py` marking it as a package. But this was done only to demonstrate the understanding of the concept
of packages. In modern Python implicit namespace packaging allows not to create `__init__.py`-s (and for backward compatibility
just in case)

## Required reports

1. `rooms_with_student_count` — rooms and the number of students in each
2. `top5_rooms_smallest_avg_age` — 5 rooms with the smallest average student age
3. `top5_rooms_largest_age_diff` — 5 rooms with the largest age gap between students
4. `rooms_with_mixed_sex` — rooms that house both M and F students

## Indexes and their usage analysis

See [`sql/indexes.sql`](sql/indexes.sql).

- `idx_students_room_id (room_id)` — speeds up point lookups and
  filtering by a single room
- `idx_students_birthday (birthday)` — this plain index would help
  global date-range queries not scoped to a room 
- `idx_students_room_birthday (room_id, birthday)` — birthday-range
  lookups scoped to a single room 
- `idx_students_room_sex (room_id, sex)` — sex-filtered lookups
  scoped to a single room
- `idx_students_name (name)` — exact-match student lookup by name
- `idx_rooms_name (name)` — exact-match room lookup by name

`rooms.id` already has a unique index via its `PRIMARY KEY`, so no
extra index is needed on the `rooms` side. `idx_students_room_id`
speeds up the `JOIN`/`GROUP BY room_id` used by every report query —
without it PostgreSQL has to scan the whole `students` table for each
room; with it, it can use an index scan on `room_id` instead.

`EXPLAIN ANALYZE` was run for all 4 report queries both before and
after creating the indexes from `sql/indexes.sql` (that version contained `idx_students_room_id`
and `idx_students_birthday`. In every case the
planner chose `Seq Scan` over `Index Scan`, with nearly identical
`cost` and execution time regardless of whether the indexes existed:

| Query | Plan node (both with and without indexes) |
|---|---|
| Rooms + student count | `Seq Scan on students (cost=0.00..176.00 rows=10000)` |
| Top-5 smallest avg age | `Seq Scan on students st (cost=0.00..176.00 rows=10000)` |
| Top-5 largest age diff | `Seq Scan on students st (cost=0.00..176.00 rows=10000)` |
| Mixed-sex rooms | `Seq Scan on students st (cost=0.00..176.00 rows=10000)` |

This is expected as every one of these
4 queries aggregates over the **entire** `students` table and the entire `rooms` table \
— there is no `WHERE` clause narrowing the result down
to a small subset. While an index only pays off when it lets Postgres skip
most of a table.

The indexes in `sql/indexes.sql` remain useful, though, for queries that
**do** filter by a small subset, but those are not part of the
4 required aggregate reports.

I realize, that most of these indexes are for potential queries, that are not implemented here. But given the
relatively small data volume, the storage/write overhead is negligible.

## Requirements

- Python 3.10+(tested with 15)
- PostgreSQL 14+ (tested with 18)
- See [`requirements.txt`](requirements.txt) for Python packages
  (`psycopg[binary]`, `python-dotenv`)

## Setup

### 1. Install PostgreSQL (if no PostgreSQL is on your computer)

! (On Windows) make sure `psql` is on your `PATH` (or add it per
terminal session):

```powershell
$env:Path += ";C:\Program Files\PostgreSQL\18\bin"
```
But in case you use the expression above, notice it has to be done
every time you use new terminal

### 2. Create a virtual environment and install dependencies

```bash
python -m venv .venv
(# Windows)
.venv\Scripts\activate
pip install -r requirements.txt
```
### 3. Configure environment variables

Create .env`. Copy `.env.example` to `.env` and fill in your password:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=rooms_students
DB_USER=postgres
DB_PASSWORD=your_password_here
```

### 4. Create the database

```bash
psql -U postgres -c "CREATE DATABASE rooms_students;"
```

Table creation is handled automatically by the application itself
(`SchemaService`, driven by `sql/schema.sql`) on every run that isn't
`--export-only` — no manual `psql -f` step is required for the tables.

## Usage

```bash
python main.py --students path/to/students.json --rooms path/to/rooms.json --format json
```

### CLI arguments

| Flag | Required | Description |
|---|---|---|
| `--students` | yes, unless `--export-only` | Path to `students.json` |
| `--rooms` | yes, unless `--export-only` | Path to `rooms.json` |
| `--format` | yes | Output format: `json` or `xml` |
| `--use-indexes` | no | Also apply `sql/indexes.sql` after creating the schema |
| `--export-only` | no | Skip dropping/reloading data; just re-export reports from what's already in the database |

**Note:** unless `--export-only` is passed, every run drops and
recreates the `rooms`/`students` tables before loading data, giving a
clean, reproducible state. Use `--export-only` if you only want to
regenerate the report file from data that's already loaded.

### Examples

Full run, loading data and applying indexes, output as JSON:

```bash
python main.py --students data/students.json --rooms data/rooms.json --format json --use-indexes
```

Re-export existing data as XML without reloading:

```bash
python main.py --format xml --export-only
```

Output files are written to the project root by default:
`result_json.json` / `result_xml.xml`.
