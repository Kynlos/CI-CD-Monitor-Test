---
title: Database
layout: default
---

# database.ts

*Auto-generated from `./database.ts`*

# `database.ts` – API Documentation

## Overview
`database.ts` provides a lightweight abstraction for connecting to a SQL‑style database, executing queries, and safely sanitizing user input.  
- **`DatabaseConfig`** – Type that describes the connection parameters.  
- **`Database`** – Class that manages a connection lifecycle (`connect`, `query`, `disconnect`).  
- **`createConnection`** – Helper that creates a `Database` instance and opens the connection automatically.  
- **`sanitizeInput`** – Utility that removes potentially dangerous characters from a string to mitigate simple injection attacks.

> **Note**: The actual database driver implementation is omitted; the methods contain placeholders. Replace them with your driver of choice (e.g., `pg`, `mysql2`, `sqlite3`).

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `DatabaseConfig` | `interface` | Configuration object for a database connection. |
| `Database` | `class` | Manages a database connection and query execution. |
| `createConnection` | `function` | Factory that returns a connected `Database` instance. |
| `sanitizeInput` | `function` | Removes single quotes, double quotes, and semicolons from a string. |

---

## Usage Examples

### 1. `DatabaseConfig`

```ts
import { DatabaseConfig } from './database';

const config: DatabaseConfig = {
  host: 'localhost',
  port: 5432,
  database: 'myapp',
  username: 'dbuser',
  password: 'secret',
};
```

### 2. `Database`

```ts
import { Database, DatabaseConfig } from './database';

const config: DatabaseConfig = { /* … */ };
const db = new Database(config);

await db.connect();          // Open the connection
const rows = await db.query(
  'SELECT * FROM users WHERE id = $1',
  [42]
);
console.log(rows);
await db.disconnect();       // Close the connection
```

### 3. `createConnection`

```ts
import { createConnection, DatabaseConfig } from './database';

const config: DatabaseConfig = { /* … */ };

(async () => {
  const db = await createConnection(config);
  const users = await db.query('SELECT * FROM users');
  console.log(users);
  await db.disconnect();
})();
```

### 4. `sanitizeInput`

```ts
import { sanitizeInput } from './database';

const raw = "O'Reilly; DROP TABLE users; --";
const safe = sanitizeInput(raw);
// safe === "OReilly DROP TABLE users --"
```

---

## Parameters

| Function / Method | Parameter | Type | Description |
|-------------------|-----------|------|-------------|
| `Database` (constructor) | `config` | `DatabaseConfig` | Connection settings. |
| `Database.connect` | — | — | No parameters. |
| `Database.query` | `sql` | `string` | SQL statement to execute. |
| | `params` | `any[]` (optional) | Values to bind to placeholders in `sql`. |
| `Database.disconnect` | — | — | No parameters. |
| `createConnection` | `config` | `DatabaseConfig` | Connection settings. |
| `sanitizeInput` | `input` | `string` | Raw user input. |

---

## Return Values

| Function / Method | Return Type | Description |
|-------------------|-------------|-------------|
| `Database.connect` | `Promise<void>` | Resolves when the connection is established. |
| `Database.query` | `Promise<any[]>` | Resolves with an array of rows returned by the query. |
| `Database.disconnect` | `Promise<void>` | Resolves when the connection is closed. |
| `createConnection` | `Promise<Database>` | Resolves with a `Database` instance that is already connected. |
| `sanitizeInput` | `string` | The sanitized string with `'`, `"`, and `;` removed. |

---

## Extending / Customizing

- **Driver Integration**: Replace the placeholder comments in `connect`, `query`, and `disconnect` with calls to your preferred database driver.
- **Error Handling**: Wrap each method in try/catch blocks and throw custom errors if needed.
- **Connection Pooling**: If your driver supports pooling, store the pool instance in `Database` and reuse it across queries.

---

## License

This module is provided as-is under the MIT license. Feel free to adapt it to your project's needs.
