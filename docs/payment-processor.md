# payment-processor.ts

*Auto-generated from `./payment-processor.ts`*

# payment‑processor.ts – API Documentation

## Overview
`payment-processor.ts` is a lightweight payment‑processing module that handles:

- **Creating** a payment transaction (`processPayment`)
- **Refunding** a completed transaction (`refundTransaction`)
- **Retrieving** all transactions for a specific user (`getUserTransactions`)

It exposes two data contracts (`PaymentMethod`, `Transaction`) and three async functions that return `Promise`s. The module is intentionally simple – it simulates external payment‑provider calls and database interactions, making it ideal for prototyping or unit‑testing.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `PaymentMethod` | `interface` | Describes a payment instrument. |
| `Transaction` | `interface` | Represents a payment transaction record. |
| `processPayment` | `function` | Creates a new transaction and attempts to charge the specified payment method. |
| `refundTransaction` | `function` | Refunds a completed transaction. |
| `getUserTransactions` | `function` | Retrieves all transactions belonging to a user. |

---

## Usage Examples

> **Tip:** All functions are `async`; use `await` or `.then()`.

### 1. `processPayment`

```ts
import { processPayment, PaymentMethod } from './payment-processor';

const card: PaymentMethod = {
  id: 'pm_123',
  type: 'card',
  last4: '4242',
  expiryDate: '12/2026',
};

async function charge() {
  try {
    const tx = await processPayment(5000, card); // $50.00
    console.log('Transaction:', tx);
  } catch (err) {
    console.error('Payment failed:', err.message);
  }
}
```

### 2. `refundTransaction`

```ts
import { refundTransaction } from './payment-processor';

async function refund() {
  try {
    const refundedTx = await refundTransaction('txn_1690000000_abc123');
    console.log('Refunded transaction:', refundedTx);
  } catch (err) {
    console.error('Refund error:', err.message);
  }
}
```

### 3. `getUserTransactions`

```ts
import { getUserTransactions } from './payment-processor';

async function listUserTxs() {
  const txs = await getUserTransactions('user_42');
  console.log(`User has ${txs.length} transactions`);
}
```

---

## Parameters

| Function | Parameter | Type | Description |
|----------|-----------|------|-------------|
| `processPayment` | `amount` | `number` | Amount to charge **in cents** (e.g., `5000` = $50.00). Must be > 0. |
| | `method` | `PaymentMethod` | The payment instrument to use. |
| `refundTransaction` | `transactionId` | `string` | Identifier of the transaction to refund. |
| `getUserTransactions` | `userId` | `string` | Identifier of the user whose transactions are requested. |

### `PaymentMethod` fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Unique identifier for the payment method. |
| `type` | `'card' | 'bank' | 'paypal'` | The method category. |
| `last4` | `string` | Last four digits of the card or account. |
| `expiryDate` | `string` (optional) | Expiry in `MM/YYYY` format (cards only). |

### `Transaction` fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | `string` | Unique transaction identifier. |
| `amount` | `number` | Amount in cents. |
| `currency` | `string` | ISO‑4217 currency code (currently always `'USD'`). |
| `status` | `'pending' | 'completed' | 'failed'` | Current state of the transaction. |
| `timestamp` | `Date` | When the transaction was created or last updated. |
| `paymentMethod` | `PaymentMethod` | The method used for this transaction. |

---

## Return Values

| Function | Return Type | Description |
|----------|-------------|-------------|
| `processPayment` | `Promise<Transaction>` | Resolves with the created transaction. `status` is `'completed'` on success, `'failed'` otherwise. |
| `refundTransaction` | `Promise<Transaction>` | Resolves with the updated transaction. The returned transaction has `status: 'failed'` to indicate it has been refunded. |
| `getUserTransactions` | `Promise<Transaction[]>` | Resolves with an array of all transactions for the given user. (Currently returns an empty array – replace with real DB logic.) |

---

## Error Handling

| Function | Condition | Error Message |
|----------|-----------|---------------|
| `processPayment` | `amount <= 0` | `'Amount must be positive'` |
| `refundTransaction` | `transaction.status !== 'completed'` | `'Can only refund completed transactions'` |
| `getTransaction` (internal) | Not implemented | `'Not implemented'` |

All errors are thrown as plain `Error` objects. Wrap calls in `try/catch` or use `.catch()` to handle them.

---

## Extending the Module

- **Persisting Transactions** – Replace the stubbed `getTransaction` and `getUserTransactions` with real database queries.
- **Real Payment Provider** – Swap out `chargePaymentMethod` and `processRefund` with SDK calls to Stripe, PayPal, etc.
- **Currency Support** – Add a `currency` parameter to `processPayment` and adjust the `Transaction` interface accordingly.

---

Happy coding! 🚀