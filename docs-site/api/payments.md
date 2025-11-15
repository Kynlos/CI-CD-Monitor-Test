---
title: Payments
layout: default
---

# payment-processor.ts

*Auto-generated from `./payment-processor.ts`*

# Payment‑Processor Module

The **payment‑processor** module is a lightweight, TypeScript‑friendly library that handles the core payment workflow for an application:

* **Create a payment transaction** (`processPayment`)
* **Refund a completed transaction** (`refundTransaction`)
* **Retrieve a user’s transaction history** (`getUserTransactions`)

All operations are asynchronous and return strongly‑typed objects that describe the transaction state. The module is intentionally minimal – it simulates external payment provider calls and uses in‑memory helpers – but it can be swapped out for a real persistence layer or payment gateway with little effort.

---

## 1. Overview

| Feature | What it does | Notes |
|---------|--------------|-------|
| `processPayment` | Charges a payment method and creates a `Transaction` record | Uses a 90 % success simulation; replace `chargePaymentMethod` with a real API call |
| `refundTransaction` | Reverses a completed transaction | Marks the transaction as `failed` to indicate a refund; you may want a separate `refunded` status |
| `getUserTransactions` | Returns all transactions for a user | Currently returns an empty array – implement a DB lookup |
| `PaymentMethod` | Describes a payment instrument | Supports card, bank, and PayPal |
| `Transaction` | Stores the result of a payment operation | Includes status, timestamp, and the used payment method |

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| `PaymentMethod` | **Interface** | Represents a payment instrument. |
| `Transaction` | **Interface** | Represents a payment transaction. |
| `processPayment` | **Function** | Creates a new transaction by charging a payment method. |
| `refundTransaction` | **Function** | Refunds a completed transaction. |
| `getUserTransactions` | **Function** | Retrieves all transactions for a user. |

> **Internal helpers** (not exported) – `generateTransactionId`, `chargePaymentMethod`, `getTransaction`, `processRefund`.

---

## 3. Usage Examples

> **Tip**: All functions return promises; use `await` or `.then()`.

### 3.1. Process a Payment

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
  expiryDate: '12/2026'
};

async function pay() {
  try {
    const tx: Transaction = await processPayment(5000, card); // $50.00
    console.log('Transaction:', tx);
  } catch (err) {
    console.error('Payment failed:', err);
  }
}
```

### 3.2. Refund a Transaction

```ts
import { refundTransaction } from './payment-processor';

async function refund() {
  try {
    const refundedTx = await refundTransaction('txn_123456');
    console.log('Refunded transaction:', refundedTx);
  } catch (err) {
    console.error('Refund error:', err);
  }
}
```

### 3.3. Get User Transactions

```ts
import { getUserTransactions } from './payment-processor';

async function listTransactions() {
  const txs = await getUserTransactions('user_42');
  console.log(`User has ${txs.length} transactions`);
}
```

---

## 4. Parameters

| Function | Parameter | Type | Description |
|----------|-----------|------|-------------|
| `processPayment` | `amount` | `number` | Amount to charge **in cents** (e.g., 5000 = $50.00). Must be > 0. |
| | `method` | `PaymentMethod` | The payment instrument to use. |
| `refundTransaction` | `transactionId` | `string` | The ID of the transaction to refund. |
| `getUserTransactions` | `userId` | `string` | The user’s unique identifier. |

**PaymentMethod**

| Property | Type | Description |
|----------|------|-------------|
| `id` | `string` | Unique identifier for the payment method. |
| `type` | `'card' | 'bank' | 'paypal'` | The method’s type. |
| `last4` | `string` | Last four digits of the card or account. |
| `expiry
