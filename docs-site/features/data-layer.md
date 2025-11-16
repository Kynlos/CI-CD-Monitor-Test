```markdown
---
title: Data Layer
layout: default
last_updated: 2025-11-16
---

# database.ts

*Auto-generated from `./database.ts`*

# `database.ts` – API Documentation

## Overview
`database.ts` provides a lightweight, TypeScript‑friendly abstraction for connecting to a relational database, executing queries, and safely handling user input.

- **`DatabaseConfig`** – Describes the connection parameters (host, port, database name, username, password).  
- **`Database`** – A class that manages a single connection lifecycle and exposes `connect()`, `query()`, and `disconnect()` methods.  
- **`createConnection`** – A convenience async factory that returns a **connected** `Database` instance.  
- **`sanitizeInput`** – A helper that removes potentially dangerous characters (`'`, `"`, `;`) from strings before they are used in SQL statements.

> **Note**: The actual connection logic is omitted in this snippet; in a real implementation you would replace the placeholder comments with a driver such as `pg`, `mysql2`, or `sqlite3`.

---

## Exports

| Export            | Type        | Description                                                                 |
|-------------------|------------|-----------------------------------------------------------------------------|
| `DatabaseConfig`  | `interface`| Defines the configuration needed to connect to a database.                 |
| `Database`        | `class`    | Manages a database connection and provides `connect`, `query`, and `disconnect` methods. |
| `createConnection`| `function` | Async factory that creates **and connects** a `Database` instance.         |
| `sanitizeInput`   | `function` | Removes single quotes, double quotes, and semicolons from a string.        |

---

## Usage Examples

### 1. Importing the API

```ts
import {
  Database,
  DatabaseConfig,
  createConnection,
  sanitizeInput,
} from './database';
```

### 2. Defining a `DatabaseConfig`

```ts
const config: DatabaseConfig = {
  host: 'localhost',
  port: 5432,
  database: 'my_app',
  username: 'app_user',
  password: 's3cr3t',
};
```

### 3. Using the `Database` Class Directly

```ts
const db = new Database(config);

async function runManual() {
  await db.connect(); // Open the connection

  const users = await db.query(
    'SELECT * FROM users WHERE age > $1',
    [30]
  );
  console.log(users);

  await db.disconnect(); // Close the connection
}
runManual().catch(console.error);
```

### 4. Using the `createConnection` Factory

```ts
async function runFactory() {
  const db = await createConnection(config); // Already connected

  const rows = await db.query('SELECT * FROM products');
  console.log(rows);

  await db.disconnect(); // Clean up
}
runFactory().catch(console.error);
```

### 5. Sanitising User Input

```ts
const raw = "O'Reilly; DROP TABLE users; --";
const safe = sanitizeInput(raw);
console.log(safe); // OReilly DROP TABLE users --
```

---

## Parameters

| Function / Method          | Parameter | Type               | Description                                    |
|----------------------------|-----------|--------------------|------------------------------------------------|
| `Database` constructor     | `config`  | `DatabaseConfig`   | Connection configuration.                     |
| `Database.connect()`       | –         | –                  | Opens the database connection.                |
| `Database.query(sql, params?)` | `sql`   | `string`           | SQL statement to execute.                     |
|                            | `params`  | `any[]` (optional) | Array of bind parameters for the query.       |
| `Database.disconnect()`   | –         | –                  | Closes the database connection.               |
| `createConnection(config)`| `config`  | `DatabaseConfig`   | Configuration used to create and connect the `Database`. |
| `sanitizeInput(input)`    | `input`   | `string`           | The raw string to be sanitised.               |

--- 

*This documentation is generated automatically from the source file `./database.ts`.*
```