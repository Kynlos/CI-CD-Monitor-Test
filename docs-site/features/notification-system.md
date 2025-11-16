---
title: Notification System
layout: default
---

# email-service.ts

*Auto-generated from `./email-service.ts`*

# Email Service Module (`email-service.ts`)

## Overview
The **Email Service** module provides a lightweight, type‑safe API for sending single or bulk emails. It validates recipients, supports plain‑text and HTML bodies, optional CC/BCC, and attachments. The module is intentionally provider‑agnostic – the actual sending logic is abstracted behind `sendViaProvider`, which can be swapped out for a real provider (SendGrid, Mailgun, SES, etc.) in production.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `EmailOptions` | **Interface** | Configuration for a single email. |
| `Attachment` | **Interface** | Represents an email attachment. |
| `EmailResult` | **Interface** | Result of an email send operation. |
| `sendEmail(options: EmailOptions)` | **Async Function** | Sends a single email. |
| `sendBulkEmails(recipients: string[], template: Omit<EmailOptions, 'to'>)` | **Async Function** | Sends the same template to many recipients. |

> **Note:** `isValidEmail` and `sendViaProvider` are internal helpers and not exported.

---

## Usage Examples

### 1. Sending a single email

```ts
import { sendEmail, EmailOptions } from './email-service';

const email: EmailOptions = {
  to: ['alice@example.com', 'bob@example.com'],
  subject: 'Welcome to Our Service',
  body: 'Hello, thanks for joining us!',
  html: '<p>Hello, <strong>thanks</strong> for joining us!</p>',
  cc: ['manager@example.com'],
  attachments: [
    {
      filename: 'terms.pdf',
      content: Buffer.from('PDF content here', 'utf-8'),
      contentType: 'application/pdf',
    },
  ],
};

const result = await sendEmail(email);

if (result.success) {
  console.log(`Email sent! Message ID: ${result.messageId}`);
} else {
  console.error(`Failed to send email: ${result.error}`);
}
```

### 2. Sending bulk emails

```ts
import { sendBulkEmails, EmailOptions } from './email-service';

const recipients = [
  'alice@example.com',
  'bob@example.com',
  'carol@example.com',
];

const template: Omit<EmailOptions, 'to'> = {
  subject: 'Monthly Newsletter',
  body: 'Here is our monthly newsletter.',
  html: '<h1>Monthly Newsletter</h1><p>Enjoy!</p>',
};

const results = await sendBulkEmails(recipients, template);

results.forEach((res, idx) => {
  if (res.success) {
    console.log(`Email ${idx + 1} sent: ${res.messageId}`);
  } else {
    console.warn(`Email ${idx + 1} failed: ${res.error}`);
  }
});
```

### 3. Handling errors

```ts
try {
  const result = await sendEmail({
    to: ['invalid-email'],
    subject: 'Test',
    body: 'Hello',
  });

  if (!result.success) {
    throw new Error(result.error);
  }
} catch (err) {
  console.error('Email send error:', err);
}
```

---

## Parameters

### `sendEmail(options: EmailOptions)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `options` | `EmailOptions` | Email configuration object. |
| `options.to` | `string[]` | **Required.** List of primary recipients. |
| `options.subject` | `string` | **Required.** Email subject line. |
| `options.body` | `string` | **Required.** Plain‑text body. |
| `options.html` | `string` | Optional HTML body. |
| `options.cc` | `string[]` | Optional CC recipients. |
| `options.bcc` | `string[]` | Optional BCC recipients. |
| `options.attachments` | `Attachment[]` | Optional list of attachments. |

### `sendBulkEmails(recipients: string[], template: Omit<EmailOptions, 'to'>)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `recipients` | `string[]` | Array of email addresses to send to. |
| `template` | `Omit<EmailOptions, 'to'>` | Email template excluding the `to` field; will be applied to each recipient. |

---

## Return Values

### `sendEmail`

Returns a `Promise<EmailResult>`:

| Property | Type | Description |
|----------|------|-------------|
| `success` | `boolean` | `true` if the email was queued/sent successfully. |
| `messageId` | `string | undefined` | Identifier returned by the provider (e.g., `msg_123456`). Only present on success. |
| `error` | `string | undefined` | Human‑readable error message on failure. |

### `sendBulkEmails`

Returns a `Promise<EmailResult[]>` – an array of results, one per recipient, preserving order.

---

## Internal Helpers (Not Exported)

| Function | Purpose |
|----------|---------|
| `isValidEmail(email: string): boolean` | Simple regex validation of email addresses. |
| `sendViaProvider(options: EmailOptions): Promise<string>` | Simulated provider call; returns a fake message ID. Replace with real API integration. |

---

## Extending / Customizing

- **Provider Integration**: Replace `sendViaProvider` with your provider SDK (SendGrid, SES, etc.). Ensure it returns a unique message ID string.
- **Validation**: Enhance `isValidEmail` with stricter checks or use a library like `validator.js`.
- **Error Handling**: Wrap `sendEmail` calls in try/catch if you prefer exceptions over `EmailResult.error`.

---

## Summary

The `email-service.ts` module offers a clean, typed API for sending emails, handling validation, attachments, and bulk dispatch. It returns structured results that make error handling straightforward, and it can be easily swapped for real provider logic.
