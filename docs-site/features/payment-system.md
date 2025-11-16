```markdown
---
title: Payment System
layout: default
---

# payment-processor.ts

*Auto-generated from `./payment-processor.ts`*

**Last updated:** 2025-11-16  

---

## Overview  

The **Payment Processor** module provides a lightweight abstraction for handling payment transactions and refunds. It supports three payment method types (`card`, `bank`, `paypal`) and exposes a simple API to:

1. **Process a payment** – create a transaction, charge the payment method, and return the transaction status.  
2. **Refund a transaction** – reverse a completed transaction and mark it as refunded.  
3. **Retrieve a user’s transaction history** – fetch all transactions for a specific user.  

The implementation is intentionally minimal and uses in‑memory helpers to simulate database and external provider interactions. It is ideal for quick prototypes, test harnesses, or as a starting point before integrating real payment‑gateway SDKs.

> ⚠️ **Note** – The current implementation uses random success/failure logic and in‑memory storage. Replace the stubbed helpers (`chargePaymentMethod`, `getTransaction`, `processRefund`) with real provider integrations for production use.

---

## Exports  

| Export               | Type        | Description                                            |
|----------------------|-------------|--------------------------------------------------------|
| `PaymentMethod`      | **interface** | Describes a payment instrument.                        |
| `Transaction`        | **interface** | Represents a payment transaction record.               |
| `processPayment`     | **function** | Initiates a payment and returns a `Transaction`.       |
| `refundTransaction`  | **function** | Refunds a completed transaction and returns the updated record. |
| `getUserTransactions`| **function** | Retrieves all transactions belonging to a user.        |

---

## Interfaces  

### `PaymentMethod`

```ts
export interface PaymentMethod {
  id: string;                         // Unique identifier for the method
  type: 'card' | 'bank' | 'paypal';    // Method type
  last4: string;                      // Last four digits of the card/account
  expiryDate?: string;                // Optional expiry date (MM/YY)
}
```

### `Transaction`

```ts
export interface Transaction {
  id: string;                         // Unique transaction ID
  amount: number;                     // Amount in cents
  currency: string;                   // ISO currency code (currently hard‑coded to 'USD')
  status: 'pending' |
          'succeeded' |
          'failed' |
          'refunded';                // Current state of the transaction
  createdAt: Date;                    // Timestamp when the transaction was created
  // Additional fields can be added as needed (e.g., userId, paymentMethodId)
}
```

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

| Function            | Parameter   | Type            | Description                                            |
|---------------------|-------------|-----------------|--------------------------------------------------------|
| `processPayment`    | `amount`    | `number`        | Amount to charge **in cents** (e.g., `5000` = $50.00). |
|                     | `method`    | `PaymentMethod` | The payment method to use for the charge.             |
| `refundTransaction` | `transactionId` | `string`   | Identifier of the transaction to be refunded.          |
| `getUserTransactions`| `userId`   | `string`        | Identifier of the user whose transactions are requested.|

```