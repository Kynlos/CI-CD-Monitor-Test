```markdown
---
title: Database
layout: default
---

_Last updated: 2025-11-16_

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

The module exports:

| Export            | Type       | Description                                                                 |
|-------------------|------------|-----------------------------------------------------------------------------|
| `DatabaseConfig`  | **Interface** | Configuration object for a database connection. |
| `Database`        | **Class**  | Encapsulates a database connection and exposes `connect`, `query`, and `disconnect` methods. |
| `createConnection`| **Function**| Convenience factory that creates a `Database` instance and automatically connects it. |
| `sanitizeInput`   | **Function**| Utility that removes potentially dangerous characters from a string. |

> **Note**: The actual database driver logic is omitted; replace the bodies of `connect`, `query`, and `disconnect` with your preferred driver (e.g., `pg`, `mysql`, `sqlite3`).

---

## 1. Exports

| Export            | Type       | Description                                                                 |
|-------------------|------------|-----------------------------------------------------------------------------|
| `DatabaseConfig`  | `interface`| Defines the configuration needed to connect to a database.                 |
| `Database`        | `class`    | Manages a database connection and provides `connect`, `query`, and `disconnect` methods. |
| `createConnection`| `function`| Async factory that creates **and connects** a `Database` instance.          |
| `sanitizeInput`   | `function`| Removes single quotes, double quotes, and semicolons from a string.        |

### 1.1 `DatabaseConfig` (Interface)

```ts
export interface DatabaseConfig {
  host: string;
  port: number;
  database: string;
  username: string;
  password: string;
}
```

- **Purpose** – Describes the connection parameters required by the `Database` class.

### 1.2 `Database` (Class)

```ts
export class Database {
  private config: DatabaseConfig;

  constructor(config: DatabaseConfig);
  async connect(): Promise<void>;
  async query(sql: string, params?: any[]): Promise<any[]>;
  async disconnect(): Promise<void>;
}
```

- **Constructor** – Instantiates a new `Database` object with the supplied configuration.  
- **`connect()`** – Opens a connection to the database. Returns `Promise<void>`.  
- **`query(sql, params?)`** – Executes a SQL statement.  
  - `sql` – The SQL string to execute.  
  - `params` – Optional array of parameters for prepared statements.  
  Returns `Promise<any[]>` – an array of rows returned by the query.  
- **`disconnect()`** – Closes the connection. Returns `Promise<void>`.

### 1.3 `createConnection` (Function)

```ts
export async function createConnection(config: DatabaseConfig): Promise<Database> {
  const db = new Database(config);
  await db.connect();
  return db;
}
```

- **Purpose** – Convenience factory that creates a `Database` instance and automatically connects it.

### 1.4 `sanitizeInput` (Function)

```ts
export function sanitizeInput(input: string): string {
  return input.replace(/['";]/g, '');
}
```

- **Purpose** – Removes single quotes, double quotes, and semicolons from a string to help prevent SQL injection.

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

  const products = await db.query(
    'SELECT * FROM products WHERE price < $1',
    [100]
  );
  console.log(products);

  await db.disconnect(); // Close when done
}

runFactory().catch(console.error);
```

--- 

*End of documentation.*
```