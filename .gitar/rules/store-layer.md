---
title: Route handlers never query the database directly
description: All data access goes through the Store. Route handlers call Store methods and never open database connections or run SQL.
type: check
when: A pull request adds or changes Python code under app/routes/ or app/main.py
actions: Fail the check when a route handler imports a database driver, opens a connection, or runs SQL. Name the file and line, and say which Store method to use or add instead.
---

# Route handlers never query the database directly

Our API has one data access layer: the `Store` interface in `app/store.py`, implemented by `MemoryStore` (unit tests) and `PostgresStore` (deployments). Route handlers in `app/routes/` call Store methods. They do not talk to the database.

## What breaks the rule

- Importing `psycopg` (or any database driver or ORM) in a module under `app/routes/`.
- Opening a connection, creating a cursor, or executing SQL inside a route handler, including when the connection string comes from `DATABASE_URL`.
- Reaching into a Store's private attributes (for example `store._url`) to run your own queries.

## What is fine

- Calling `store.get_charge`, `store.list_refunds`, `store.record_refund`, or any other method on the `Store` interface.
- Adding a new method to the `Store` protocol, `MemoryStore`, and `PostgresStore` when a handler needs a query the Store does not offer yet (an aggregate, for example). SQL belongs in `app/store_pg.py` only.
- Code outside `app/routes/`, such as `scripts/migrate.py`.

## Expected fix

Move the query into a method on `Store`, implement it in both `MemoryStore` and `PostgresStore`, and have the handler call it.
