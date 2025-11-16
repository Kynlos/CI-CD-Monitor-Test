# database.ts

*Auto-generated from `./database.ts`*

# `database.ts` – API Documentation

## Overview
`database.ts` provides a lightweight abstraction for connecting to a relational database, executing queries, and safely sanitizing user input.  
The module exports:

| Export | Type | Description |
|--------|------|-------------|
| `DatabaseConfig` | **Interface** | Configuration object for a database connection. |
| `Database` | **Class** | Encapsulates a database connection and exposes `connect`, `query`, and `disconnect` methods. |
| `createConnection` | **Function** | Convenience factory that creates a `Database` instance and automatically connects it. |
| `sanitizeInput` | **Function** | Utility that removes potentially dangerous characters from a string. |

> **Note**: The actual database driver logic is omitted; the methods contain placeholders. Replace the body of `connect`, `query`, and `disconnect` with your preferred driver (e.g., `pg`, `mysql`, `sqlite3`).

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
export async function createConnection(config: DatabaseConfig): Promise<Database>;
```

- **Purpose** – Instantiates a `Database`, connects it, and returns the connected instance.  
- **Parameters:**  
  - `config` – `DatabaseConfig` object.  
- **Returns:** `Promise<Database>` – A connected `Database` instance.

### 4. `sanitizeInput` (Function)

```ts
export function sanitizeInput(input: string): string;
```

- **Purpose** – Removes semicolons, single quotes, and double quotes from a string to mitigate simple injection attacks.  
- **Parameters:**  
  - `input` – The raw string to sanitize.  
- **Returns:** `string` – The sanitized string.

---

## Usage Examples

### 1. Using `DatabaseConfig` & `Database`

```ts
import { Database, DatabaseConfig } from './database';

const config: DatabaseConfig = {
  host: 'localhost',
  port: 5432,
  database: 'mydb',
  username: 'user',
  password: 'pass',
};

async function run() {
  const db = new Database(config);
  await db.connect();

  const users = await db.query('SELECT * FROM users WHERE id = $1', [1]);
  console.log(users);

  await db.disconnect();
}

run().catch(console.error);
```

### 2. Using `createConnection`

```ts
import { createConnection, DatabaseConfig } from './database';

const config: DatabaseConfig = {
  host: 'localhost',
  port: 5432,
  database: 'mydb',
  username: 'user',
  password: 'pass',
};

async function main() {
  const db = await createConnection(config);

  const rows = await db.query('SELECT * FROM products');
  console.log(rows);

  await db.disconnect();
}

main().catch(console.error);
```

### 3. Using `sanitizeInput`

```ts
import { sanitizeInput } from './database';

const raw = "O'Reilly; DROP TABLE users; \"admin\"";
const safe = sanitizeInput(raw);

console.log(safe); // OReilly DROP TABLE users admin
```

---

## Parameters & Return Values

| Function / Method | Parameters | Return Value | Notes |
|-------------------|------------|--------------|-------|
| `Database` constructor | `config: DatabaseConfig` | `void` | Stores config internally. |
| `connect()` | – | `Promise<void>` | Opens DB connection. |
| `query(sql, params?)` | `sql: string`, `params?: any[]` | `Promise<any[]>` | Returns rows; empty array placeholder. |
| `disconnect()` | – | `Promise<void>` | Closes DB connection. |
| `createConnection(config)` | `config: DatabaseConfig` | `Promise<Database>` | Returns a connected instance. |
| `sanitizeInput(input)` | `input: string` | `string` | Removes `;`, `'`, `"` characters. |

---

## Extending the Module

1. **Replace placeholders** – Insert your database driver logic inside `connect`, `query`, and `disconnect`.  
2. **Add error