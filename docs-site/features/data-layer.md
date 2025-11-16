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
`database.ts` provides a lightweight, TypeScript‑friendly abstraction for connecting to a relational database, executing queries, and safely sanitising user input.  
The module exports:

| Export               | Type      | Description                                                                 |
|----------------------|-----------|-----------------------------------------------------------------------------|
| `DatabaseConfig`     | Interface | Configuration object for a database connection.                            |
| `Database`           | Class     | Encapsulates a database connection and exposes `connect`, `query`, and `disconnect` methods. |
| `createConnection`   | Function  | Convenience factory that creates a `Database` instance and automatically connects it. |
| `sanitizeInput`      | Function  | Utility that removes potentially dangerous characters (`'`, `"`, `;`) from a string. |

> **Note**: The actual database driver logic is omitted; replace the bodies of `connect`, `query`, and `disconnect` with your preferred driver (e.g., `pg`, `mysql2`, or `sqlite3`).

---

## Exports

### 1. `DatabaseConfig` (Interface)

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

### 2. `Database` (Class)

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
- **`connect()`** – Opens a connection to the database.  
  *Returns:* `Promise<void>`  
- **`query(sql, params?)`** – Executes a SQL statement.  
  *Parameters:*  
  - `sql` – The SQL string to execute.  
  - `params` – Optional array of parameters for prepared statements.  
  *Returns:* `Promise<any[]>` – Array of rows returned by the query.  
- **`disconnect()`** – Closes the database connection.  
  *Returns:* `Promise<void>`

### 3. `createConnection` (Function)

```ts
export async function createConnection(
  config: DatabaseConfig
): Promise<Database> {
  const db = new Database(config);
  await db.connect(); // automatically connects
  return db;
}
```

- **Purpose** – Creates a `Database` instance **and** connects it, returning the ready‑to‑use object.

### 4. `sanitizeInput` (Function)

```ts
export function sanitizeInput(input: string): string {
  // Remove single quotes, double quotes, and semicolons
  return input.replace(/[\'\";]+/g, '');
}
```

- **Purpose** – Strips potentially dangerous characters from a string before it is interpolated into SQL statements.

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

```