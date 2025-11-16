---
title: Payment System
layout: default
---

# payment-processor.ts

*Auto-generated from `./payment-processor.ts`*

# Payment‑Processor Module

## Overview
The **payment‑processor** module is a lightweight, TypeScript‑based library that simulates the core workflow of a payment system.  
It exposes:

- **Data contracts** (`PaymentMethod`, `Transaction`) that describe the shape of payment information and transaction records.
- **Business functions** (`processPayment`, `refundTransaction`, `getUserTransactions`) that orchestrate payment flow, refunding, and transaction retrieval.
- A handful of internal helpers that generate IDs, mock provider calls, and simulate database access.

> **Note** – The module is intentionally minimal and uses random success/failure to mimic a third‑party provider. In production you would replace the stubbed helpers with real API calls and persistence logic.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `PaymentMethod` | **Interface** | Describes a payment instrument. |
| `Transaction` | **Interface** | Represents a payment transaction record. |
| `processPayment` | **Function** | Initiates a payment and returns the resulting transaction. |
| `refundTransaction` | **Function** | Refunds a completed transaction and returns the updated record. |
| `getUserTransactions` | **Function** | Retrieves all transactions for a given user. |

---

## Usage Examples

### 1. Processing a Payment

```ts
import {
  processPayment,
  PaymentMethod,
  Transaction
} from './payment-processor';

const card: PaymentMethod = {
  id: 'pm_123',
  type: 'card',
  last4: '4242',
  expiryDate: '12/2025'
};

async function charge() {
  try {
    const tx: Transaction = await processPayment(5000, card); // $50.00
    console.log('Transaction:', tx);
  } catch (err) {
    console.error('Payment failed:', err);
  }
}

charge();
```

### 2. Refunding a Transaction

```ts
import { refundTransaction } from './payment-processor';

async function refund() {
  try {
    const refundedTx = await refundTransaction('txn_1690000000_abc123');
    console.log('Refunded transaction:', refundedTx);
  } catch (err) {
    console.error('Refund error:', err);
  }
}

refund();
```

### 3. Listing User Transactions

```ts
import { getUserTransactions } from './payment-processor';

async function list() {
  const txs = await getUserTransactions('user_42');
  console.log('User transactions:', txs);
}

list();
```

---

## Parameters

| Function | Parameter | Type | Description |
|----------|-----------|------|-------------|
| `processPayment` | `amount` | `number` | Amount to charge **in cents** (e.g., 5000 = $50.00). Must be > 0. |
| | `method` | `PaymentMethod` | The payment instrument to use. |
| `refundTransaction` | `transactionId` | `string` | The ID of the transaction to refund. |
| `getUserTransactions` | `userId` | `string` | The user’s unique identifier. |

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
| `currency` | `string` | ISO‑4217 code (currently always `'USD'`). |
| `status` | `'pending' | 'completed' | 'failed'` | Current state. |
| `timestamp` | `Date` | When the transaction was created or updated. |
| `paymentMethod` | `PaymentMethod` | The method used. |

---

## Return Values

| Function | Return Type | Description |
|----------|-------------|-------------|
| `processPayment` | `Promise<Transaction>` | Resolves to a `Transaction` object whose `status` is `'completed'` on success or `'failed'` on failure. |
| `refundTransaction` | `Promise<Transaction>` | Resolves to the original transaction object with `status` set to `'failed'` (used here to flag a refund) and an updated `timestamp`. |
| `getUserTransactions` | `Promise<Transaction[]>` | Resolves to an array of `Transaction` objects belonging to the specified user. Currently returns an empty array because the database layer is not implemented. |

---

## Error Handling

| Function | Error Condition | Message |
|----------|-----------------|---------|
| `processPayment` | `amount <= 0` | `"Amount must be positive"` |
| `refundTransaction` | Transaction not found | `"Not implemented"` (from `getTransaction`) |
| | Transaction status ≠ `'completed'` | `"Can only refund completed transactions"` |

All errors are thrown as plain `Error` instances. In a real system you might replace these with custom error classes.

---

## Extending the Module

1. **Persist Transactions** – Replace the stubbed `getTransaction`, `processRefund`, and `getUserTransactions` with real database queries.
2. **Real Payment Providers** – Swap out `chargePaymentMethod` with an SDK call to Stripe, PayPal, etc.
3. **Currency Support** – Add a `currency` parameter to `processPayment` and validate against supported codes.
4. **Status Enumeration** – Replace the string literals with a TypeScript `enum` for stricter typing.

---

## Summary

- **`PaymentMethod`** and **`Transaction`** define the data contracts.  
- **`processPayment`** validates the amount, creates a transaction, calls a mock provider, and updates the status.  
- **`refundTransaction`** ensures the transaction is completed before marking it as refunded.  
- **`getUserTransactions`** is a placeholder for future database integration.  

Use the examples above as a starting point and adapt the helper functions to your persistence and payment‑gateway stack.
