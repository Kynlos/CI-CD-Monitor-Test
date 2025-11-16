# database.ts

*Auto-generated from `./database.ts`*

# `database.ts` – API Documentation

## Overview
`database.ts` provides a lightweight abstraction for connecting to a relational database, executing queries, and safely handling user input.  
- **`DatabaseConfig`** – Describes the connection parameters.  
- **`Database`** – A class that manages a single connection lifecycle.  
- **`createConnection`** – A convenience factory that returns a connected `Database` instance.  
- **`sanitizeInput`** – A helper that removes potentially dangerous characters from strings before they are used in SQL statements.

> **Note**: The actual connection logic is omitted in this snippet; in a real implementation you would replace the placeholder comments with a driver such as `pg`, `mysql2`, or `sqlite3`.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `DatabaseConfig` | `interface` | Defines the configuration needed to connect to a database. |
| `Database` | `class` | Manages a database connection and provides `connect`, `query`, and `disconnect` methods. |
| `createConnection` | `function` | Async factory that creates and connects a `Database` instance. |
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

async function run() {
  await db.connect();          // Open the connection
  const users = await db.query(
    'SELECT * FROM users WHERE age > $1',
    [30]
  );
  console.log(users);
  await db.disconnect();       // Close the connection
}
run().catch(console.error);
```

### 3. `createConnection` Factory

```ts
import { createConnection, DatabaseConfig } from './database';

const config: DatabaseConfig = { /* … */ };

async function main() {
  const db = await createConnection(config); // connects automatically
  const rows = await db.query('SELECT * FROM products');
  console.log(rows);
  await db.disconnect();
}
main().catch(console.error);
```

### 4. `sanitizeInput`

```ts
import { sanitizeInput } from './database';

const unsafe = "O'Reilly; DROP TABLE users;";
