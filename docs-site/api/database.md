---
title: Database
layout: default
---

# database.ts

*Auto-generated from `./database.ts`*

# `database.ts` – API Documentation

> **What this module does**  
> Provides a lightweight, type‑safe wrapper around a generic database connection.  
> It exposes a configuration interface, a `Database` class with basic lifecycle methods, a helper to create a connected instance, and a simple input‑sanitisation utility.

---

## 1. Overview

The module is a **stand‑alone database abstraction** written in TypeScript.  
It is intentionally minimal – the actual connection logic is omitted so you can plug in any driver (PostgreSQL, MySQL, SQLite, etc.) without changing the public API.

Typical usage pattern:

```ts
import { createConnection, DatabaseConfig, sanitizeInput } from './database';

const config: DatabaseConfig = {
  host: 'localhost',
  port: 5432,
  database: 'mydb',
  username: 'user',
  password: 'secret',
};

async function run() {
  const db = await createConnection(config);

  const safeName = sanitizeInput('O\'Reilly; DROP TABLE users;');
  const rows = await db.query('SELECT * FROM users WHERE name = $1', [safeName]);

  console.log(rows);
  await db.disconnect();
}
```

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| `DatabaseConfig` | `interface` | Configuration object for a database connection. |
| `Database` | `class` | Represents a database connection with lifecycle methods. |
| `createConnection` | `function` | Factory that creates and connects a `Database` instance. |
| `sanitizeInput` | `function` | Removes potentially dangerous characters from a string. |

---

## 3. Usage Examples

### 3.1 `DatabaseConfig`

```ts
const config: DatabaseConfig = {
  host: 'db.example.com',
  port: 3306,
  database: 'app',
  username: 'admin',
  password: 'p@ssw0rd',
};
```

### 3.2 `Database`

```ts
import { Database, DatabaseConfig } from './database';

const config: DatabaseConfig = { /* … */ };
const db = new Database(config);

await db.connect();                     // Establish connection
const users = await db.query('SELECT * FROM users'); // Execute query
await db.disconnect();                  // Close connection
```

### 3.3 `createConnection`

```ts
import { createConnection, DatabaseConfig } from './database';

const config: DatabaseConfig = { /* … */ };
const db = await createConnection(config); // Already connected
```

### 3.4 `sanitizeInput`

```ts
import { sanitizeInput } from './database';

const raw = "O'Reilly; DROP TABLE users;";
const safe = sanitizeInput(raw); // "OReilly DROP TABLE users"
```

---

## 4. Parameters

| Function / Method | Parameter | Type | Description |
|-------------------|-----------|------|-------------|
| `new Database(config)` | `config` | `DatabaseConfig` | Connection settings. |
| `Database.connect()` | – | – | No parameters. |
| `Database.query(sql, params?)` | `sql` | `string` | SQL statement. |
| | `params` | `any[]` | Optional array of bind values. |
| `Database.disconnect()` | – | – | No parameters. |
| `createConnection(config)` | `config` | `DatabaseConfig` | Connection settings. |
| `sanitizeInput(input)` | `input` | `string` | String to sanitise. |

---

## 5. Return Values

| Function / Method | Return Type | Notes |
|-------------------|-------------|-------|
| `Database.connect()` | `Promise<void>` | Resolves when the connection is established. |
| `Database.query(sql, params?)` | `Promise<any[]>` | Resolves with an array of rows. |
| `Database.disconnect()` | `Promise<void>` | Resolves when the connection is closed. |
| `createConnection(config)` | `Promise<Database>` | Resolves with a connected `Database` instance. |
| `sanitizeInput(input)` | `string` | Returns the input with `;`, `'`, and `"` removed. |

---

## 6. Implementation Notes

- **Connection logic is a placeholder** – replace the body of `connect`, `query`, and `disconnect` with your driver’s API (e.g., `pg.Client`, `mysql2`, `sqlite3`, etc.).
- **Query parameters** are passed as an array; the actual driver should handle parameter binding to prevent SQL injection.
- **`sanitizeInput`** is a very simple helper. For production use, rely on parameterised queries instead of manual sanitisation.
- The module is fully typed; you can extend `DatabaseConfig` or the `Database` class to add more options (SSL, pool size, etc.).

---

## 7. Quick Start

```bash
# Install a driver of your choice (example: pg for PostgreSQL)
npm install pg
```

```ts
// db.ts
import { Database, DatabaseConfig } from './database';
import { Client } from 'pg';

export class PostgresDatabase extends Database {
  private client!: Client;

  async connect(): Promise<void> {
    this.client = new Client(this.config);
    await this.client.connect();
  }

  async query(sql: string, params?: any[]): Promise<any[]> {
    const res = await this.client.query(sql, params);
    return res.rows;
  }

  async disconnect(): Promise<void> {
    await this.client.end();
  }
}
```

Now you can use `PostgresDatabase` exactly like the generic `Database` class.

---

### TL;DR

- **`DatabaseConfig`** – host, port, database, username, password.  
- **`Database`** – `connect()`, `query(sql, params?)`, `disconnect()`.  
- **`createConnection(config)`** – returns a connected `Database`.  
- **`sanitizeInput(input)`** – removes `;`, `'`, `"` from a string.  

Happy coding!
