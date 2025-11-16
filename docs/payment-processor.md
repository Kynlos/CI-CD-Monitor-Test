# payment-processor.ts

*Auto-generated from `./payment-processor.ts`*

# payment‑processor.ts – API Documentation

## Overview

The **Payment Processing Module** is a lightweight, self‑contained TypeScript library that handles the lifecycle of a payment transaction.  
It exposes:

- **Data contracts** (`PaymentMethod`, `Transaction`) that describe the shape of payment methods and transaction records.
- **Core operations** for charging a payment method, refunding a completed transaction, and retrieving a user’s transaction history.
- **Utility helpers** for generating transaction IDs and simulating provider calls (the real implementation would call a payment gateway).

> ⚠️ **Note** – The current implementation uses in‑memory stubs and random success/failure logic. Replace the stubbed helpers (`chargePaymentMethod`, `getTransaction`, `processRefund`) with real provider integrations for production use.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `PaymentMethod` | **interface** | Describes a stored payment method. |
| `Transaction` | **interface** | Represents a payment transaction record. |
| `processPayment` | **function** | Charges a payment method and returns a `Transaction`. |
| `refundTransaction` | **function** | Refunds a completed transaction and returns the updated record. |
| `getUserTransactions` | **function** | Retrieves all transactions for a given user. |

---

## Usage Examples

> **Prerequisites** – Install the module (or copy the file) and import the functions:

```ts
import {
  PaymentMethod,
  Transaction,
  processPayment,
  refundTransaction,
  getUserTransactions
} from './payment-processor';
```

### 1. Charging a Payment Method

```ts
const card: PaymentMethod = {
  id: 'pm_123',
  type: 'card',
  last4: '4242',
  expiryDate: '12/2026'
};

async function charge() {
  try {
    const tx: Transaction = await processPayment(5000, card); // $50.00
    console.log('Transaction status:', tx.status);
  } catch (err) {
    console.error('Payment failed:', err.message);
  }
}
charge();
```

### 2. Refunding a Transaction

```ts
async function refund() {
  try {
    const refundedTx = await refundTransaction('txn_1699999999999_abc123');
    console.log('Refunded transaction status:', refundedTx.status);
  } catch (err) {
    console.error('Refund error:', err.message);
  }
}
refund();
```

### 3. Fetching a User’s Transaction History

```ts
async function listTransactions() {
  const userId = 'user_456';
  const txs = await getUserTransactions(userId);
  console.log(`Found ${txs.length} transactions for ${userId}`);
}
listTransactions();
```

---

## Parameters

| Function | Parameter | Type | Description |
|----------|-----------|------|-------------|
| `processPayment` | `amount` | `number` | Amount to charge **in cents** (e.g., `5000` = $50.00). |
| | `method` | `PaymentMethod` | The payment method to use for the charge. |
| `refundTransaction` | `transactionId` | `string` | The ID of the transaction to refund. |
| `getUserTransactions` | `userId` | `string` | The user’s unique identifier. |

---

## Return Values

| Function | Return Type | Description |
|----------|-------------|-------------|
| `processPayment` | `Promise<Transaction>` | Resolves to a `Transaction` object whose `status` is `'completed'` or `'failed'`. |
| `refundTransaction` | `Promise<Transaction>` | Resolves to the original transaction object with `status` set to `'failed'` (used to indicate a refunded state) and an updated `timestamp`. |
| `getUserTransactions` | `Promise<Transaction[]>` | Resolves to an array of `Transaction` objects belonging to the specified user. Currently returns an empty array – replace with a real DB query. |

---

## Data Contracts

### `PaymentMethod`

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | `string` | ✅ | Unique identifier for the payment method. |
| `type` | `'card' | 'bank' | 'paypal'` | ✅ | The method’s type. |
| `last4` | `string` | ✅ | Last four digits of the card or account number. |
| `expiryDate` | `string` | ❌ | Expiration date in `MM/YY` format (applicable to cards). |

### `Transaction`

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `id` | `string` | ✅ | Unique transaction identifier. |
| `amount` | `number` | ✅ | Amount in cents. |
| `currency` | `string` | ✅ | ISO‑4217 currency code (currently hard‑coded to `'USD'`). |
| `status` | `'pending' | 'completed' | 'failed'` | ✅ | Current state of the transaction. |
| `timestamp` | `Date` | ✅ | When the transaction was created or last updated. |
| `paymentMethod` | `PaymentMethod` | ✅ | The payment method used. |

---

## Extending the Module

1. **Persist Transactions** – Replace the stubbed `getTransaction` and `getUserTransactions` with real database queries (e.g., PostgreSQL, MongoDB).  
2. **Real Payment Provider** – Swap out `chargePaymentMethod` and `processRefund` with SDK calls to Stripe, PayPal, Braintree, etc.  
3. **Error Handling** – Wrap provider errors in custom error classes (`PaymentError`, `RefundError`) for richer context.  
4. **Unit Tests** – Add Jest or Vitest tests that mock the provider functions to verify business logic.

---

## Summary

- **`processPayment`**: Charge a payment method, returning a transaction record.  
- **`refundTransaction`**: Refund a completed transaction, marking it as failed.  
- **`getUserTransactions`**: Retrieve all transactions for a user.  

Use the provided interfaces to type your own payment method storage and transaction history. Replace the stubbed helpers with real integrations to move from a demo to a production‑ready payment system.