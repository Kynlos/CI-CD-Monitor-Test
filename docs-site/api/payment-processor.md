---
title: Payment Processor
layout: default
last_updated: 2025-11-16
---

# payment-processor.ts

*Auto-generated from `./payment-processor.ts`*

# Payment Processor Module (`payment-processor.ts`)

## Overview
The **Payment Processor** module is a lightweight, TypeScript‑based service that handles the lifecycle of payment transactions for e‑commerce or subscription platforms.

- Validates and processes payments via a simulated payment provider.  
- Supports refunds for completed transactions.  
- Provides a simple API for retrieving a user’s transaction history.  

> **NOTE** – The current implementation uses in‑memory stubs and random success rates. In a production environment you would replace the helper functions (`chargePaymentMethod`, `getTransaction`, `processRefund`) with real calls to a payment gateway and a persistent database.

### Feature Summary

| Feature                | What it does |
|------------------------|--------------|
| **PaymentMethod**      | A lightweight representation of a card, bank account, or PayPal account. |
| **Transaction**        | Immutable snapshot of a payment attempt, including status, amount, and the payment method used. |
| **processPayment**     | Validates the amount, creates a transaction record, and attempts to charge the payment method. |
| **refundTransaction**  | Looks up a completed transaction and issues a refund. |
| **getUserTransactions**| Returns all transactions for a given user (currently returns an empty array). |

## Exports

| Export               | Type      | Description                                                            |
|----------------------|-----------|------------------------------------------------------------------------|
| `PaymentMethod`      | Interface | Describes a payment instrument.                                        |
| `Transaction`        | Interface | Represents a payment transaction record.                               |
| `processPayment`     | Function  | Initiates a payment and returns the resulting `Transaction`.          |
| `refundTransaction`  | Function  | Refunds a completed transaction and returns the updated record.       |
| `getUserTransactions`| Function  | Retrieves all transactions belonging to a user.                        |

## Interfaces

### `PaymentMethod`
```ts
export interface PaymentMethod {
  /** Unique identifier for the method */
  id: string;
  /** Method type */
  type: 'card' | 'bank' | 'paypal';
  /** Last four digits of the card/account */
  last4: string;
  /** Optional expiry date (MM/YY) */
  expiryDate?: string;
}
```

### `Transaction`
```ts
export interface Transaction {
  /** Unique transaction identifier */
  id: string;
  /** Identifier of the user who made the payment */
  userId: string;
  /** Amount in the smallest currency unit (e.g., cents) */
  amount: number;
  /** Current status of the transaction */
  status: 'pending' | 'succeeded' | 'failed' | 'refunded';
  /** Payment method used for this transaction */
  paymentMethod: PaymentMethod;
  /** Timestamp when the transaction was created */
  createdAt: Date;
  /** Timestamp of the last update to the transaction */
  updatedAt: Date;
}
```

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

// 2️⃣ Process a payment of $49.99 (4999 cents)
async function makePurchase() {
  try {
    const tx: Transaction = await processPayment(4999, card);
    console.log('Transaction:', tx);
  } catch (err) {
    console.error('Payment failed:', err);
  }
}

// 3️⃣ Refund a transaction
async function refund(txId: string) {
  try {
    const refundedTx = await refundTransaction(txId);
    console.log('Refunded transaction:', refundedTx);
  } catch (err) {
    console.error('Refund failed:', err);
  }
}

// 4️⃣ Retrieve a user's transaction history
async function showHistory(userId: string) {
  const history = await getUserTransactions(userId);
  console.table(history);
}
```

--- 

*All operations are asynchronous and return plain JavaScript objects that can be persisted or sent over the network.*