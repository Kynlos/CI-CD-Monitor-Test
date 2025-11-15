---
title: Database
layout: default
---

# database.ts

*Auto-generated from `./database.ts`*

# Database Module – `database.ts`

## Overview
The **database** module provides a lightweight abstraction for establishing a database connection, executing SQL queries, and safely sanitizing user‑supplied input.  
It is intentionally minimal – you can plug it into any SQL‑compatible driver (PostgreSQL, MySQL, SQLite, etc.) by implementing the connection logic inside the `connect`, `query`, and `disconnect` methods.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `DatabaseConfig` | **Interface** | Configuration object required to create a connection. |
| `Database` | **Class** | Represents a database connection. |
| `createConnection` | **Function** | Factory that creates a `Database` instance and opens the connection. |
| `sanitizeInput` | **Function** | Removes potentially dangerous characters from a string. |

---

## Usage Examples

### 1. Create a connection with `createConnection`

```ts
import { createConnection, DatabaseConfig } from './database';

const config: DatabaseConfig = {
  host: 'localhost',
  port: 5432,
  database: 'myapp',
  username: 'dbuser',
  password: 'secret',
};

async function main() {
  const db = await createConnection(config);
  // … use db …
  await db.disconnect();
}

main().catch(console.error);
```

### 2. Use the `Database` class directly

```ts
import { Database, DatabaseConfig } from './database';

const config: DatabaseConfig = { /* … */ };
const db = new Database(config);

async function run() {
  await db.connect();

  const users = await db.query('SELECT * FROM users WHERE age > $1', [30]);
  console.log(users);

  await db.disconnect();
}

run().catch(console.error);
```

### 3. Sanitize user input

```ts
import { sanitizeInput } from './database';

const raw = "Robert'); DROP TABLE Students;--";
const safe = sanitizeInput(raw);
// safe === "Robert DROP TABLE Students--"
```

---

## Parameters

| Function / Method | Parameter | Type | Description |
|-------------------|-----------|------|-------------|
| `Database` (constructor) | `config` | `DatabaseConfig` | Connection configuration. |
| `connect` | – | – | Opens the connection. |
| `query` | `sql` | `string` | SQL statement to execute. |
| | `params` | `any[]` | Optional array of parameters for parameterized queries. |
| `disconnect` | – | – | Closes the connection. |
| `createConnection` | `config` | `DatabaseConfig` | Same as the constructor. |
| `sanitizeInput` | `input` | `string` | Raw string to be sanitized. |

---

## Return Values

| Function / Method | Return Type | Description |
|-------------------|-------------|-------------|
| `connect` | `Promise<void>` | Resolves when the connection is established. |
| `query` | `Promise<any[]>` | Resolves to an array of rows returned by the query. |
| `disconnect` | `Promise<void>` | Resolves when the connection is closed. |
| `createConnection` | `Promise<Database>` | Resolves to a connected `Database` instance. |
| `sanitizeInput` | `string` | The sanitized string with `'`, `;`, and `"` removed. |

> **Note**: The actual database driver implementation is omitted in this file.  
> Replace the body of `connect`, `query`, and `disconnect` with the driver‑specific logic (e.g., using `pg`, `mysql2`, `sqlite3`, etc.) to make the module functional.
