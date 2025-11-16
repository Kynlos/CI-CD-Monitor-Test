---
title: Data Layer
layout: default
---

# database.ts

*Auto-generated from `./database.ts`*

# `database.ts` – API Documentation

> **What this module does**  
> A lightweight, TypeScript‑friendly wrapper that defines a database configuration interface, a `Database` class with async connection helpers, a factory function to create a connected instance, and a simple input‑sanitisation helper.  
> The implementation is intentionally minimal – the methods are placeholders that you can replace with your own driver logic (e.g. `pg`, `mysql2`, `sqlite3`, etc.).

---

## 1. Overview

| Feature | Description |
|---------|-------------|
| **Configuration** | `DatabaseConfig` interface describes the connection parameters. |
| **Connection** | `Database` class encapsulates a connection and exposes `connect()`, `query()`, and `disconnect()` methods. |
| **Factory** | `createConnection()` creates a `Database` instance and automatically connects it. |
| **Sanitisation** | `sanitizeInput()` removes potentially dangerous characters from a string. |

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| `DatabaseConfig` | `interface` | Describes the host, port, database name, username, and password. |
| `Database` | `class` | Represents a database connection. |
| `createConnection` | `function` | Async factory that returns a connected `Database`. |
| `sanitizeInput` | `function` | Utility that strips `'`, `"`, and `;` from a string. |

---

## 3. Usage Examples

### 3.1 Importing

```ts
import {
  Database,
  DatabaseConfig,
  createConnection,
  sanitizeInput,
} from './database';
```

### 3.2 Using `DatabaseConfig`

```ts
const config: DatabaseConfig = {
  host: 'localhost',
  port: 5432,
  database: 'mydb',
  username: 'user',
  password: 'pass',
};
```

### 3.3 Instantiating `Database` Manually

```ts
const db = new Database(config);

await db.connect();          // Establish the connection
const rows = await db.query('SELECT * FROM users WHERE id = $1', [1]);
console.log(rows);
await db.disconnect();       // Close the connection
```

### 3.4 Using `createConnection`

```ts
async function run() {
  const db = await createConnection(config); // Already connected

  const rows = await db.query('SELECT * FROM products');
  console.log(rows);

  await db.disconnect(); // Clean up
}
run();
```

### 3.5 Sanitising Input

```ts
const raw = "O'Reilly; DROP TABLE users; --";
const safe = sanitizeInput(raw);
console.log(safe); // OReilly DROP TABLE users --
```

---

## 4. Parameters

| Function / Method | Parameter | Type | Description |
|-------------------|-----------|------|-------------|
| `Database` constructor | `config` | `DatabaseConfig` | Connection configuration. |
| `connect()` | – | – | No parameters. |
| `query(sql, params?)` | `sql` | `string` | SQL statement. |
|  | `params` | `any[]` | Optional array of bind parameters. |
| `disconnect()` | – | – | No parameters. |
| `createConnection(config)` | `config` | `DatabaseConfig` | Connection configuration. |
| `sanitizeInput(input)` | `input` | `string` | Raw user input. |

---

## 5. Return Values

| Function / Method | Return Type | Description |
|-------------------|-------------|-------------|
| `Database` constructor | `Database` | Instance of the class. |
| `connect()` | `Promise<void>` | Resolves when the connection is established. |
| `query(sql, params?)` | `Promise<any[]>` | Resolves to an array of rows (currently an empty array). |
| `disconnect()` | `Promise<void>` | Resolves when the connection is closed. |
| `createConnection(config)` | `Promise<Database>` | Resolves to a connected `Database` instance. |
| `sanitizeInput(input)` | `string` | Returns the sanitized string. |

---

## 6. Extending the Implementation

The current methods contain placeholder comments. Replace them with real driver logic, e.g.:

```ts
import { Client } from 'pg';

class Database {
  private client: Client;

  constructor(private config: DatabaseConfig) {
    this.client = new Client({
      host: config.host,
      port: config.port,
      database: config.database,
      user: config.username,
      password: config.password,
    });
  }

  async connect() {
    await this.client.connect();
  }

  async query(sql: string, params?: any[]) {
    const res = await this.client.query(sql, params);
    return res.rows;
  }

  async disconnect() {
    await this.client.end();
  }
}
```

---

## 7. Notes

- **Async/Await**: All I/O methods return `Promise`s; use `await` or `.then()`.
- **Type Safety**: The `query` method returns `any[]`. In a real project, you’d replace `any` with a generic or a typed result set.
- **Sanitisation**: `sanitizeInput` is very basic. For production use, prefer parameterised queries or a dedicated sanitisation library.
- **Testing**: The skeleton is ideal for unit tests; you can mock the methods to simulate database behaviour.

---

Happy coding! 🚀
