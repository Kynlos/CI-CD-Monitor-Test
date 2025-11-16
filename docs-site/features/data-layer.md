---
title: Data Layer
layout: default
last_updated: 2025-11-16
---

# database.ts

*Auto-generated from `./database.ts`*

# `database.ts` – API Documentation

## Overview
`database.ts` provides a lightweight abstraction for establishing a database connection, executing queries, and safely handling user input.

- **`DatabaseConfig`** – Describes the connection parameters.  
- **`Database`** – A class that manages the lifecycle of a connection and exposes `connect`, `query`, and `disconnect` methods.  
- **`createConnection`** – A helper that creates a `Database` instance and automatically connects it.  
- **`sanitizeInput`** – A small utility that removes (or escapes) potentially dangerous characters from strings.

> **Note**: The actual database driver logic is omitted; the methods contain placeholder comments. Replace them with your preferred driver (e.g., `pg`, `mysql2`, `sqlite3`, etc.) to make the module functional.

---

## Exports

| Export            | Type      | Description                                                            |
|-------------------|-----------|------------------------------------------------------------------------|
| `DatabaseConfig`  | Interface | Connection configuration object.                                      |
| `Database`        | Class     | Manages a database connection.                                         |
| `createConnection`| Function  | Instantiates and connects a `Database`.                                |
| `sanitizeInput`   | Function  | Escapes/removes single quotes, double quotes, and semicolons.          |

---

## Detailed API

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

#### Parameters
| Property   | Type   | Description                              |
|------------|--------|------------------------------------------|
| `host`     | `string` | Database host address (e.g., `"localhost"`). |
| `port`     | `number` | Port number the database listens on.    |
| `database` | `string` | Name of the database/schema.            |
| `username` | `string` | Username for authentication.            |
| `password` | `string` | Password for authentication.            |

#### Usage Example
```ts
const config: DatabaseConfig = {
  host: '127.0.0.1',
  port: 5432,
  database: 'my_app',
  username: 'app_user',
  password: 's3cr3t',
};
```

---

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

---

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

---

### 4. `sanitizeInput` (Function)

```ts
export function sanitizeInput(input: string): string {
  // Remove single quotes, double quotes, and semicolons
  return input.replace(/[\'\";]+/g, '');
}
```

- **Purpose** – Strips (or escapes) potentially dangerous characters from a string before it is interpolated into SQL statements.