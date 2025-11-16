# auth.ts

*Auto-generated from `./auth.ts`*

# Authentication Module – `auth.ts`

## Overview
The **Authentication** module provides a minimal, type‑safe API for user authentication, session handling, and token generation.  
It defines:

- **Data contracts** (`User`, `LoginOptions`) for user information and login behaviour.
- A **service class** (`AuthService`) that encapsulates the core authentication logic.
- Two **utility functions** (`hashPassword`, `generateToken`) for password hashing and JWT creation.

> **⚠️ Note** – The current implementation contains placeholder logic (`return {} as User`, `return 'token'`, etc.). Replace these stubs with real database lookups, password hashing, and JWT handling before using in production.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `User` | **Interface** | Represents a user record. |
| `LoginOptions` | **Interface** | Optional parameters for the login flow. |
| `AuthService` | **Class** | Provides methods to login, logout, and validate tokens. |
| `hashPassword` | **Function** | Hashes a plain‑text password. |
| `generateToken` | **Function** | Generates a JWT token for a user. |

---

## Usage Examples

### 1. `User` Interface
```ts
import { User } from './auth';

const user: User = {
  id: '123',
  username: 'alice',
  email: 'alice@example.com',
};
```

### 2. `LoginOptions` Interface
```ts
import { LoginOptions } from './auth';

const options: LoginOptions = {
  rememberMe: true,
  timeout: 3600, // seconds
};
```

### 3. `AuthService`

```ts
import { AuthService, LoginOptions, User } from './auth';

const auth = new AuthService();

// Login
async function doLogin() {
  const user: User = await auth.login('alice', 'secret', { rememberMe: true });
  console.log('Logged in:', user);
}

// Logout
async function doLogout(userId: string) {
  await auth.logout(userId);
  console.log('Logged out');
}

// Validate JWT
async function checkToken(token: string) {
  const user: User = await auth.validateToken(token);
  console.log('Token belongs to:', user.username);
}
```

### 4. `hashPassword`

```ts
import { hashPassword } from './auth';

const plain = 'myPassword123';
const hashed = hashPassword(plain);
console.log('Hashed password:', hashed);
```

### 5. `generateToken`

```ts
import { generateToken } from './auth';

const token = generateToken('123'); // userId
console.log('JWT:', token);
```

---

## Parameters

| Function / Method | Parameter | Type | Description |
|-------------------|-----------|------|-------------|
| `AuthService.login` | `username` | `string` | The user’s login name. |
| | `password` | `string` | The user’s plain‑text password. |
| | `options?` | `LoginOptions` | Optional login behaviour flags. |
| `AuthService.logout` | `userId` | `string` | The ID of the user to log out. |
| `AuthService.validateToken` | `token` | `string` | JWT token to validate. |
| `hashPassword` | `password` | `string` | Plain‑text password to hash. |
| `generateToken` | `userId` | `string` | The ID of the user for whom to create a token. |

---

## Return Values

| Function / Method | Return Type | Description |
|-------------------|-------------|-------------|
| `AuthService.login` | `Promise<User>` | Resolves to the authenticated `User` object. |
| `AuthService.logout` | `Promise<void>` | Resolves when the session is cleared. |
| `AuthService.validateToken` | `Promise<User>` | Resolves to the `User` represented by the token. |
| `AuthService.validateCredentials` | `Promise<User>` | **Private** – resolves to a `User` after DB lookup. |
| `hashPassword` | `string` | Returns the hashed password (currently a placeholder). |
| `generateToken` | `string` | Returns a JWT token string (currently a placeholder). |

---

## Extending the Module

1. **Replace placeholders**  
   - Implement real password hashing (e.g., `bcrypt` or `argon2`).  
   - Generate real JWTs with a secret key and proper claims.

2. **Persist sessions**  
   - Store session data in a store (Redis, database, etc.) inside `logout` and `validateToken`.

3. **Error handling**  
   - Throw descriptive errors (`InvalidCredentialsError`, `TokenExpiredError`, etc.) instead of returning empty objects.

4. **Unit tests**  
   - Write tests for each method, mocking database and crypto operations.

---

### Quick Reference

```ts
// Import
import { AuthService, hashPassword, generateToken } from './auth';

// Create service
const auth = new AuthService();

// Login
const user = await auth.login('bob', 's3cr3t', { rememberMe: true });

// Hash password
const hashed = hashPassword('s3cr3t');

// Generate JWT
const token = generateToken(user.id);
```

---