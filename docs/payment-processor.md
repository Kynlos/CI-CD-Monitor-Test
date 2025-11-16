# payment-processor.ts

*Auto-generated from `./payment-processor.ts`*

# Payment‑Processor Module

The **payment‑processor** module is a lightweight, TypeScript‑based library that handles the core payment flow for an e‑commerce or subscription service.  
It exposes a small set of public types and async functions that:

1. **Validate** and **charge** a payment method.  
2. **Refund** a completed transaction.  
3. **Retrieve** all transactions for a specific user.  

The implementation is intentionally simple – it simulates external payment provider calls and uses in‑memory helpers.  In a real application you would replace the stubbed helpers (`chargePaymentMethod`, `getTransaction`, `processRefund`) with calls to a database or a payment gateway SDK.

---

## 1. Overview

| Feature | What it does | Where it lives |
|---------|--------------|----------------|
| `processPayment` | Validates the amount, creates a transaction record, calls a simulated payment provider, and returns the transaction with a final status. | `processPayment()` |
| `refundTransaction` | Looks up a transaction, ensures it is completed, processes a refund, and returns an updated transaction marked as **failed** (used here to indicate a refunded state). | `refundTransaction()` |
| `getUserTransactions` | Fetches all transactions belonging to a user. (Stubbed to return an empty array.) | `getUserTransactions()` |
| `PaymentMethod` | Describes a payment instrument (card, bank, PayPal). | Interface |
| `Transaction` | Represents a payment record with status, timestamp, and the used payment method. | Interface |

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| `PaymentMethod` | `interface` | Defines the shape of a payment instrument. |
| `Transaction` | `interface` | Represents a payment transaction. |
| `processPayment` | `async function` | Processes a new payment. |
| `refundTransaction` | `async function` | Refunds a completed transaction. |
| `getUserTransactions` | `async function` | Retrieves all transactions for a user. |

---

## 3. Usage Examples

> **Tip**: All functions return `Promise`s, so use `await` or `.then()`.

### 3.1. Process a Payment

```ts
import { processPayment, PaymentMethod } from './payment-processor';

const card: PaymentMethod = {
  id: 'pm_123',
  type: 'card',
  last4: '4242',
  expiryDate: '12/24',
};

async function charge() {
  try {
    const transaction = await processPayment(5000, card); // $50.00
    console.log('Transaction:', transaction);
  } catch (err) {
    console.error('Payment failed:', err.message);
  }
}

charge();
```

### 3.2. Refund a Transaction

```ts
import { refundTransaction } from './payment-processor';

async function refund() {
  try {
    const refunded = await refundTransaction('txn_abcdef123');
    console.log('Refunded transaction:', refunded);
  } catch (err) {
    console.error('Refund error:', err.message);
  }
}

refund();
```

### 3.3. Get All Transactions for a User

```ts
import { getUserTransactions } from './payment-processor';

async function listTransactions() {
  const userId = 'user_456';
  const txns = await getUserTransactions(userId);
  console.log(`Transactions for ${userId}:`, txns);
}

listTransactions();
```

---

## 4. Parameters

### `processPayment(amount: number, method: PaymentMethod)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `amount` | `number` | Amount to charge **in cents** (e.g., `5000` = $50.00). Must be > 0. |
| `method` | `PaymentMethod` | The payment instrument to use. |

### `refundTransaction(transactionId: string)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `transactionId` | `string` | The ID of the transaction to refund. |

### `getUserTransactions(userId: string)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `userId` | `string` | The ID of the user whose transactions you want to retrieve. |

---

## 5. Return Values

| Function | Return Type | Description |
|----------|-------------|-------------|
| `processPayment` | `Promise<Transaction>` | A `Transaction` object with a status of **pending → completed** or **failed**. |
| `refundTransaction` | `Promise<Transaction>` | The original transaction object, but with `status` set to **failed** and a new `timestamp`. |
| `getUserTransactions` | `Promise<Transaction[]>` | An array of `Transaction` objects belonging to the user (currently empty). |

### `Transaction` Interface

```ts
interface Transaction {
  id: string;          // e.g., "txn_1690000000_abc123xyz"
  amount: number;      // cents
  currency: string;    // always "USD" in this stub
  status: 'pending' | 'completed' | 'failed';
  timestamp: