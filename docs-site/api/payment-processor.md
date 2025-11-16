```markdown
---
title: Payment Processor
layout: default
last_updated: 2025-11-16
---

# payment-processor.ts

*Auto-generated from `./payment-processor.ts`*

# Payment Processor Module  
**File:** `payment-processor.ts`

---

## Overview  
The **Payment Processor** module provides a lightweight abstraction for handling payment transactions and refunds. It supports three payment‑method types (`card`, `bank`, `paypal`) and exposes a simple API to:

1. **Process a payment** – create a transaction, charge the payment method, and return the transaction status.  
2. **Refund a transaction** – reverse a completed transaction and mark it as refunded.  
3. **Retrieve a user’s transaction history** – fetch all transactions for a specific user.  

The module is intentionally minimal and uses in‑memory helpers to simulate database and external‑provider interactions. It can be dropped into any TypeScript project that needs a quick payment‑processing prototype or a test harness.

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

| Function               | Parameter      | Type            | Description                                                            |
|------------------------|----------------|-----------------|------------------------------------------------------------------------|
| `processPayment`       | `amount`       | `number`        | Amount to charge **in cents** (e.g., `5000` = $50.00). Must be > 0.    |
|                        | `method`       | `PaymentMethod` | The payment instrument to use.                                         |
| `refundTransaction`    | `transactionId`| `string`        | Identifier of the transaction to refund.                               |
| `getUserTransactions`  | `userId`       | `string`        | Identifier of the user whose transactions are requested.              |

### `PaymentMethod` fields

| Field       | Type                                 | Description                              |
|-------------|--------------------------------------|------------------------------------------|
| `id`        | `string`                             | Unique identifier for the payment method.|
| `type`      | `'card' \| 'bank' \| 'paypal'`       | Type of payment method.                  |
| `last4`     | `string`                             | Last four digits of the card/account.    |
| `expiryDate`| `string` (optional)                  | Expiry date in `MM/YY` format.           |

### `Transaction` fields

| Field       | Type                                 | Description                                          |
|-------------|--------------------------------------|------------------------------------------------------|
| `id`        | `string`                             | Unique transaction ID.                               |
| `amount`    | `number`                             | Amount in cents.                                     |
| `currency`  | `string`                             | ISO currency code (e.g., `'USD'`).                  |
| `status`    | `'pending' \| 'succeeded' \| 'failed' \| 'refunded'` | Current status of the transaction. |
| `methodId`  | `string`                             | ID of the `PaymentMethod` used.                      |
| `userId`    | `string`                             | Owner of the transaction.                            |
| `createdAt` | `Date`                               | When the transaction was created.                    |
| `updatedAt` | `Date`                               | Last update timestamp (e.g., after a refund).       |

--- 

*Generated on 2025‑11‑16.*
```