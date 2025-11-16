```markdown
---
title: Database
layout: default
---

# database.ts

*Auto-generated from `./database.ts`*

# `database.ts` – API Documentation

> **What this module does**  
> A lightweight, TypeScript‑friendly wrapper that defines a database configuration interface, a `Database` class with async connection helpers, a factory function to create a connected instance, and a simple input‑sanitisation helper.  
> The implementation is intentionally minimal – the methods are placeholders that you can replace with your own driver logic (e.g. `pg`, `mysql2`, `sqlite3`, etc.).

> **Note**: The actual connection logic is omitted in this snippet; in a real implementation you would replace the placeholder comments with a driver such as `pg`, `mysql2`, or `sqlite3`.

---

## Overview

`database.ts` provides a lightweight abstraction for connecting to a relational database, executing queries, and safely handling user input.

- **`DatabaseConfig`** – Describes the connection parameters (host, port, database name, username, password).  
- **`Database`** – A class that manages a single connection lifecycle and exposes `connect()`, `query()`, and `disconnect()` methods.  
- **`createConnection`** – A convenience async factory that returns a **connected** `Database` instance.  
- **`sanitizeInput`** – A helper that removes potentially dangerous characters (`'`, `"`, `;`) from strings before they are used in SQL statements.

---

## 1. Exports

| Export            | Type       | Description                                                                 |
|-------------------|------------|-----------------------------------------------------------------------------|
| `DatabaseConfig`  | `interface`| Defines the configuration needed to connect to a database.                 |
| `Database`        | `class`    | Manages a database connection and provides `connect`, `query`, and `disconnect` methods. |
| `createConnection`| `function`| Async factory that creates **and connects** a `Database` instance.          |
| `sanitizeInput`   | `function`| Removes single quotes, double quotes, and semicolons from a string.        |

---

## 2. Usage Examples

### 2.1 Importing

```ts
import {
  Database,
  DatabaseConfig,
  createConnection,
  sanitizeInput,
} from './database';
```

### 2.2 Defining a Configuration

```ts
const config: DatabaseConfig = {
  host: 'localhost',
  port: 5432,
  database: 'my_app',
  username: 'app_user',
  password: 's3cr3t',
};
```

### 2.3 Instantiating `Database` Manually

```ts
const db = new Database(config);

async function runManual() {
  await db.connect(); // Open the connection

  const rows = await db.query(
    'SELECT * FROM users WHERE age > $1',
    [30]
  );
  console.log(rows);

  await db.disconnect(); // Close the connection
}

runManual().catch(console.error);
```

### 2.4 Using the `createConnection` Factory

```ts
async function runFactory() {
  const db = await createConnection(config); // Already connected

  const products = await db.query('SELECT * FROM products');
  console.log(products);

  await db.disconnect(); // Clean up
}

runFactory().catch(console.error);
```

### 2.5 Sanitising Input

```ts
const raw = "O'Reilly; DROP TABLE users; --";
const safe = sanitizeInput(raw);
console.log(safe); // OReilly DROP TABLE users --
```

---

## 3. Parameters

| Function / Method          | Parameter | Type               | Description                                   |
|----------------------------|-----------|--------------------|-----------------------------------------------|
| `Database` constructor     | `config`  | `DatabaseConfig`   | Connection configuration.                    |
| `Database.connect()`       | –         | –                  | Opens the database connection.               |
| `Database.query(sql, params?)`| `sql`   | `string`           | SQL statement to execute.                    |
|                            | `params`  | `any[]` (optional) | Array of bind parameters for the query.      |
| `Database.disconnect()`   | –         | –                  | Closes the database connection.              |
| `createConnection(config)`| `config`  | `DatabaseConfig`   | Configuration used to create & connect the `Database`. |
| `sanitizeInput(input)`    | `input`   | `string`           | Raw string that may contain unsafe characters. |
|                            | –         | –                  | Returns a sanitized version of `input`.      |

---

*Last updated: 2025-11-16*  
```