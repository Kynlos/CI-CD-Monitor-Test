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

The **Payment Processor** module provides a lightweight abstraction for handling payment transactions and refunds. It supports three payment‑method types (`card`, `bank`, `paypal`) and exposes a simple API to:

1. **Process a payment** – create a transaction, charge the payment method, and return the transaction status.  
2. **Refund a transaction** – reverse a completed transaction and mark it as refunded.  
3. **Retrieve a user’s transaction history** – fetch all transactions for a specific user.  

All operations are asynchronous and return plain JavaScript objects that can be persisted or sent over the network. The implementation is intentionally minimal and uses in‑memory helpers to simulate database and external provider interactions. It is ideal for quick prototypes, test harnesses, or as a starting point before integrating real payment‑gateway SDKs.

> ⚠️ **Note** – The current implementation uses random success/failure logic and in‑memory storage. Replace the stubbed helpers (`chargePaymentMethod`, `getTransaction`, `processRefund`) with real provider integrations for production use.

### Feature Summary

| Feature               | What it does |
|-----------------------|--------------|
| **PaymentMethod**     | A lightweight representation of a card, bank account, or PayPal account. |
| **Transaction**       | Immutable snapshot of a payment attempt, including status, amount, and the payment method used. |
| **processPayment**    | Validates the amount, creates a transaction record, and attempts to charge the payment method. |
| **refundTransaction** | Looks up a completed transaction and issues a refund. |
| **getUserTransactions**| Returns all transactions for a given user (currently returns an empty array). |

---

## Exports  

| Export               | Type        | Description |
|----------------------|-------------|-------------|
| `PaymentMethod`      | **interface** | Describes a payment instrument. |
| `Transaction`        | **interface** | Represents a payment transaction record. |
| `processPayment`     | **function** | Charges a payment method and returns a `Transaction`. |
| `refundTransaction`  | **function** | Refunds a completed transaction and returns the updated `Transaction`. |
| `getUserTransactions`| **function** | Retrieves all transactions belonging to a user. |

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
  getUserTransactions,
} from './payment-processor';

// 1️⃣ Create a payment method representation
const myCard: PaymentMethod = {
  id: 'pm_001',
  type: 'card',
  last4: '4242',
  expiryDate: '12/27',
};

// 2️⃣ Process a payment
async function makePurchase() {
  try {
    const tx: Transaction = await processPayment({
      amount: 1999,          // $19.99 in cents
      currency: 'USD',
      paymentMethod: myCard,
      userId: 'user_123',
    });

    console.log('Transaction result:', tx);
  } catch (err) {
    console.error('Payment failed:', err);
  }
}

// 3️⃣ Refund a transaction
async function refundPurchase(transactionId: string) {
  try {
    const refundedTx = await refundTransaction(transactionId);
    console.log('Refunded transaction:', refundedTx);
  } catch (err) {
    console.error('Refund failed:', err);
  }
}

// 4️⃣ Get a user's transaction history
async function showHistory(userId: string) {
  const history = await getUserTransactions(userId);
  console.log(`Transaction history for ${userId}:`, history);
}

// Example flow
(async () => {
  await makePurchase();
  // Assume the transaction ID is known after the purchase
  // await refundPurchase('tx_abc123');
  await showHistory('user_123');
})();
```

The example demonstrates the full lifecycle:

1. Define a `PaymentMethod`.
2. Call `processPayment` to create and charge a transaction.
3. Optionally call `refundTransaction` with the transaction ID.
4. Retrieve all of a user’s transactions via `getUserTransactions`.

> **Tip** – Because the current implementation stores data only in memory, the transaction history will be lost when the process exits. Swap the in‑memory helpers with persistent storage (e.g., a database) for real‑world usage.