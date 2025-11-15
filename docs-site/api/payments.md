---
title: Payments
layout: default
---

# payment-processor.ts

*Auto-generated from `./payment-processor.ts`*

# Payment‑Processor Module API Documentation

## Overview
The **payment‑processor** module provides a lightweight abstraction for handling payment transactions in a TypeScript codebase. It exposes a set of interfaces and async functions that:

- Validate and process payments via a simulated payment provider.
- Record transaction metadata (ID, amount, currency, status, timestamp, and payment method).
- Allow refunds of completed transactions.
- Retrieve a user’s transaction history.

The module is intentionally minimal and uses in‑memory stubs for database access and external API calls, making it ideal for prototyping, unit testing, or as a foundation for a production‑ready payment system.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `PaymentMethod` | **interface** | Describes a payment instrument (card, bank, or PayPal). |
| `Transaction` | **interface** | Represents a payment transaction record. |
| `processPayment` | **async function** | Initiates a payment and returns a `Transaction`. |
| `refundTransaction` | **async function** | Refunds a completed transaction and returns the updated record. |
| `getUserTransactions` | **async function** | Retrieves all transactions belonging to a user. |

---

## Usage Examples

> **Note**: These examples assume the module is imported from `./payment-processor`.

```ts
import {
  PaymentMethod,
  Transaction,
  processPayment,
  refundTransaction,
  getUserTransactions
} from './payment-processor';

/* ---------- 1️⃣ Process a payment ---------- */
const card: PaymentMethod = {
  id: 'pm_123',
  type: 'card',
  last4: '4242',
  expiryDate: '12/24'
};

async function makePayment() {
  try {
    const tx: Transaction = await processPayment(5000, card); // $50.00
    console.log('Transaction:', tx);
  } catch (err) {
    console.error('Payment failed:', err);
  }
}
makePayment();

/* ---------- 2️⃣ Refund a transaction ---------- */
async function refund() {
  try {
    const refundedTx = await refundTransaction('txn_1690000000_abc123');
    console.log('Refunded transaction:', refundedTx);
  } catch (err) {
    console.error('Refund error:', err);
  }
}
refund();

/* ---------- 3️⃣ Get all user transactions ---------- */
async function listTransactions() {
  const userTxs = await getUserTransactions('user_456');
  console.log('User transactions:', userTxs);
}
listTransactions();
```

---

## Parameters

### `processPayment(amount: number, method: PaymentMethod)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `amount` | `number` | Amount to charge **in cents** (e.g., `5000` = $50.00). Must be > 0. |
| `method` | `PaymentMethod` | The payment instrument to use. |

### `refundTransaction(transactionId: string)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `transactionId` | `string` | The unique ID of the transaction to refund. |

### `getUserTransactions(userId: string)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `userId` | `string` | The identifier of the user whose transactions are requested. |

---

## Return Values

| Function | Return Type | Description |
|----------|-------------|-------------|
| `processPayment` | `Promise<Transaction>` | Resolves to a `Transaction` object. The `status` field will be `'completed'` on success or `'failed'` on failure. |
| `refundTransaction` | `Promise<Transaction>` | Resolves to the original transaction object with `status` set to `'failed'` (indicating a refund) and an updated `timestamp`. |
| `getUserTransactions` | `Promise<Transaction[]>` | Resolves to an array of `Transaction` objects belonging to the specified user. Currently returns an empty array (stub). |

---

## Error Handling

| Function | Possible Errors | When |
|----------|-----------------|------|
| `processPayment` | `Error('Amount must be positive')` | If `amount` ≤ 0. |
| `refundTransaction` | `Error('Can only refund completed transactions')` | If the transaction status is not `'completed'`. |
| `refundTransaction` | `Error('Not implemented')` | When `getTransaction` fails (currently unimplemented). |
| `getUserTransactions` | – | No errors currently; stub returns an empty array. |

---

## Interfaces

### `PaymentMethod`

```ts
interface PaymentMethod {
  id: string;          // Unique identifier for the payment instrument
  type: 'card' | 'bank' | 'paypal'; // Supported payment types
  last4: string;       // Last four digits of the card or account number
  expiryDate?: string; // Optional expiry date (e.g., "12/24")
}
```

### `Transaction`

```ts
interface Transaction {
  id: string;               // Unique transaction ID
  amount: number;           // Amount in cents
  currency: string;         // ISO currency code (currently hard‑coded to 'USD')
  status: 'pending' | 'completed' | 'failed'; // Current status
  timestamp: Date;          // When the transaction was created or updated
  paymentMethod: PaymentMethod; // The method used for the transaction
}
```

---

## Extending the Module

- **Persisting Transactions**: Replace the stubbed `getTransaction` and `getUserTransactions` with real database queries.
- **Real Payment Providers**: Swap out `chargePaymentMethod` and `processRefund` with SDK calls to Stripe, PayPal, etc.
- **Currency Support**: Add a `currency` parameter to `processPayment` and validate against supported codes.

---

### TL;DR

- **`processPayment`**: Charge a payment method → returns a `Transaction`.
- **`refundTransaction`**: Refund a completed transaction → returns the updated `Transaction`.
- **`getUserTransactions`**: Fetch all transactions for a user → returns an array of `Transaction`.

Use the provided interfaces to type your payment data, and handle the returned promises to build a robust checkout flow.
