---
title: Database
layout: default
---

_Last updated: 2025-11-16_

# database.ts

*Auto-generated from `./database.ts`*

# `database.ts` – API Documentation

> **What this module does**  
> A lightweight, TypeScript‑friendly wrapper that defines a database configuration interface, a `Database` class with async connection helpers, a factory function to create a connected instance, and a simple input‑sanitisation helper.  
> The implementation is intentionally minimal – the methods are placeholders that you can replace with your own driver logic (e.g. `pg`, `mysql2`, `sqlite3`, etc.).

> **Note**: The actual connection logic is omitted in this snippet; in a real implementation you would replace the placeholder comments with a driver such as `pg`, `mysql2`, or `sqlite3`.

---

## Overview

`database.ts` provides a lightweight abstraction for establishing a database connection, executing queries, and safely handling user input.

- **`DatabaseConfig`** – Describes the connection parameters (host, port, database name, username, password).  
- **`Database`** – A class that manages the lifecycle of a connection and exposes `connect()`, `query()`, and `disconnect()` methods.  
- **`createConnection`** – A helper that creates a `Database` instance and automatically connects it.  
- **`sanitizeInput`** – A small utility that removes potentially dangerous characters (`'`, `"`, `;`) from strings before they are used in SQL statements.

> **Note**: The actual database driver logic is omitted; replace the bodies of `connect`, `query`, and `disconnect` with your preferred driver (e.g., `pg`, `mysql`, `sqlite3`).

---

## Exports

| Export            | Type            | Description                                                                 |
|-------------------|-----------------|-----------------------------------------------------------------------------|
| `DatabaseConfig`  | **Interface**   | Configuration object for a database connection.                             |
| `Database`        | **Class**       | Encapsulates a database connection and exposes `connect`, `query`, and `disconnect` methods. |
| `createConnection`| **Function**    | Convenience factory that creates a `Database` instance and automatically connects it. |
| `sanitizeInput`   | **Function**    | Utility that removes potentially dangerous characters (`'`, `"`, `;`) from a string. |

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

| Property   | Type     | Description                                 |
|------------|----------|---------------------------------------------|
| `host`     | `string` | Database host address (e.g., `"localhost"`). |
| `port`     | `number` | Port number the database listens on.        |
| `database` | `string` | Name of the database/schema.                |
| `username` | `string` | Username for authentication.                |
| `password` | `string` | Password for authentication.                |

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

### 2. `Database` (Class)

*Documentation for the `Database` class can be added here.* *(Placeholder for future expansion.)*

### 3. `createConnection` (Function)

*Documentation for the `createConnection` factory can be added here.* *(Placeholder for future expansion.)*

### 4. `sanitizeInput` (Function)

*Documentation for the `sanitizeInput` utility can be added here.* *(Placeholder for future expansion.)*