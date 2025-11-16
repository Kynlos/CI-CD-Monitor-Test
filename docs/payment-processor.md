# payment-processor.ts

*Auto-generated from `./payment-processor.ts`*

# Payment Processor Module

The **payment‑processor.ts** module provides a lightweight abstraction for handling payment transactions, refunds, and transaction history.  
It exposes three async functions and two TypeScript interfaces that can be imported into any Node.js/TypeScript project.

> **Note** – The implementation is intentionally minimal and uses in‑memory stubs. Replace the helper functions (`chargePaymentMethod`, `getTransaction`, `processRefund`) with real payment‑gateway integrations for production use.

---

## 1. Overview

| Feature | Description |
|---------|-------------|
| `processPayment` | Authorises and captures a payment using a supplied `PaymentMethod`. |
| `refundTransaction` | Issues a refund for a previously completed transaction. |
| `getUserTransactions` | Retrieves all transactions belonging to a specific user. |
| `PaymentMethod` | Describes a payment instrument (card, bank, PayPal). |
| `Transaction` | Represents a payment record with status, amount, and metadata. |

The module is designed to be **stateless** – all persistence logic is delegated to the helper functions. This keeps the core logic testable and agnostic of any particular database or payment provider.

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| `PaymentMethod` | `interface` | Defines a payment instrument. |
| `Transaction` | `interface` | Represents a payment transaction. |
| `processPayment` | `function` | Processes a new payment. |
| `refundTransaction` | `function` | Refunds a completed transaction. |
| `getUserTransactions` | `function` | Retrieves all transactions for a user. |

---

## 3. Usage Examples

> **Prerequisites** – Install the module (or copy the file) and import the required symbols.

```ts
import {
  PaymentMethod,
  Transaction,
  processPayment,
  refundTransaction,
  getUserTransactions
} from './payment-processor';
```

### 3.1 Process a Payment

```ts
const card: PaymentMethod = {
  id: 'pm_123',
  type: 'card',
  last4: '4242',
  expiryDate: '12/25'
};

async function charge() {
  try {
    const tx: Transaction = await processPayment(5000, card); // $50.00
    console.log('Transaction status:', tx.status); // 'completed' or 'failed'
  } catch (err) {
    console.error('Payment failed:', err.message);
  }
}
```

### 3.2 Refund a Transaction

```ts
async function refund() {
  try {
    const refundedTx = await refundTransaction('txn_1699999999999_abc123');
    console.log('Refunded transaction:', refundedTx);
  } catch (err) {
    console.error('Refund error:', err.message);
  }
}
```

### 3.3 Retrieve User Transactions

```ts
async function listTransactions() {
  const userTxs = await getUserTransactions('user_456');
  console.log('User has', userTxs.length, 'transactions');
}
```

---

## 4. Parameters

### `processPayment(amount: number, method: PaymentMethod)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `amount` | `number` | Amount to charge **in cents** (e.g., 5000 = $50.00). Must be > 0. |
| `method` | `PaymentMethod` | The payment instrument to use. |

### `refundTransaction(transactionId: string)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `transactionId` | `string` | The unique identifier of the transaction to refund. |

### `getUserTransactions(userId: string)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `userId` | `string` | The user’s unique identifier. |

---

## 5. Return Values

| Function | Return Type | Description |
|----------|-------------|-------------|
| `processPayment` | `Promise<Transaction>` | Resolves to a `Transaction` object whose `status` is `'completed'` on success or `'failed'` on failure. |
| `refundTransaction` | `Promise<Transaction>` | Resolves to the original transaction object with `status` set to `'failed'` (indicating a refund). The `timestamp` is updated to the refund time. |
| `getUserTransactions` | `Promise<Transaction[]>` | Resolves to an array of `Transaction` objects belonging to the specified user. Currently returns an empty array – replace the stub with a real query. |

---

## 6. Error Handling

| Function | Error Condition | Error Message |
|----------|-----------------|---------------|
| `processPayment` | `amount <= 0` | `'Amount must be positive'` |
| `refundTransaction` | Transaction not found | `'Not implemented'` (from `getTransaction`) |
| `refundTransaction` | Transaction status ≠ `'completed'` | `'Can only refund completed transactions'` |

All errors are thrown as plain `Error` objects; catch them with `try/catch` in your application code.

---

## 7. Extending the Module

1. **Persist Transactions** – Replace the `getTransaction` and `getUserTransactions` stubs with real database queries (e.g., Prisma, TypeORM, MongoDB).  
2. **Integrate a Payment Provider** – Implement `chargePaymentMethod` and `processRefund` using Stripe, PayPal, or any other gateway SDK.  
3. **Add Logging / Metrics** – Wrap the async functions with logging or telemetry to trace payment flows.

---

## 8. Quick Reference

```ts
// Interfaces
interface PaymentMethod { ... }
interface Transaction { ... }

// Functions
async function processPayment(amount: number, method: PaymentMethod): Promise<Transaction>
async function refundTransaction(transactionId: string): Promise<Transaction>
async function getUserTransactions(userId: string): Promise<Transaction[]>
```

Happy coding! 🚀