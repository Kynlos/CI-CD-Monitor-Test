---
title: Notifications
layout: default
---

# email-service.ts

*Auto-generated from `./email-service.ts`*

# Email Service Module (`email-service.ts`)

## Overview
The **Email Service** module provides a simple, type‑safe API for sending single or bulk emails.  
- Validates recipients and email addresses.  
- Supports plain text, HTML, CC/BCC, and attachments.  
- Abstracts the underlying provider (e.g., SendGrid, Mailgun) behind `sendViaProvider`.  
- Returns a consistent `EmailResult` object indicating success or failure.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `EmailOptions` | **Interface** | Configuration object for an email. |
| `Attachment` | **Interface** | Represents a file attachment. |
| `EmailResult` | **Interface** | Result of an email send operation. |
| `sendEmail` | **Function** | Sends a single email. |
| `sendBulkEmails` | **Function** | Sends the same template to multiple recipients. |

---

## Usage Examples

### 1. Sending a single email

```ts
import { sendEmail, EmailOptions } from './email-service';

const options: EmailOptions = {
  to: ['alice@example.com'],
  subject: 'Welcome!',
  body: 'Hello Alice, welcome aboard.',
  html: '<p>Hello <strong>Alice</strong>, welcome aboard.</p>',
  cc: ['bob@example.com'],
  attachments: [
    {
      filename: 'welcome.pdf',
      content: Buffer.from('PDF content here', 'utf-8'),
      contentType: 'application/pdf',
    },
  ],
};

const result = await sendEmail(options);

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
  body: 'Hello, check out our latest updates!',
  html: '<h1>Monthly Newsletter</h1><p>Check out our latest updates!</p>',
};

const results = await sendBulkEmails(recipients, template);

results.forEach((res, idx) => {
  if (res.success) {
    console.log(`Email to ${recipients[idx]} sent! ID: ${res.messageId}`);
  } else {
    console.warn(`Failed to email ${recipients[idx]}: ${res.error}`);
  }
});
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
| `options.attachments` | `Attachment[]` | Optional file attachments. |

### `sendBulkEmails(recipients: string[], template: Omit<EmailOptions, 'to'>)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `recipients` | `string[]` | List of email addresses to send the template to. |
| `template` | `Omit<EmailOptions, 'to'>` | Email template excluding the `to` field. |

---

## Return Values

### `sendEmail`

Returns a `Promise<EmailResult>`:

| Property | Type | Description |
|----------|------|-------------|
| `success` | `boolean` | `true` if the email was sent successfully. |
| `messageId` | `string | undefined` | Unique identifier returned by the provider (only on success). |
| `error` | `string | undefined` | Error message if `success` is `false`. |

### `sendBulkEmails`

Returns a `Promise<EmailResult[]>` – an array of results, one per recipient, preserving order.

---

## Interface Definitions

```ts
/**
 * Email configuration.
 */
export interface EmailOptions {
  to: string[];            // Primary recipients
  subject: string;         // Subject line
  body: string;            // Plain‑text body
  html?: string;           // Optional HTML body
  cc?: string[];           // Optional CC recipients
  bcc?: string[];          // Optional BCC recipients
  attachments?: Attachment[]; // Optional attachments
}

/**
 * File attachment.
 */
export interface Attachment {
  filename: string;        // Name of the file
  content: Buffer | string; // File content
  contentType: string;     // MIME type
}

/**
 * Result of an email send operation.
 */
export interface EmailResult {
  success: boolean;        // True if sent
  messageId?: string;      // Provider message ID
  error?: string;          // Error message on failure
}
```

---

## Notes

- **Validation**: The module checks for at least one recipient and validates all email addresses using a simple regex.  
- **Provider abstraction**: `sendViaProvider` is a placeholder; replace it with real provider SDK logic.  
- **Error handling**: Errors are caught and returned in `EmailResult.error`.  
- **Bulk sending**: `sendBulkEmails` sends emails sequentially; for high‑volume use, consider parallelism or provider bulk APIs.  

Feel free to extend the module with additional features such as templating engines, retry logic, or integration with a queue system.
