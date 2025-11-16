---
title: Database
layout: default
---

# database.ts

*Auto-generated from `./database.ts`*

# `database.ts` – API Documentation

## Overview
`database.ts` provides a lightweight abstraction for managing a database connection and executing SQL queries.  
- **`DatabaseConfig`** – Type describing connection parameters.  
- **`Database`** – Class that encapsulates a connection lifecycle (`connect`, `query`, `disconnect`).  
- **`createConnection`** – Helper that creates a `Database` instance and opens the connection automatically.  
- **`sanitizeInput`** – Utility that removes common SQL‑injection characters from a string.

> **Note:** The actual connection logic is omitted in this snippet; replace the placeholder comments with your preferred driver (e.g., `pg`, `mysql`, `sqlite3`).

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `DatabaseConfig` | `interface` | Configuration object for a database connection. |
| `Database` | `class` | Represents a database connection with lifecycle methods. |
| `createConnection` | `function` | Factory that returns a connected `Database` instance. |
| `sanitizeInput` | `function` | Removes potentially dangerous characters from a string. |

---

## Usage Examples

### 1. `DatabaseConfig`

```ts
import { DatabaseConfig } from './database';

const config: DatabaseConfig = {
  host: 'localhost',
  port: 5432,
  database: 'mydb',
  username: 'user',
  password: 'secret',
};
```

### 2. `Database`

```ts
import { Database, DatabaseConfig } from './database';

const config: DatabaseConfig = { /* … */ };
const db = new Database(config);

await db.connect();

const users = await db.query('SELECT * FROM users WHERE id = $1', [42]);

await db.disconnect();
```

### 3. `createConnection`

```ts
import { createConnection, DatabaseConfig } from './database';

const config: DatabaseConfig = { /* … */ };

async function run() {
  const db = await createConnection(config);

  try {
    const rows = await db.query('SELECT * FROM products');
    console.log(rows);
  } finally {
    await db.disconnect();
  }
}

run().catch(console.error);
```

### 4. `sanitizeInput`

```ts
import { sanitizeInput } from './database';

const raw = "O'Reilly; DROP TABLE users; --";
const safe = sanitizeInput(raw);
// safe === "OReilly DROP TABLE users --"
```

---

## Parameters & Return Values

### `DatabaseConfig` (interface)

| Property | Type | Description |
|----------|------|-------------|
| `host` | `string` | Database host address. |
| `port` | `number` | Port number. |
| `database` | `string` | Database name. |
| `username` | `string` | Login username. |
| `password` | `string` | Login password. |

### `Database` (class)

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `constructor(config: DatabaseConfig)` | `config` – connection configuration | `void` | Stores the config for later use. |
| `connect(): Promise<void>` | – | `Promise<void>` | Opens the database connection. |
| `query(sql: string, params?: any[]): Promise<any[]>` | `sql` – SQL string; `params` – optional array of bind values | `Promise<any[]>` – array of rows returned by the query. |
| `disconnect(): Promise<void>` | – | `Promise<void>` | Closes the database connection. |

### `createConnection(config: DatabaseConfig): Promise<Database>`

| Parameter | Type | Description |
|-----------|------|-------------|
| `config` | `DatabaseConfig` | Connection configuration. |

| Return | Description |
|--------|-------------|
| `Promise<Database>` | A `Database` instance that is already connected. |

### `sanitizeInput(input: string): string`

| Parameter | Type | Description |
|-----------|------|-------------|
| `input` | `string` | Raw user input. |

| Return | Description |
|--------|-------------|
| `string` | The input string with `'`, `;`, and `"` characters removed. |

---

## Extending / Customizing

- **Driver Integration**: Replace the placeholder comments in `connect`, `query`, and `disconnect` with the API of your chosen database driver.
- **Error Handling**: Wrap calls in `try/catch` blocks to handle connection or query errors.
- **Connection Pooling**: For production workloads, consider using a connection pool (e.g., `pg.Pool`) instead of a single connection.

---

## License

This file is provided as-is under the MIT license. Feel free to adapt it to your project.
