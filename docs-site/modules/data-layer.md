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
`database.ts` provides a lightweight abstraction for connecting to a relational database, executing SQL queries, and safely sanitizing user input.  
It intentionally contains only the minimal plumbing needed to illustrate the API; the actual driver logic (e.g., `pg`, `mysql2`, `sqlite3`) is omitted and should be implemented in the placeholder methods `connect`, `query`, and `disconnect`.

The module exports:

| Export | Type | Description |
|--------|------|-------------|
| `DatabaseConfig` | **Interface** | Configuration object for a database connection. |
| `Database` | **Class** | Encapsulates a database connection and exposes `connect`, `query`, and `disconnect` methods. |
| `createConnection` | **Function** | Convenience factory that creates a `Database` instance and automatically connects it. |
| `sanitizeInput` | **Function** | Utility that removes potentially dangerous characters from a string. |

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `DatabaseConfig` | **interface** | Configuration object for a database connection. |
| `Database` | **class** | Represents a database connection with methods to connect, query, and disconnect. |
| `createConnection` | **function** | Factory that creates and connects a `Database` instance. |
| `sanitizeInput` | **function** | Removes potentially dangerous characters from a string. |

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
- **`connect()`** – Opens a connection to the database. *Returns:* `Promise<void>`  
- **`query(sql, params?)`** – Executes a SQL statement.  
  - `sql` – The SQL string to execute.  
  - `params` – Optional array of parameters for prepared statements.  
  *Returns:* `Promise<any[]>` – Array of rows returned by the query.  
- **`disconnect()`** – Closes the connection. *Returns:* `Promise<void>`  

> **Note**: Replace the bodies of `connect`, `query`, and `disconnect` with calls to your preferred driver (e.g., `pg`, `mysql`, `sqlite3`).

### 3. `createConnection` (Function)

```ts
export async function createConnection(config: DatabaseConfig): Promise<Database> {
  const db = new Database(config);
  await db.connect();
  return db;
}
```

- **Purpose** – Convenience factory that creates a `Database` instance and automatically connects it.

### 4. `sanitizeInput` (Function)

```ts
export function sanitizeInput(input: string): string {
  // Very naive sanitisation – replace characters that are commonly used in SQL injection.
  return input.replace(/[;'"]/g, '');
}
```

- **Purpose** – Removes potentially dangerous characters from a string before it is interpolated into a query.

---

## Usage Examples

### 1. `DatabaseConfig`

```ts
import { DatabaseConfig } from './database';

const config: DatabaseConfig = {
  host: 'localhost',
  port: 5432,
  database: 'mydb',
  username: 'admin',
  password: 'secret',
};
```

### 2. `Database` Class

```ts
import { Database, DatabaseConfig } from './database';

const config: DatabaseConfig = { /* … */ };
const db = new Database(config);

async function run() {
  await db.connect();                     // 1️⃣ Open connection
  const rows = await db.query('SELECT * FROM users WHERE id = $1', [42]); // 2️⃣ Query
  console.log(rows);
  await db.disconnect();                  // 3️⃣ Close connection
}
run();
```

### 3. `createConnection` Factory

```ts
import { createConnection, DatabaseConfig } from './database';

async function init() {
  const config: DatabaseConfig = { /* … */ };
  const db = await createConnection(config); // connects automatically
  const users = await db.query('SELECT * FROM users');
  console.log(users);
  await db.disconnect();
}
init();
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

### `DatabaseConfig`

| Property | Type   | Description                              |
|----------|--------|------------------------------------------|
| `host`   | string | Database server hostname or IP.          |
| `port`   | number | TCP port number.                         |
| `database`| string| Name of the database to connect to.      |
| `username`| string| User credential.                         |
| `password`| string| User credential.                         |

### `Database.connect()`
No parameters.

### `Database.query(sql, params?)`

| Parameter | Type    | Description                                   |
|-----------|---------|-----------------------------------------------|
| `sql`     | string  | SQL statement to execute.                     |
| `params`  | any[]   | (optional) Positional parameters for prepared statements. |

```ts
// Example:
await db.query('SELECT * FROM users WHERE id = $1', [42]);
```

--- 

*Generated by the documentation editor on 2025-11-16.* 
```