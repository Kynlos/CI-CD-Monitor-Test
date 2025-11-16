# payment-processor.ts

*Auto-generated from `./payment-processor.ts`*

# Payment Processor Module  
**File:** `payment-processor.ts`

---

## Overview  
The **Payment Processor** module provides a lightweight abstraction for handling payment transactions and refunds. It supports three payment method types (`card`, `bank`, `paypal`) and exposes a simple API to:

1. **Process a payment** – create a transaction, charge the payment method, and return the transaction status.  
2. **Refund a transaction** – reverse a completed transaction and mark it as refunded.  
3. **Retrieve a user’s transaction history** – fetch all transactions for a specific user.  

The module is intentionally minimal and uses in‑memory helpers to simulate database and external provider interactions. It can be dropped into any TypeScript project that needs a quick payment‑processing prototype or a test harness.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `PaymentMethod` | **interface** | Describes a payment instrument. |
| `Transaction` | **interface** | Represents a payment transaction record. |
| `processPayment` | **function** | Initiates a payment and returns a `Transaction`. |
| `refundTransaction` | **function** | Refunds a completed transaction and returns the updated record. |
| `getUserTransactions` | **function** | Retrieves all transactions belonging to a user. |

---

## Interfaces

### `PaymentMethod`
```ts
export interface PaymentMethod {
  id: string;                // Unique identifier for the method
  type: 'card' | 'bank' | 'paypal'; // Method type
  last4: string;             // Last four digits of the card/account
  expiryDate?: string;       // Optional expiry date (MM/YY)
}
```

### `Transaction`
```ts
export interface Transaction {
  id: string;                // Unique transaction ID
  amount: number;            // Amount in cents
  currency: string;          // ISO currency code (currently hard‑coded to 'USD')
  status: 'pending' | 'completed' | 'failed'; // Current status
  timestamp: Date;           // When the transaction was created/updated
  paymentMethod: PaymentMethod; // The method used
}
```

---

## Functions

### `processPayment(amount, method)`

```ts
export async function processPayment(
  amount: number,
  method: PaymentMethod
): Promise<Transaction>
```

#### Parameters
| Name | Type | Description |
|------|------|-------------|
| `amount` | `number` | Amount to charge **in cents** (e.g., 1999 for $19.99). Must be > 0. |
| `method` | `PaymentMethod` | The payment instrument to use. |

#### Return Value
| Type | Description |
|------|-------------|
| `Promise<Transaction>` | A promise that resolves to a `Transaction` object. The `status` will be `'completed'` on success or `'failed'` on failure. |

#### Example
```ts
import { processPayment, PaymentMethod } from './payment-processor';

const card: PaymentMethod = {
  id: 'pm_123',
  type: 'card',
  last4: '4242',
  expiryDate: '12/25'
};

const transaction = await processPayment(4999, card);
console.log(transaction.status); // 'completed' or 'failed'
```

---

### `refundTransaction(transactionId)`

```ts
export async function refundTransaction(
  transactionId: string
): Promise<Transaction>
```

#### Parameters
| Name | Type | Description |
|------|------|-------------|
| `transactionId` | `string` | The ID of the transaction to refund. |

#### Return Value
| Type | Description |
|------|-------------|
| `Promise<Transaction>` | The original transaction object, but with `status` set to `'failed'` (used to indicate a refunded transaction) and `timestamp` updated to the refund time. |

#### Example
```ts
import { refundTransaction } from './payment-processor';

try {
  const refunded = await refundTransaction('txn_123456');
  console.log(refunded.status); // 'failed'
} catch (err) {
  console.error(err.message); // e.g., "Can only refund completed transactions"
}
```

---

### `getUserTransactions(userId)`

```ts
export async function getUserTransactions(
  userId: string
): Promise<Transaction[]>
```

#### Parameters
| Name | Type | Description |
|------|------|-------------|
| `userId` | `string` | The user’s unique identifier. |

#### Return Value
| Type | Description |
|------|-------------|
| `Promise<Transaction[]>` | An array of `Transaction` objects belonging to the user. Currently returns an empty array (placeholder for real DB logic). |

#### Example
```ts
import { getUserTransactions } from './payment-processor';

const history = await getUserTransactions('user_42');
console.log(history.length); // 0 (placeholder)
```

---

## Helper Functions (internal)

| Function | Purpose |
|----------|---------|
| `generateTransactionId()` | Creates a pseudo‑unique transaction ID. |
| `chargePaymentMethod(method, amount)` | Simulates an external payment provider call; 90 % success rate. |
| `getTransaction(id)` | Placeholder for DB lookup – throws “Not implemented”. |
| `processRefund(transaction)` | Placeholder for refund logic. |

> **Note:** The helper functions are intentionally simple and should be replaced with real database and payment‑gateway integrations in production.

---

## Quick Start

```ts
import {
  processPayment,
  refundTransaction,
  getUserTransactions,
  PaymentMethod
} from './payment-processor';

async function demo() {
  const method: PaymentMethod = {
    id: 'pm_001',
    type: 'card',
    last4: '1111',
    expiryDate: '01/30'
  };

  // 1. Process a payment
  const tx = await processPayment(2500, method);
  console.log('Transaction:', tx);

  // 2. Refund if needed
  if (tx.status === 'completed') {
    const refunded = await refundTransaction(tx.id);
    console.log('Refunded:', refunded);
  }

  // 3. Fetch user history
  const history = await getUserTransactions('user_123');
  console.log('History:', history);
}

demo().catch(console.error);
```

---

## Error Handling

- `processPayment` throws `Error('Amount must be positive')` if the amount is ≤ 0.  
- `refundTransaction` throws `Error('Can only refund completed transactions')` if the transaction is not in the `completed` state.  
- `getTransaction` (used internally) currently throws `Error('Not implemented')`; replace with real DB logic.

---

## Extending the Module

| Feature | Suggested Change |
|---------|------------------|
| Persist transactions | Replace `getTransaction` and `getUserTransactions` with real DB queries. |
| Support more currencies | Add `currency` parameter to `processPayment` and validate against a whitelist. |
| Real payment gateway | Swap `chargePaymentMethod` and `processRefund` with SDK calls to Stripe, PayPal, etc. |
| Logging & metrics | Add instrumentation around each helper to track success/failure rates. |

---

**Happy coding!**