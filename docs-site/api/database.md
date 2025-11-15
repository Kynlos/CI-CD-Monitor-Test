---
title: Database
layout: default
---

# database.ts

*Auto-generated from `./database.ts`*

# database.ts – API Documentation

## Overview
`database.ts` provides a lightweight abstraction for connecting to a relational database, executing queries, and safely handling user input.  
- **`DatabaseConfig`** – Type that describes the connection parameters.  
- **`Database`** – Class that manages a connection lifecycle (`connect`, `query`, `disconnect`).  
- **`createConnection`** – Helper that creates and connects a `Database` instance in one step.  
- **`sanitizeInput`** – Utility that removes potentially dangerous characters from a string.

> **Note**: The actual database driver implementation is omitted; the methods contain placeholders. Replace them with your preferred driver (e.g., `pg`, `mysql`, `sqlite3`) to make the module functional.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `DatabaseConfig` | `interface` | Configuration object for a database connection. |
| `Database` | `class` | Handles connection lifecycle and query execution. |
| `createConnection` | `function` | Factory that returns a connected `Database` instance. |
| `sanitizeInput` | `function` | Removes single quotes, double quotes, and semicolons from a string. |

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

const config: DatabaseConfig = { /* … */ };
const db = new Database(config);

await db.connect();

const users = await db.query('SELECT * FROM users WHERE id = $1', [42]);

await db.disconnect();
```

### 3. `createConnection` Helper

```ts
import { createConnection, DatabaseConfig } from './database';

const config: DatabaseConfig = { /* … */ };
const db = await createConnection(config);

// Use the connected instance
const posts = await db.query('SELECT * FROM posts ORDER BY created_at DESC');
```

### 4. `sanitizeInput` Utility

```ts
import { sanitizeInput } from './database';

const raw = "O'Reilly; DROP TABLE users; --";
const safe = sanitizeInput(raw);
// safe === "OReilly DROP TABLE users --"
```

---

## Parameters

| Function/Method | Parameter | Type | Description |
|-----------------|-----------|------|-------------|
| `Database` (constructor) | `config` | `DatabaseConfig` | Connection settings. |
| `Database.connect` | *none* | `void` | Initiates the connection. |
| `Database.query` | `sql` | `string` | SQL statement to execute. |
| | `params` | `any[]` | Optional array of bind parameters. |
| `Database.disconnect` | *none* | `void` | Closes the connection. |
| `createConnection` | `config` | `DatabaseConfig` | Same as the constructor. |
| `sanitizeInput` | `input` | `string` | Raw user input. |

---

## Return Values

| Function/Method | Return Type | Description |
|-----------------|-------------|-------------|
| `Database.connect` | `Promise<void>` | Resolves when the connection is established. |
| `Database.query` | `Promise<any[]>` | Resolves with an array of rows returned by the query. |
| `Database.disconnect` | `Promise<void>` | Resolves when the connection is closed. |
| `createConnection` | `Promise<Database>` | Resolves with a connected `Database` instance. |
| `sanitizeInput` | `string` | The sanitized string with `'`, `"`, and `;` removed. |

---

## Extending the Module

1. **Add a real driver** – Replace the placeholder comments in `connect`, `query`, and `disconnect` with calls to your chosen database library.  
2. **Error handling** – Wrap driver calls in `try/catch` blocks and expose meaningful error messages.  
3. **Connection pooling** – If your driver supports pooling, integrate it into the `Database` class.  
4. **Type safety** – Define generic return types for `query` (e.g., `Promise<T[]>`) to enforce schema contracts.

---

### Quick Reference

```ts
// Import
import { createConnection, sanitizeInput, DatabaseConfig } from './database';

// Config
const cfg: DatabaseConfig = { host: 'localhost', port: 5432, database: 'demo', username: 'demo', password: 'demo' };

// Connect
const db = await createConnection(cfg);

// Query
const rows = await db.query('SELECT * FROM users WHERE email = $1', ['alice@example.com']);

// Disconnect
await db.disconnect();

// Sanitize
const safe = sanitizeInput("O'Reilly; DROP TABLE users;");
```

Happy coding!
