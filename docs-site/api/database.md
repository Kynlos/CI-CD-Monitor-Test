---
title: Database
layout: default
---

# database.ts

*Auto-generated from `./database.ts`*

# `database.ts` – API Documentation

## Overview
`database.ts` provides a lightweight abstraction for connecting to a relational database, executing queries, and safely sanitizing user input.  
- **`Database`** – A class that manages a single connection lifecycle.  
- **`createConnection`** – A helper that creates and connects a `Database` instance in one step.  
- **`sanitizeInput`** – Utility to strip potentially dangerous characters from strings before they are used in SQL statements.

> **Note**: The actual connection logic is omitted (`// Establish connection`) – replace with your preferred driver (e.g., `pg`, `mysql2`, `sqlite3`).

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `DatabaseConfig` | `interface` | Configuration options for a database connection. |
| `Database` | `class` | Represents a database connection with `connect`, `query`, and `disconnect` methods. |
| `createConnection` | `function` | Factory that returns a connected `Database` instance. |
| `sanitizeInput` | `function` | Removes single quotes, semicolons, and double quotes from a string. |

---

## Usage Examples

### 1. `DatabaseConfig`

```ts
const config: DatabaseConfig = {
  host: 'localhost',
  port: 5432,
  database: 'mydb',
  username: 'user',
  password: 'pass',
};
```

### 2. `Database` Class

```ts
import { Database, DatabaseConfig } from './database';

const config: DatabaseConfig = { /* … */ };
const db = new Database(config);

async function run() {
  await db.connect();          // Open the connection
  const rows = await db.query('SELECT * FROM users WHERE id = $1', [1]);
  console.log(rows);
  await db.disconnect();       // Close the connection
}
run();
```

### 3. `createConnection` Helper

```ts
import { createConnection, DatabaseConfig } from './database';

const config: DatabaseConfig = { /* … */ };

async function main() {
  const db = await createConnection(config); // connects automatically
  const users = await db.query('SELECT * FROM users');
  console.log(users);
  await db.disconnect();
}
main();
```

### 4. `sanitizeInput` Utility

```ts
import { sanitizeInput } from './database';

const raw = "O'Reilly; DROP TABLE users;";
const safe = sanitizeInput(raw); // "OReilly DROP TABLE users"
```

---

## Parameters & Return Values

### `DatabaseConfig` (interface)

| Property | Type | Description |
|----------|------|-------------|
| `host` | `string` | Database host address. |
| `port` | `number` | Port number the database listens on. |
| `database` | `string` | Name of the database. |
| `username` | `string` | Username for authentication. |
| `password` | `string` | Password for authentication. |

---

### `Database` Class

| Method | Parameters | Return Type | Description |
|--------|------------|-------------|-------------|
| `constructor(config: DatabaseConfig)` | `config` – connection settings | `void` | Stores the config for later use. |
| `connect(): Promise<void>` | – | `Promise<void>` | Opens a connection to the database. |
| `query(sql: string, params?: any[]): Promise<any[]>` | `sql` – SQL statement; `params` – optional bind values | `Promise<any[]>` | Executes the query and returns an array of rows. |
| `disconnect(): Promise<void>` | – | `Promise<void>` | Closes the database connection. |

---

### `createConnection(config: DatabaseConfig): Promise<Database>`

| Parameter | Type | Description |
|-----------|------|-------------|
| `config` | `DatabaseConfig` | Connection settings. |

| Return Value | Type | Description |
|--------------|------|-------------|
| `Promise<Database>` | A promise that resolves to a connected `Database` instance. |

---

### `sanitizeInput(input: string): string`

| Parameter | Type | Description |
|-----------|------|-------------|
| `input` | `string` | The raw user input to sanitize. |

| Return Value | Type | Description |
|--------------|------|-------------|
| `string` | The input string with all `'`, `;`, and `"` characters removed. |

---

## Extending / Customizing

- **Driver Integration**: Replace the placeholder connection logic with your preferred database driver.  
- **Error Handling**: Wrap `connect`, `query`, and `disconnect` calls in `try/catch` blocks in production code.  
- **Parameterization**: The `query` method accepts an optional `params` array for prepared statements; adapt the placeholder syntax (`$1`, `?`, etc.) to match your driver.

---

## Summary

`database.ts` offers a minimal, type‑safe API for database interactions and input sanitization. Use the `createConnection` helper for quick setup, or instantiate `Database` directly if you need finer control over the connection lifecycle. The `sanitizeInput` function helps prevent basic SQL injection by stripping dangerous characters from user‑supplied strings.
