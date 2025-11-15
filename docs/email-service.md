# email-service.ts

*Auto-generated from `./email-service.ts`*

# Email Service Module (`email-service.ts`)

## Overview
The **Email Service** module provides a lightweight, type‑safe API for sending single or bulk emails from a Node.js/TypeScript application.  
- Validates recipient addresses.  
- Supports plain‑text and HTML bodies.  
- Handles optional CC/BCC and attachments.  
- Returns a clear success/error result for each send operation.  
- The actual transport is abstracted behind `sendViaProvider`, making it trivial to swap out SendGrid, Mailgun, SES, etc.

> **Note**: The current implementation simulates a provider and always returns a message ID. Replace `sendViaProvider` with a real provider SDK for production use.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `EmailOptions` | Interface | Configuration object for a single email. |
| `Attachment` | Interface | Represents an email attachment. |
| `EmailResult` | Interface | Result of an email send operation. |
| `sendEmail` | Function | Sends a single email. |
| `sendBulkEmails` | Function | Sends the same template to multiple recipients. |

---

## Usage Examples

### 1. Sending a Single Email

```ts
import { sendEmail, EmailOptions } from './email-service';

const email: EmailOptions = {
  to: ['alice@example.com'],
  subject: 'Welcome!',
  body: 'Hello Alice, welcome to our platform.',
  html: '<p>Hello <strong>Alice</strong>, welcome to our platform.</p>',
  cc: ['bob@example.com'],
  attachments: [
    {
      filename: 'terms.pdf',
      content: Buffer.from('PDF content here', 'utf-8'),
      contentType: 'application/pdf',
    },
  ],
};

async function main() {
  const result = await sendEmail(email);
  if (result.success) {
    console.log(`Email sent, messageId: ${result.messageId}`);
  } else {
    console.error(`Failed to send email: ${result.error}`);
  }
}

main();
```

### 2. Sending Bulk Emails

```ts
import { sendBulkEmails, EmailOptions } from './email-service';

const recipients = [
  'alice@example.com',
  'bob@example.com',
  'carol@example.com',
];

const template: Omit<EmailOptions, 'to'> = {
  subject: 'Monthly Newsletter',
  body: 'Hello, here is our monthly newsletter.',
  html: '<h1>Monthly Newsletter</h1><p>Enjoy!</p>',
};

async function main() {
  const results = await sendBulkEmails(recipients, template);
  results.forEach((res, idx) => {
    if (res.success) {
      console.log(`✅ Sent to ${recipients[idx]} (msgId: ${res.messageId})`);
    } else {
      console.warn(`❌ Failed to send to ${recipients[idx]}: ${res.error}`);
    }
  });
}

main();
```

### 3. Handling Errors

```ts
import { sendEmail } from './email-service';

async function main() {
  const result = await sendEmail({
    to: ['invalid-email'],
    subject: 'Test',
    body: 'This will fail',
  });

  if (!result.success) {
    // Graceful fallback or retry logic
    console.error('Email failed:', result.error);
  }
}
```

---

## Parameters

### `sendEmail(options: EmailOptions)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `options` | `EmailOptions` | Email configuration object. |
| `options.to` | `string[]` | **Required**. List of primary recipients. |
| `options.subject` | `string` | **Required**. Email subject line. |
| `options.body` | `string` | **Required**. Plain‑text body. |
| `options.html` | `string` | Optional. HTML body. |
| `options.cc` | `string[]` | Optional. Carbon‑copy recipients. |
| `options.bcc` | `string[]` | Optional. Blind‑carbon‑copy recipients. |
| `options.attachments` | `Attachment[]` | Optional. List of attachments. |

### `sendBulkEmails(recipients: string[], template: Omit<EmailOptions, 'to'>)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `recipients` | `string[]` | Array of email addresses to send to. |
| `template` | `Omit<EmailOptions, 'to'>` | Email template that will be applied to each recipient. All fields except `to` are reused. |

---

## Return Values

### `sendEmail`

| Property | Type | Description |
|----------|------|-------------|
| `success` | `boolean` | `true` if the email was sent successfully. |
| `messageId` | `string` | **Present when `success` is `true`**. Identifier returned by the provider. |
| `error` | `string` | **Present when `success` is `false`**. Human‑readable error message. |

### `sendBulkEmails`

Returns an array of `EmailResult` objects, one per recipient, preserving the order of the input `recipients` array.

---

## Internal Helpers (Not Exported)

| Function | Purpose |
|----------|---------|
| `isValidEmail(email: string): boolean` | Simple regex check for RFC‑5322 compliant email addresses. |
| `sendViaProvider(options: EmailOptions): Promise<string>` | Simulates sending an email and returns a fake message ID. Replace with real provider logic. |

---

## Extending / Customizing

| Feature | How to Extend |
|---------|---------------|
| **Real Provider** | Replace `sendViaProvider` with an SDK call (SendGrid, SES, etc.). |
| **Advanced Validation** | Override `isValidEmail` or add additional checks before calling `sendEmail`. |
| **Concurrency** | `sendBulkEmails` currently sends sequentially. For high‑volume scenarios, consider `Promise.all` or a concurrency limiter. |
| **Logging** | Add instrumentation inside `sendEmail` or `sendBulkEmails` to log message IDs or errors. |
| **Retry Logic** | Wrap `sendEmail` in a retry helper that retries on transient errors. |

---

## Quick Reference

```ts
// Types
interface EmailOptions { ... }
interface Attachment { ... }
interface EmailResult { ... }

// Functions
async function sendEmail(options: EmailOptions): Promise<EmailResult>
async function sendBulkEmails(
  recipients: string[],
