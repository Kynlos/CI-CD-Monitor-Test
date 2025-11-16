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
It validates recipients, supports plain‑text and HTML bodies, handles CC/BCC, and allows attachments.  
The implementation is intentionally minimal – the `sendViaProvider` function is a stub that simulates an external provider (SendGrid, Mailgun, etc.). Replace it with real provider logic in production.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `EmailOptions` | **Interface** | Configuration object for a single email. |
| `Attachment` | **Interface** | Represents a file attachment. |
| `EmailResult` | **Interface** | Result of an email send operation. |
| `sendEmail` | **Function** | Sends a single email. |
| `sendBulkEmails` | **Function** | Sends the same template to many recipients. |

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

| Parameter | Type          | Description                              |
|-----------|---------------|------------------------------------------|
| `options` | `EmailOptions`| Email configuration object.              |

### `sendBulkEmails(recipients: string[], template: Omit<EmailOptions, 'to'>)`

| Parameter   | Type                              | Description                                 |
|-------------|-----------------------------------|---------------------------------------------|
| `recipients`| `string[]`                        | List of email addresses to receive the email. |
| `template`  | `Omit<EmailOptions, 'to'>`        | Email configuration without the `to` field; will be merged with each recipient. |

> **Note:** `isValidEmail` and `sendViaProvider` are internal helpers and are **not** exported.
```