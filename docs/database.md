# database.ts

*Auto-generated from `./database.ts`*

# database.ts – API Documentation

## Overview
`database.ts` provides a lightweight abstraction for managing a database connection and executing SQL queries.  
It exposes:

- A `DatabaseConfig` interface for connection settings.  
- A `Database` class that handles connection lifecycle and query execution.  
- Helper functions: `createConnection` (factory) and `sanitizeInput` (basic SQL‑injection guard).

The module is intentionally minimal and can be extended with a real driver (e.g., `pg`, `mysql2`) by implementing the placeholder methods.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `DatabaseConfig` | **interface** | Configuration object for a database connection. |
| `Database` | **class** | Represents a database connection with methods to connect, query, and disconnect. |
| `createConnection` | **function** | Factory that creates and connects a `Database` instance. |
| `sanitizeInput` | **function** | Removes potentially dangerous characters from a string. |

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
| Property | Type | Description |
|----------|------|-------------|
| `host` | `string` | Database server hostname or IP. |
| `port` | `number` | TCP port number. |
| `database` | `string` | Name of the database to connect to. |
| `username` | `string` | User credential. |
| `password` | `string` | User credential. |

### `Database.connect()`
No parameters.

### `Database.query(sql, params?)`
| Parameter | Type | Description |
|-----------|------|-------------|
| `sql` | `string` | SQL statement to execute. |
| `params` | `any[]` (optional) | Positional parameters for parameterized queries. |

### `Database.disconnect()`
No parameters.

### `createConnection(config)`
| Parameter | Type | Description |
|-----------|------|-------------|
| `config` | `DatabaseConfig` | Connection configuration. |

### `sanitizeInput(input)`
| Parameter | Type | Description |
|-----------|------|-------------|
| `input` | `string` | Raw user input that may contain SQL meta‑characters. |

---

## Return Values

| Function | Returns | Notes |
|----------|---------|-------|
| `Database.connect()` | `Promise<void>` | Resolves when the connection is established. |
| `Database.query(sql, params?)` | `Promise<any[]>` | Resolves with an array of rows (empty array if none). |
| `Database.disconnect()` | `Promise<void>` | Resolves when the connection is closed. |
| `createConnection(config)` | `Promise<Database>` | Resolves with a connected `Database` instance. |
| `sanitizeInput(input)` | `string` | Returns the input string with `'`, `;`, and `"` removed. |

---

### Extending the Implementation

The placeholder methods (`connect`, `query`, `disconnect`) should be replaced with actual driver logic. For example, using `pg`:

```ts
import { Client } from 'pg';

export class Database {
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

Replace the placeholder comments accordingly to make the module functional.