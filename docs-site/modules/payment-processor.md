---
title: Payment Processor
layout: default
---

_Last updated: 2025-11-16_

# payment-processor.ts

*Auto-generated from `./payment-processor.ts`*

# Payment Processor Module (`payment-processor.ts`)

## Overview
The **Payment Processor** module is a lightweight, TypeScript‑based service that handles the lifecycle of payment transactions.

- **Process payments** – validates and authorises a payment via a simulated provider.  
- **Refunds** – issues refunds for completed transactions.  
- **Transaction history** – simple API for retrieving a user’s transaction records.  

The implementation uses **in‑memory stubs** for persistence and external payment calls (`chargePaymentMethod`, `getTransaction`, `processRefund`). Replace these helpers with real integrations for production use.

---

## Exports

| Export               | Type        | Description                                                            |
|----------------------|-------------|------------------------------------------------------------------------|
| `PaymentMethod`      | Interface   | Describes a payment instrument (card, bank, PayPal).                  |
| `Transaction`        | Interface   | Represents a payment transaction record (status, amount, metadata). |
| `processPayment`    | Function    | Initiates a payment and returns the resulting `Transaction`.          |
| `refundTransaction` | Function    | Refunds a completed transaction and returns the updated `Transaction`.|
| `getUserTransactions`| Function   | Retrieves all transactions for a given user.                           |

---

## Usage Examples

> **Tip:** All functions return `Promise`s, so use `await` or `.then()`.

```ts
import {
  processPayment,
  refundTransaction,
  getUserTransactions,
  PaymentMethod,
  Transaction
} from './payment-processor';

// 1️⃣ Create a payment method (e.g., a card)
const card: PaymentMethod = {
  id: 'pm_12345',
  type: 'card',
  last4: '4242',
  expiryDate: '12/2026'
};
```

### 1️⃣ Process a Payment

```ts
async function makePurchase() {
  try {
    // Amount is in cents – $49.99 = 4999
    const tx: Transaction = await processPayment(4999, card);
    console.log('Transaction created:', tx);
  } catch (err) {
    console.error('Payment failed:', (err as Error).message);
  }
}
```

### 2️⃣ Refund a Transaction

```ts
async function refund(txId: string) {
  try {
    const refundedTx = await refundTransaction(txId);
    console.log('Refunded transaction:', refundedTx);
  } catch (err) {
    console.error('Refund error:', (err as Error).message);
  }
}
```

### 3️⃣ Retrieve a User’s Transactions

```ts
async function listUserTransactions(userId: string) {
  try {
    const userTxs = await getUserTransactions(userId);
    console.log(`User ${userId} has ${userTxs.length} transaction(s):`, userTxs);
  } catch (err) {
    console.error('Failed to fetch transactions:', (err as Error).message);
  }
}
```

---

## Parameters

### `processPayment(amount: number, method: PaymentMethod): Promise<Transaction>`

| Parameter | Type            | Description                                            |
|-----------|-----------------|--------------------------------------------------------|
| `amount`  | `number`        | Amount in **cents** (e.g., `4999` = $49.99).           |
| `method`  | `PaymentMethod` | Payment instrument to charge (card, bank, PayPal, …). |
| Returns   | `Promise<Transaction>` | Resolves with a `Transaction` object whose `status` is `'completed'` or `'failed'`. |

### `refundTransaction(transactionId: string): Promise<Transaction>`

| Parameter      | Type     | Description                                            |
|----------------|----------|--------------------------------------------------------|
| `transactionId`| `string` | Identifier of the transaction to refund.               |
| Returns        | `Promise<Transaction>` | Resolves with the updated `Transaction` (status `'refunded'`). |

### `getUserTransactions(userId: string): Promise<Transaction[]>`

| Parameter | Type     | Description                                            |
|-----------|----------|--------------------------------------------------------|
| `userId`  | `string` | Identifier of the user whose transactions are requested. |
| Returns   | `Promise<Transaction[]>` | Array of all `Transaction` records belonging to the user. |

---

## 5. Implementation Notes

- The module is **stateless** – all persistence is delegated to the stub helpers.  
- Replace the following helpers with real implementations for production:  
  - `chargePaymentMethod` – interacts with a payment gateway.  
  - `getTransaction` – fetches a transaction from a database.  
  - `processRefund` – calls the gateway’s refund endpoint.  

--- 

*Generated documentation – keep in sync with `payment-processor.ts` source.*