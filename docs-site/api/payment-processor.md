```markdown
---
title: Payment Processor
layout: default
last_updated: 2025-11-16
---

# payment-processor.ts

*Auto-generated from `./payment-processor.ts`*

# Payment Processor Module  

The **payment‑processor** module is a lightweight, self‑contained library that handles the core payment flow for an e‑commerce or subscription service.  
It provides a simple API to:

1. **Create a payment method representation** – a minimal object describing a card, bank account, or PayPal account.  
2. **Charge a payment method** – `processPayment` creates a transaction, attempts to charge the method, and returns the transaction status.  
3. **Refund a completed transaction** – `refundTransaction` reverses a successful transaction and marks it as refunded.  
4. **Retrieve a user’s transaction history** – `getUserTransactions` returns all transactions belonging to a given user.

All operations are asynchronous and return plain JavaScript objects that can be persisted or sent over the network.

> **NOTE** – The current implementation uses in‑memory stubs and random success rates. In a production environment you would replace the helper functions (`chargePaymentMethod`, `getTransaction`, `processRefund`) with real calls to a payment gateway and a database.

---

## Overview

| Feature | What it does |
|---------|--------------|
| **PaymentMethod** | A lightweight representation of a card, bank account, or PayPal account. |
| **Transaction** | Immutable snapshot of a payment attempt, including status, amount, and the payment method used. |
| **processPayment** | Validates the amount, creates a transaction record, and attempts to charge the payment method. |
| **refundTransaction** | Looks up a completed transaction and issues a refund. |
| **getUserTransactions** | Returns all transactions for a given user (currently returns an empty array). |

---

## Exports

| Export               | Type      | Description                                                            |
|----------------------|-----------|------------------------------------------------------------------------|
| `PaymentMethod`      | interface | Describes a payment instrument.                                        |
| `Transaction`        | interface | Represents a payment transaction record.                               |
| `processPayment`     | function  | Initiates a payment and returns a `Transaction`.                       |
| `refundTransaction`  | function  | Refunds a completed transaction and returns the updated record.       |
| `getUserTransactions`| function  | Retrieves all transactions belonging to a user.                        |

---

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
  /** Unique transaction ID */
  id: string;
  /** Amount in cents (e.g., 5000 = $50.00) */
  amount: number;
  /** ISO currency code – currently hard‑coded to 'USD' */
  currency: string;
  /** Current status of the transaction */
  status: 'pending' | 'succeeded' | 'failed' | 'refunded';
  /** Identifier of the payment method used */
  methodId: string;
  /** Identifier of the user who owns the transaction */
  userId: string;
  /** Timestamp when the transaction was created */
  createdAt: Date;
  /** Timestamp of the last update (e.g., after a refund) */
  updatedAt: Date;
}
```

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
  expiryDate: '12/27',
};

async function run() {
  const transaction = await processPayment({
    amount: 5000,          // $50.00
    currency: 'USD',
    methodId: card.id,
    userId: 'user_456',
  });

  console.log('Transaction result:', transaction);
}

run();
```

### 2. `refundTransaction`

```ts
import { refundTransaction } from './payment-processor';

async function refundDemo(transactionId: string) {
  const refunded = await refundTransaction(transactionId);
  console.log('Refunded transaction:', refunded);
}

// Example usage
refundDemo('tx_789');
```

### 3. `getUserTransactions`

```ts
import { getUserTransactions } from './payment-processor';

async function listUserTxns(userId: string) {
  const txns = await getUserTransactions(userId);
  console.log(`Transactions for ${userId}:`, txns);
}

// Example usage
listUserTxns('user_456');
```

--- 

*Generated documentation – keep in sync with `payment-processor.ts`.*