```markdown
---
title: Email Service
layout: default
---

_Last updated: 2025-11-16_

# email-service.ts

*Auto‑generated from `./email-service.ts`*

# Email Service Module (`email-service.ts`)

## Overview
The **Email Service** module provides a lightweight, type‑safe API for sending single or bulk emails.  

- Validates recipients and email addresses.  
- Supports plain‑text, HTML, CC/BCC, and attachments.  
- Abstracts the underlying provider (e.g., SendGrid, Mailgun, SES) behind a `sendViaProvider` stub that simulates an external provider. Replace this stub with real provider logic in production.  
- Returns a consistent `EmailResult` object indicating success or failure.

---

## Exports

| Export          | Type      | Description                                   |
|-----------------|-----------|-----------------------------------------------|
| `EmailOptions`  | Interface | Configuration object for a single email.      |
| `Attachment`    | Interface | Represents a file attachment.                |
| `EmailResult`   | Interface | Result of an email send operation.           |
| `sendEmail`     | Function  | Sends a single email.                         |
| `sendBulkEmails`| Function  | Sends the same template to many recipients.   |

---

## Usage Examples

### 1. Sending a single email

```ts
import { sendEmail, EmailOptions } from './email-service';

const email: EmailOptions = {
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

const result = await sendEmail(email);

if (result.success) {
  console.log(`Email sent, messageId: ${result.messageId}`);
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
  html: '<h1>Monthly Newsletter</h1><p>Here is our monthly newsletter.</p>',
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
| `options.body` | `string` | **Required.** Plain‑text body of the email. |
| `options.html` | `string` (optional) | HTML version of the email body. |
| `options.cc` | `string[]` (optional) | List of CC recipients. |
| `options.bcc` | `string[]` (optional) | List of BCC recipients. |
| `options.attachments` | `Attachment[]` (optional) | Files to attach to the email. |

### `sendBulkEmails(recipients: string[], template: Omit<EmailOptions, 'to'>)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `recipients` | `string[]` | **Required.** Array of email addresses to receive the message. |
| `template` | `Omit<EmailOptions, 'to'>` | **Required.** Email options that will be applied to each recipient (subject, body, html, cc, bcc, attachments). |
| Returns | `Promise<EmailResult[]>` | An array of `EmailResult` objects, one per recipient, preserving order. |

---

## Implementation Note

The core transport function `sendViaProvider` is currently a stub that mimics an external email provider. To integrate with a real service (e.g., SendGrid, Mailgun, AWS SES), replace the stub with the provider‑specific SDK calls while keeping the public API unchanged.

```ts
// Example stub – replace with real implementation
async function sendViaProvider(opts: EmailOptions): Promise<EmailResult> {
  // Simulated async operation
  return {
    success: true,
    messageId: `simulated-${Date.now()}`,
    error: null,
  };
}
```

--- 

*Generated documentation reflects the current state of `email-service.ts` as of the last update.*