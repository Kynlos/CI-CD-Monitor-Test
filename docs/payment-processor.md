# payment-processor.ts

*Auto-generated from `./payment-processor.ts`*

# Payment‑Processor Module

The **payment‑processor** module is a lightweight, self‑contained library that handles the core payment flow for an e‑commerce or subscription service.  
It exposes a small API that lets you:

- Create a payment method representation
- Charge a payment method (`processPayment`)
- Refund a completed transaction (`refundTransaction`)
- Retrieve a user’s transaction history (`getUserTransactions`)

All operations are asynchronous and return plain JavaScript objects that can be persisted or sent over the network.

> **NOTE** – The current implementation uses in‑memory stubs and random success rates. In a production environment you would replace the helper functions (`chargePaymentMethod`, `getTransaction`, `processRefund`) with real calls to a payment gateway and a database.

---

## 1. Overview

| Feature | What it does |
|---------|--------------|
| **PaymentMethod** | A lightweight representation of a card, bank account, or PayPal account. |
| **Transaction** | Immutable snapshot of a payment attempt, including status, amount, and the payment method used. |
| **processPayment** | Validates the amount, creates a transaction record, and attempts to charge the payment method. |
| **refundTransaction** | Looks up a completed transaction and issues a refund. |
| **getUserTransactions** | Returns all transactions for a given user (currently returns an empty array). |

---

## 2. Exports

| Export | Type | Description |
|--------|------|-------------|
| `PaymentMethod` | `interface` | Describes a payment method. |
| `Transaction` | `interface` | Describes a payment transaction. |
| `processPayment` | `function` | Charges a payment method and returns a `Transaction`. |
| `refundTransaction` | `function` | Refunds a completed transaction and returns the updated `Transaction`. |
| `getUserTransactions` | `function` | Retrieves all transactions for a user. |

---

## 3. Usage Examples

> **Tip** – All functions return promises; use `await` or `.then()`.

### 3.1. Create a payment method

```ts
import { PaymentMethod } from './payment-processor';

const card: PaymentMethod = {
  id: 'pm_123456',
  type: 'card',
  last4: '4242',
  expiryDate: '12/2026',
};
```

### 3.2. Process a payment

```ts
import { processPayment, PaymentMethod } from './payment-processor';

const card: PaymentMethod = {
  id: 'pm_123456',
  type: 'card',
  last4: '4242',
  expiryDate: '12/2026',
};

async function charge() {
  try {
    const transaction = await processPayment(5000, card); // $50.00
    console.log('Transaction:', transaction);
  } catch (err) {
    console.error('Payment failed:', err.message);
  }
}
```

### 3.3. Refund a transaction

```ts
import { refundTransaction } from './payment-processor';

async function refund() {
  try {
    const refunded = await refundTransaction('txn_1699999999999_abc123');
    console.log('Refunded transaction:', refunded);
  } catch (err) {
    console.error('Refund error:', err.message);
  }
}
```

### 3.4. Get a user’s transaction history

```ts
import { getUserTransactions } from './payment-processor';

async function listTransactions() {
  const txns = await getUserTransactions('user_42');
  console.log('User transactions:', txns);
}
```

---

## 4. Parameters

| Function | Parameter | Type | Description |
|----------|-----------|------|-------------|
| `processPayment` | `amount` | `number` | Amount to charge **in cents** (e.g., 5000 = $50.00). Must be > 0. |
| | `method` | `PaymentMethod` | The payment method to charge. |
| `refundTransaction` | `transactionId` | `string` | The ID of the transaction you wish to refund. |
| `getUserTransactions` | `userId` | `string` | The user’s unique identifier. |

---

## 5. Return Values

| Function | Return Type | Description |
|----------|-------------|-------------|
| `processPayment` | `Promise<Transaction>` | Resolves to a `Transaction` object. The `status` will be `'completed'` on success or `'failed'` on failure. |
| `refundTransaction` | `Promise<Transaction>` | Resolves to the original transaction object with `status` set to `'failed'` (used here to indicate a refund). The `timestamp` is updated to the refund time. |
| `getUserTransactions` | `Promise<Transaction[]>` | Resolves to an array of `Transaction` objects. Currently returns an empty array; replace the stub with a real query. |

---

## 6. Type Definitions

```ts
/**
 * PaymentMethod
 * @property id - Unique identifier for the payment method
 * @property type - One of 'card', 'bank', or 'paypal'
 * @property last4 - Last four digits of the card or account number
 * @property expiryDate - Optional expiry date (MM/YYYY) for cards
 */
export interface PaymentMethod {
  id: string;
  type: 'card' | 'bank' | 'paypal';
  last4: string;
  expiryDate?: string;
}

/**
 * Transaction
 * @property id - Unique transaction identifier
 * @property amount - Amount in cents
 * @property currency - ISO currency code (default: 'USD')
 * @property status - Current status: 'pending', 'completed', or 'failed'
 * @property timestamp - Date/time of the transaction
 * @property paymentMethod - The payment method used
 */
export interface Transaction {
  id: string;
  amount: number;
  currency: string;
  status: 'pending' | 'completed' | 'failed';
  timestamp: Date;
  paymentMethod: PaymentMethod;
}
```

---

## 7. Error Handling

- `processPayment` throws `Error('Amount must be positive')` if the amount is ≤ 0.
- `refundTransaction` throws `Error('Can only refund completed transactions')` if the transaction is not in the `completed` state.
- `getTransaction` (used internally) currently throws `Error('Not implemented')`; replace with a real DB lookup.
- All helper functions (`chargePaymentMethod`, `processRefund`) are stubs and should be replaced with real gateway logic.

---

## 8. Extending the Module

| Area | Suggested Improvement |
|------|-----------------------|
| **Persistence** | Replace the in‑memory stubs with a real database (e.g., PostgreSQL, MongoDB). |
| **Gateway Integration** | Swap `chargePaymentMethod` and `processRefund` for SDK calls to Stripe, PayPal, or Braintree. |
| **Idempotency** | Add an idempotency key to `processPayment` to avoid double charges. |
| **Currency Support** | Allow `currency` to be passed in or derived from the user’s locale. |
| **Logging** | Add structured logging for audit trails. |
| **Unit Tests** | Write tests that mock the gateway and database layers. |

---

## 9. Importing the Module

```ts
import {
  PaymentMethod,
  Transaction,
  processPayment,
  refundTransaction,
  getUserTransactions,
} from './payment-processor';
```

---

### Quick Reference

| Export | Usage |
|--------|-------|
