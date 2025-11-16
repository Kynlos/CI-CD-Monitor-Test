```markdown
---
title: Email Service
layout: default
last_updated: 2025-11-16
---

# email-service.ts

*Auto-generated from `./email-service.ts`*

# Email Service Module (`email-service.ts`)

## Overview
The **Email Service** module provides a lightweight, type‑safe API for sending single or bulk emails.  
- Validates recipient addresses and optional CC/BCC lists.  
- Supports plain‑text and HTML bodies, as well as file attachments.  
- Returns a structured result indicating success, the provider’s message ID, or an error message.  
- Designed to be provider‑agnostic; the actual sending logic is abstracted behind `sendViaProvider`, which can be swapped out for a real SMTP/SendGrid/Mailgun/SES implementation in production.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `EmailOptions` | **Interface** | Configuration for a single email. |
| `Attachment` | **Interface** | Represents an email attachment. |
| `EmailResult` | **Interface** | Result of an email send operation. |
| `sendEmail(options: EmailOptions)` | **Async Function** | Sends a single email. |
| `sendBulkEmails(recipients: string[], template: Omit<EmailOptions, 'to'>)` | **Async Function** | Sends the same template to many recipients. |

> **Note:** `isValidEmail` and `sendViaProvider` are internal helpers and are **not** exported.

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
  'bob@example.com',
  'carol@example.com',
  'dave@example.com',
];

const template: Omit<EmailOptions, 'to'> = {
  subject: 'Monthly Newsletter',
  body: 'Here is this month’s newsletter.',
  html: '<h1>Monthly Newsletter</h1><p>Enjoy!</p>',
};

const results = await sendBulkEmails(recipients, template);

results.forEach((res, idx) => {
  if (res.success) {
    console.log(`✅ Sent to ${recipients[idx]} (id: ${res.messageId})`);
  } else {
    console.warn(`❌ Failed to send to ${recipients[idx]}: ${res.error}`);
  }
});
```

---

## Parameters

### `sendEmail(options: EmailOptions)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `options` | `EmailOptions` | Email configuration object. |
| `options.to` | `string[]` | **Required.** Recipients’ email addresses. |
| `options.subject` | `string` | **Required.** Email subject line. |
| `options.body` | `string` | **Required.** Plain‑text body. |
| `options.html` | `string` | Optional HTML body. |
| `options.cc` | `string[]` | Optional CC recipients. |
| `options.bcc` | `string[]` | Optional BCC recipients. |
| `options.attachments` | `Attachment[]` | Optional file attachments. |

### `sendBulkEmails(recipients: string[], template: Omit<EmailOptions, 'to'>)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `recipients` | `string[]` | **Required.** List of email addresses to receive the email. |
| `template` | `Omit<EmailOptions, 'to'>` | **Required.** Email options that apply to every recipient (subject, body, html, cc, bcc, attachments, etc.). |

---

## Internal Helpers (not exported)

- `isValidEmail(email: string): boolean` – Simple regex‑based validation used internally.  
- `sendViaProvider(options: EmailOptions): Promise<EmailResult>` – Abstracted sending implementation; replace with your provider of choice.

```