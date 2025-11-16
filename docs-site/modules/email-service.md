---
title: Email Service
layout: default
---

*Last updated: 2025-11-16*

# email-service.ts

*Auto-generated from `./email-service.ts`*

# Email Service Module (`email-service.ts`)

## Overview
The **Email Service** module provides a simple, type‑safe API for sending single or bulk emails.  
- Validates recipients and email addresses.  
- Supports plain‑text, HTML bodies, CC/BCC, and file attachments.  
- Abstracts the underlying provider (e.g., SendGrid, Mailgun, SES) behind `sendViaProvider`, allowing the transport layer to be swapped without changing the public API.  
- Returns a consistent `EmailResult` object indicating success or failure.

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
  console.log(`HTML email sent! Message ID: ${result.messageId}`);
} else {
  console.error(`Failed to send HTML email: ${result.error}`);
}
```

### 3. Sending a Single Email with Attachments (Full Example)

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

### 4. Sending Bulk Emails

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
| `recipients` | `string[]` | **Required.** Array of email addresses that will receive the email. |
| `template` | `Omit<EmailOptions, 'to'>` | **Required.** Email options shared by all recipients (subject, body, html, cc, bcc, attachments, etc.). |
| Returns | `Promise<EmailResult[]>` | A promise that resolves to an array of `EmailResult` objects, one per recipient, preserving order. |

--- 

*End of documentation.*