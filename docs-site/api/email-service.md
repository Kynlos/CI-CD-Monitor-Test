---
title: Email Service
layout: default
last_updated: 2025-11-16
---

# email-service.ts

*Auto-generated from `./email-service.ts`*

# Email Service Module (`email-service.ts`)

## Overview
The **Email Service** module provides a simple, type‑safe API for sending single or bulk emails.  
It validates recipients, supports optional CC/BCC, attachments, and HTML bodies, and returns a clear success/error result.  
The actual transport is abstracted behind `sendViaProvider`, which can be swapped out for a real provider (SendGrid, Mailgun, SES, etc.) without changing the public API.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `EmailOptions` | **Interface** | Configuration object for a single email. |
| `Attachment` | **Interface** | Represents an email attachment. |
| `EmailResult` | **Interface** | Result of an email send operation. |
| `sendEmail` | **Function** | Sends a single email. |
| `sendBulkEmails` | **Function** | Sends the same template to multiple recipients. |

---

## Usage Examples

### 1. Sending a Simple Text Email

```ts
import { sendEmail, EmailOptions } from './email-service';

const options: EmailOptions = {
  to: ['alice@example.com'],
  subject: 'Welcome!',
  body: 'Hello Alice, welcome to our platform.',
};

const result = await sendEmail(options);

if (result.success) {
  console.log(`Email sent, messageId: ${result.messageId}`);
} else {
  console.error(`Failed to send email: ${result.error}`);
}
```

### 2. Sending an HTML Email with CC, BCC, and Attachments

```ts
import { sendEmail, EmailOptions, Attachment } from './email-service';
import fs from 'fs';

const attachment: Attachment = {
  filename: 'report.pdf',
  content: fs.readFileSync('./report.pdf'), // Buffer
  contentType: 'application/pdf',
};

const options: EmailOptions = {
  to: ['bob@example.com'],
  cc: ['carol@example.com'],
  bcc: ['dave@example.com'],
  subject: 'Monthly Report',
  body: 'Please find the report attached.',
  html: '<p>Please find the <strong>report</strong> attached.</p>',
  attachments: [attachment],
};

const result = await sendEmail(options);

if (result.success) {
  console.log(`Email sent, messageId: ${result.messageId}`);
} else {
  console.error(`Failed to send email: ${result.error}`);
}
```

### 3. Sending Bulk Emails

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
| `template`  | `Omit<EmailOptions, 'to'>`        | Email template (subject, body, etc.) without the `to` field. |

---