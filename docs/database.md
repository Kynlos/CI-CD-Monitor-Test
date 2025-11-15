# database.ts

*Auto-generated from `./database.ts`*

# Database Module (`database.ts`)

## Overview
The **database** module provides a lightweight abstraction for connecting to a relational database, executing queries, and safely handling user input.  
It exposes:

- A `DatabaseConfig` interface for connection settings.
- A `Database` class that manages the connection lifecycle.
- A convenience factory `createConnection` that returns a ready‑to‑use `Database` instance.
- A `sanitizeInput` helper that removes common SQL‑injection characters from strings.

> **Note**: The actual database driver implementation is omitted; the methods contain placeholders (`// Establish connection`, etc.) that should be replaced with your preferred driver (e.g., `pg`, `mysql`, `sqlite3`).

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `DatabaseConfig` | Interface | Configuration object for a database connection. |
| `Database` | Class | Manages a database connection and provides query execution. |
| `createConnection` | Function | Factory that creates and connects a `Database` instance. |
| `sanitizeInput` | Function | Removes potentially dangerous characters from a string. |

---

## Usage Examples

### 1. `DatabaseConfig`

```ts
import { DatabaseConfig } from './database';

const config: DatabaseConfig = {
  host: 'localhost',
  port: 5432,
  database: 'mydb',
  username: 'user',
  password: 'pass',
};
```

### 2. `Database` Class

```ts
import { Database, DatabaseConfig } from './database';

const config: DatabaseConfig = { /* … */ };
const db = new Database(config);

await db.connect();          // Open the connection
const rows = await db.query('SELECT * FROM users WHERE id = $1', [1]); // Execute
await db.disconnect();       // Close the connection
```

### 3. `createConnection`

```ts
import { createConnection, DatabaseConfig } from './database';

const config: DatabaseConfig = { /* … */ };

(async () => {
  const db = await createConnection(config); // Already connected
  const users = await db.query('SELECT * FROM users');
  console.log(users);
  await db.disconnect();
})();
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
| `port` | `number` | Port number the database listens on. |
| `database` | `string` | Name of the database to connect to. |
| `username` | `string` | Username for authentication. |
| `password` | `string` | Password for authentication. |

### `Database.connect()`
No parameters.

### `Database.query(sql, params?)`
| Parameter | Type | Description |
|-----------|------|-------------|
| `sql` | `string` | The SQL statement to execute. |
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
| `input` | `string` | The string to sanitize. |

---

## Return Values

| Function | Return Type | Description |
|----------|-------------|-------------|
| `Database.connect()` | `Promise<void>` | Resolves when the connection is established. |
| `Database.query(sql, params?)` | `Promise<any[]>` | Resolves with an array of rows returned by the query. |
| `Database.disconnect()` | `Promise<void>` | Resolves when the connection is closed. |
| `createConnection(config)` | `Promise<Database>` | Resolves with a `Database` instance that is already connected. |
| `sanitizeInput(input)` | `string` | Returns the input string with `'`, `;`, and `"` characters removed. |

---

## Extending / Customizing

- **Driver Integration**: Replace the placeholder comments in `connect`, `query`, and `disconnect` with your database driver logic (e.g., using `pg.Client` for PostgreSQL).
- **Error Handling**: Wrap driver calls in `try/catch` blocks and re‑throw or log errors as needed.
- **Connection Pooling**: If your driver supports pooling, consider storing a pool instance instead of a single connection.

---

## License

This module is provided as-is under the MIT license. Feel free to adapt it to your project's needs.