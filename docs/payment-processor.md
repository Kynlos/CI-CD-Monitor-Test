# payment-processor.ts

*Auto-generated from `./payment-processor.ts`*

# Payment Processor API Documentation

## Overview
The **Payment Processor** module is a lightweight, TypeScript‑friendly library that handles the core billing workflow for an e‑commerce or subscription service.  
It exposes:

- **Data models** (`PaymentMethod`, `Transaction`) that describe payment instruments and transaction records.
- **Core functions** to create, refund, and query transactions.
- A small set of internal helpers that simulate communication with a payment provider.

> **Note**: The current implementation uses in‑memory stubs and random success rates. Replace the stubbed helpers (`chargePaymentMethod`, `getTransaction`, `processRefund`) with real provider SDK calls for production use.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `PaymentMethod` | **Interface** | Describes a payment instrument (card, bank, PayPal). |
| `Transaction` | **Interface** | Represents a payment transaction record. |
| `processPayment` | **Function** | Creates and processes a payment. |
| `refundTransaction` | **Function** | Refunds a completed transaction. |
| `getUserTransactions` | **Function** | Retrieves all transactions for a user. |

---

## Usage Examples

> **Prerequisites** – Import the module and create a `PaymentMethod` instance.

```ts
import {
  PaymentMethod,
  processPayment,
  refundTransaction,
  getUserTransactions,
} from './payment-processor';

// Example payment method (card)
const card: PaymentMethod = {
  id: 'pm_123',
  type: 'card',
  last4: '4242',
  expiryDate: '12/2026',
};
```

### 1. Process a Payment

```ts
async function charge() {
  try {
    const tx = await processPayment(5000, card); // $50.00
    console.log('Transaction:', tx);
  } catch (err) {
    console.error('Payment failed:', err.message);
  }
}
```

### 2. Refund a Transaction

```ts
async function refund() {
  try {
    const refundedTx = await refundTransaction('txn_1699999999999_abc123xyz');
    console.log('Refunded transaction:', refundedTx);
  } catch (err) {
    console.error('Refund error:', err.message);
  }
}
```

### 3. Get All Transactions for a User

```ts
async function listUserTxs() {
  const txs = await getUserTransactions('user_456');
  console.log('User transactions:', txs);
}
```

---

## Function Signatures & Details

### `processPayment(amount: number, method: PaymentMethod) → Promise<Transaction>`

| Parameter | Type | Description |
|-----------|------|-------------|
| `amount` | `number` | Amount to charge **in cents** (e.g., `5000` = $50.00). |
| `method` | `PaymentMethod` | The payment instrument to use. |

| Return | Type | Description |
|--------|------|-------------|
| `Promise<Transaction>` | Resolves to a `Transaction` object. The `status` field will be `'completed'` on success or `'failed'` on failure. |

| Errors | Conditions |
|--------|------------|
| `Error('Amount must be positive')` | If `amount <= 0`. |

> **Behavior**  
> 1. Validates the amount.  
> 2. Creates a provisional `Transaction` with status `'pending'`.  
> 3. Calls `chargePaymentMethod` (stubbed to succeed 90% of the time).  
> 4. Updates the transaction status and returns it.

---

### `refundTransaction(transactionId: string) → Promise<Transaction>`

| Parameter | Type | Description |
|-----------|------|-------------|
| `transactionId` | `string` | The ID of the transaction to refund. |

| Return | Type | Description |
|--------|------|-------------|
| `Promise<Transaction>` | Resolves to the original transaction object with `status` set to `'failed'` (used here to indicate a refund). The `timestamp` is updated to the refund time. |

| Errors | Conditions |
|--------|------------|
| `Error('Can only refund completed transactions')` | If the transaction status is not `'completed'`. |
| `Error('Not implemented')` | Thrown by the stubbed `getTransaction` helper. |

> **Behavior**  
> 1. Retrieves the transaction via `getTransaction`.  
> 2. Ensures it is completed.  
> 3. Calls `processRefund` (stubbed).  
> 4. Returns an updated transaction object.

---

### `getUserTransactions(userId: string) → Promise<Transaction[]>`

| Parameter | Type | Description |
|-----------|------|-------------|
| `userId` | `string` | Identifier of the user whose transactions are requested. |

| Return | Type | Description |
|--------|------|-------------|
| `Promise<Transaction[]>` | Resolves to an array of `Transaction` objects. Currently returns an empty array; replace with a real DB query. |

> **Behavior**  
> Fetches all transactions belonging to the specified user. The function is a placeholder and should be wired to your persistence layer.

---

## Data Models

### `PaymentMethod`

| Property | Type | Description |
|----------|------|-------------|
| `id` | `string` | Unique identifier for the payment instrument. |
| `type` | `'card' | 'bank' | 'paypal'` | The kind of payment method. |
| `last4` | `string` | Last four digits of the card or account number. |
| `expiryDate?` | `string` | Optional expiry date in `MM/YYYY` format (cards only). |

### `Transaction`

| Property | Type | Description |
|----------|------|-------------|
| `id` | `string` | Unique transaction identifier. |
| `amount` | `number` | Amount in cents. |
| `currency` | `string` | ISO‑4217 currency code (currently hard‑coded to `'USD'`). |
| `status` | `'pending' | 'completed' | 'failed'` | Current state of the transaction. |
| `timestamp` | `Date` | When the transaction was created or last updated. |
| `paymentMethod` | `PaymentMethod` | The instrument used for the transaction. |

---

## Extending the Module

- **Persist Transactions** – Replace the stubbed `getTransaction` and `getUserTransactions` with real database calls (e.g., Prisma, TypeORM, MongoDB).  
- **Real Payment Provider** – Swap `chargePaymentMethod` and `processRefund` with SDK calls to Stripe, PayPal, Braintree, etc.  
- **Error Handling** – Wrap provider errors and map them to meaningful `Transaction` status codes or custom error classes.  
- **Currency Support** – Add a `currency` parameter to `processPayment` and store it in the transaction record.  

---

## Summary

This module gives you a quick, type‑safe way to:

- Create and process payments (`processPayment`).
- Refund completed transactions (`refundTransaction`).
- Retrieve a user’s transaction history (`getUserTransactions`).

Replace the stubbed helpers with real persistence and provider logic to move from a demo to a production‑ready payment system. Happy coding!