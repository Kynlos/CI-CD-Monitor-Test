# payment-processor.ts

*Auto-generated from `./payment-processor.ts`*

# Payment Processor Module (`payment-processor.ts`)

## Overview
The **Payment Processor** module is a lightweight, TypeScript‑based service that handles the lifecycle of payment transactions.  
- It validates and processes payments via a simulated payment provider.  
- Supports refunds for completed transactions.  
- Provides a simple API for retrieving a user’s transaction history.  

The module is intentionally minimal and uses in‑memory stubs for database access and external payment calls. Replace the stubbed helpers (`chargePaymentMethod`, `getTransaction`, `processRefund`) with real integrations for production use.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `PaymentMethod` | **Interface** | Describes a payment instrument (card, bank, PayPal). |
| `Transaction` | **Interface** | Represents a payment transaction record. |
| `processPayment` | **Function** | Initiates a payment and returns the resulting transaction. |
| `refundTransaction` | **Function** | Refunds a completed transaction and returns the updated record. |
| `getUserTransactions` | **Function** | Retrieves all transactions for a given user. |

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
    console.error('Refund error:', err);
  }
}

// 4️⃣ Get all transactions for a user
async function listUserTx(userId: string) {
  const txs = await getUserTransactions(userId);
  console.log(`Transactions for ${userId}:`, txs);
}
```

---

## Parameters

### `processPayment(amount: number, method: PaymentMethod): Promise<Transaction>`
| Parameter | Type | Description |
|-----------|------|-------------|
| `amount` | `number` | Amount to charge **in cents** (e.g., 4999 for $49.99). Must be > 0. |
| `method` | `PaymentMethod` | The payment instrument to use. |

### `refundTransaction(transactionId: string): Promise<Transaction>`
| Parameter | Type | Description |
|-----------|------|-------------|
| `transactionId` | `string` | The unique ID of the transaction to refund. |

### `getUserTransactions(userId: string): Promise<Transaction[]>`
| Parameter | Type | Description |
|-----------|------|-------------|
| `userId` | `string` | The identifier of the user whose transactions are requested. |

---

## Return Values

| Function | Return Type | Description |
|----------|-------------|-------------|
| `processPayment` | `Promise<Transaction>` | Resolves to a `Transaction` object. The `status` field will be `'completed'` on success or `'failed'` on failure. |
| `refundTransaction` | `Promise<Transaction>` | Resolves to the original transaction object with `status` set to `'failed'` (used here to indicate a refunded state) and an updated `timestamp`. |
| `getUserTransactions` | `Promise<Transaction[]>` | Resolves to an array of `Transaction` objects belonging to the specified user. Currently returns an empty array (stub). |

---

## Interface Definitions

```ts
/**
 * PaymentMethod
 * Represents a payment instrument.
 */
export interface PaymentMethod {
  /** Unique identifier for the payment method. */
  id: string;

  /** Type of payment instrument. */
  type: 'card' | 'bank' | 'paypal';

  /** Last four digits of the card or account number. */
  last4: string;

  /** Optional expiry date (MM/YY). */
  expiryDate?: string;
}

/**
 * Transaction
 * Represents a payment transaction record.
 */
export interface Transaction {
  /** Unique transaction identifier. */
  id: string;

  /** Amount in cents. */
  amount: number;

  /** Currency code (ISO 4217). */
  currency: string;

  /** Current status of the transaction. */
  status: 'pending' | 'completed' | 'failed';

  /** ISO‑8601 timestamp of the transaction. */
  timestamp: Date;

  /** Payment method used for the transaction. */
  paymentMethod: PaymentMethod;
}
```

---

## Error Handling

| Function | Possible Errors | When They Occur |
|----------|-----------------|-----------------|
| `processPayment` | `Error('Amount must be positive')` | If `amount` ≤ 0. |
| `refundTransaction` | `Error('Can only refund completed transactions')` | If the transaction status is not `'completed'`. |
| `refundTransaction` | `Error('Not implemented')` | From the stubbed `getTransaction` helper. |
| `getUserTransactions` | None (stub returns empty array). | – |

> **Note:** The helper `getTransaction` currently throws a “Not implemented” error. Replace it with a real database lookup before using `refundTransaction`.

---

## Extending the Module

1. **Persist Transactions** – Replace the stubbed `getTransaction` and `getUserTransactions` with real database queries (e.g., using Prisma, TypeORM, or a simple in‑memory store).  
2. **Real Payment Integration** – Swap `chargePaymentMethod` and `processRefund` with calls to Stripe, PayPal, or your preferred provider.  
3. **Status Enumeration** – Consider adding a dedicated `enum` for transaction status to avoid string literals.  
4. **Logging & Monitoring** – Add structured logging around payment attempts and failures.  

---

## Summary

- **`processPayment`**: Validates, creates, and attempts to charge a payment method.  
- **`refundTransaction`**: Refunds a completed transaction and marks it as refunded.  
- **`getUserTransactions`**: Retrieves all transactions for a user (currently a stub).  

Use these APIs as building blocks for a full‑fledged e‑commerce or subscription platform.