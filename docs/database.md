# database.ts

*Auto-generated from `./database.ts`*

# `database.ts` – API Documentation

## Overview
`database.ts` provides a lightweight abstraction for establishing a database connection, executing queries, and safely handling user input.  
- **`DatabaseConfig`** – Describes the connection parameters.  
- **`Database`** – A class that manages the lifecycle of a connection and exposes `connect`, `query`, and `disconnect` methods.  
- **`createConnection`** – A helper that creates a `Database` instance and automatically connects it.  
- **`sanitizeInput`** – A small utility that removes potentially dangerous characters from strings.

> **Note**: The actual database driver logic is omitted; the methods contain placeholder comments. Replace them with your preferred driver (e.g., `pg`, `mysql`, `sqlite3`, etc.) to make the module functional.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `DatabaseConfig` | **Interface** | Connection configuration object. |
| `Database` | **Class** | Manages a database connection. |
| `createConnection` | **Function** | Instantiates and connects a `Database`. |
| `sanitizeInput` | **Function** | Escapes single quotes, double quotes, and semicolons. |

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
| Property | Type | Description |
|----------|------|-------------|
| `host` | `string` | Database host address (e.g., `"localhost"`). |
| `port` | `number` | Port number the database listens on. |
| `database` | `string` | Name of the database/schema. |
| `username` | `string` | Username for authentication. |
| `password` | `string` | Password for authentication. |

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

#### Constructor
- **`new Database(config)`**
  - **Parameter**: `config` – `DatabaseConfig` object.
  - **Effect**: Stores the configuration for later use.

#### Methods

| Method | Parameters | Return Value | Description |
|--------|------------|--------------|-------------|
| `connect()` | – | `Promise<void>` | Establishes a connection to the database. |
| `query(sql, params?)` | `sql: string` – SQL statement.<br>`params?: any[]` – Optional array of bind parameters. | `Promise<any[]>` – Array of rows returned by the query. | Executes the provided SQL and returns the result set. |
| `disconnect()` | – | `Promise<void>` | Closes the database connection. |

#### Usage Example
```ts
import { Database, DatabaseConfig } from './database';

const config: DatabaseConfig = {
  host: 'localhost',
  port: 3306,
  database: 'shop',
  username: 'root',
  password: 'password',
};

async function run() {
  const db = new Database(config);
  await db.connect();

  const users = await db.query('SELECT * FROM users WHERE age > ?', [30]);
  console.log(users);

  await db.disconnect();
}

run().catch(console.error);
```

---

### 3. `createConnection` (Function)

```ts
export async function createConnection(config: DatabaseConfig): Promise<Database>;
```

#### Parameters
| Name | Type | Description |
|------|------|-------------|
| `config` | `DatabaseConfig` | Connection configuration. |

#### Return Value
- `Promise<Database>` – A `Database` instance that is already connected.

#### Usage Example
```ts
import { createConnection, DatabaseConfig } from './database';

const config: DatabaseConfig = {
  host: 'db.example.com',
  port: 5432,
  database: 'analytics',
  username: 'analytics_user',
  password: 'p@ssw0rd',
};

async function main() {
  const db = await createConnection(config);
  const stats = await db.query('SELECT COUNT(*) AS total FROM events');
  console.log(stats);
  await db.disconnect();
}

main().catch(console.error);
```

---

### 4. `sanitizeInput` (Function)

```ts
export function sanitizeInput(input: string): string;
```

#### Parameters
| Name | Type | Description |
|------|------|-------------|
| `input` | `string` | Raw user input that may contain dangerous characters. |

#### Return Value
- `string` – The input string with all semicolons (`;`), single quotes (`'`), and double quotes (`"`) removed.

#### Usage Example
```ts
import { sanitizeInput } from './database';

const raw = "O'Reilly; DROP TABLE users; \"admin\"";
const safe = sanitizeInput(raw);
console.log(safe); // OReilly DROP TABLE users admin
```

> **Caution**: `sanitizeInput` is a very simple sanitizer. For production use, prefer parameterized queries or a robust escaping library.

---

## Quick Reference

| Export | Purpose |
|--------|---------|
| `DatabaseConfig` | Connection settings |
| `Database` | Connection lifecycle & query execution |
| `createConnection` | Convenience factory that auto‑connects |
| `sanitizeInput` | Basic input sanitization |

Feel free to extend the class with additional helpers (e.g., transaction support, connection pooling) and replace the placeholder logic with a real database driver.