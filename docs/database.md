# database.ts

*Auto-generated from `./database.ts`*

# Database Module (`database.ts`)

## Overview
The **database** module provides a lightweight, type‑safe wrapper around a generic database connection.  
It exposes:

- A `DatabaseConfig` interface for connection settings.  
- A `Database` class that manages a connection lifecycle (`connect`, `query`, `disconnect`).  
- A convenience factory `createConnection` that returns a connected instance.  
- A helper `sanitizeInput` that removes common SQL‑injection characters from a string.

The module is intentionally minimal – it can be swapped out for a real driver (e.g., `pg`, `mysql2`, `sqlite3`) by implementing the stubbed methods.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `DatabaseConfig` | `interface` | Configuration object for a database connection. |
| `Database` | `class` | Encapsulates a database connection and provides query execution. |
| `createConnection` | `function` | Factory that creates and connects a `Database` instance. |
| `sanitizeInput` | `function` | Removes potentially dangerous characters from a string. |

---

## Usage Examples

### 1. `DatabaseConfig`

```ts
import { DatabaseConfig } from './database';

const config: DatabaseConfig = {
  host: 'localhost',
  port: 5432,
  database: 'my_app',
  username: 'app_user',
  password: 's3cr3t',
};
```

### 2. `Database` Class

```ts
import { Database, DatabaseConfig } from './database';

const config: DatabaseConfig = { /* ... */ };
const db = new Database(config);

await db.connect();                     // Open the connection
const rows = await db.query('SELECT * FROM users WHERE id = $1', [42]); // Execute query
console.log(rows);
await db.disconnect();                  // Close the connection
```

### 3. `createConnection`

```ts
import { createConnection, DatabaseConfig } from './database';

const config: DatabaseConfig = { /* ... */ };

async function run() {
  const db = await createConnection(config); // Automatically connects
  const users = await db.query('SELECT * FROM users');
  console.log(users);
  await db.disconnect();
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

## Parameters

### `DatabaseConfig`
| Property | Type | Description |
|----------|------|-------------|
| `host` | `string` | Database host address. |
| `port` | `number` | TCP port of the database server. |
| `database` | `string` | Name of the database to connect to. |
| `username` | `string` | Username for authentication. |
| `password` | `string` | Password for authentication. |

### `Database.connect()`
| Parameter | Type | Description |
|-----------|------|-------------|
| *none* | – | No parameters. |

### `Database.query(sql, params?)`
| Parameter | Type | Description |
|-----------|------|-------------|
| `sql` | `string` | The SQL statement to execute. |
| `params` | `any[]` | Optional array of parameters for parameterized queries. |

### `Database.disconnect()`
| Parameter | Type | Description |
|-----------|------|-------------|
| *none* | – | No parameters. |

### `createConnection(config)`
| Parameter | Type | Description |
|-----------|------|-------------|
| `config` | `DatabaseConfig` | Connection configuration. |

### `sanitizeInput(input)`
| Parameter | Type | Description |
|-----------|------|-------------|
| `input` | `string` | Raw user input that may contain dangerous characters. |

---

## Return Values

| Function | Return Type | Description |
|----------|-------------|-------------|
| `Database.connect()` | `Promise<void>` | Resolves when the connection is established. |
| `Database.query(sql, params?)` | `Promise<any[]>` | Resolves with an array of rows returned by the query. |
| `Database.disconnect()` | `Promise<void>` | Resolves when the connection is closed. |
| `createConnection(config)` | `Promise<Database>` | Resolves with a `Database` instance that is already connected. |
| `sanitizeInput(input)` | `string` | The sanitized string with `'`, `;`, and `"` removed. |

---

## Notes

- The current implementation contains placeholder logic (`// Establish connection`, `// Execute query`, `// Close connection`). Replace these with actual driver code (e.g., `pg.Client`, `mysql2.Connection`) for production use.
- `sanitizeInput` is a very simple sanitizer. For real applications, use parameterized queries or a dedicated sanitization library.
- All methods are `async` and return `Promise`s, allowing them to be used with `await` or `.then()`.

---