---
title: Email Service
layout: default
---

_Last updated: 2025-11-16_

# email-service.ts

*Auto‑generated from `./email-service.ts`*

# Email Service Module (`email-service.ts`)

## Overview
The **Email Service** module provides a simple, type‑safe API for sending single or bulk emails.  
It validates recipients, supports optional CC/BCC, attachments, and HTML bodies, and returns a clear success/error result.  
The actual transport is abstracted behind `sendViaProvider`, which can be swapped out for a real provider (SendGrid, Mailgun, SES, etc.) without changing the public API.

---

## Exports

| Export          | Type      | Description                                            |
|-----------------|-----------|--------------------------------------------------------|
| `EmailOptions`  | **Interface** | Configuration object for a single email.               |
| `Attachment`    | **Interface** | Represents an email attachment.                         |
| `EmailResult`   | **Interface** | Result of an email send operation.                      |
| `sendEmail`     | **Function**  | Sends a single email.                                    |
| `sendBulkEmails`| **Function**  | Sends the same template to multiple recipients.          |

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

### 2. Sending a Single Email with Attachments & HTML

```ts
import { sendEmail, EmailOptions, Attachment } from './email-service';
import fs from 'fs';

const attachment: Attachment = {
  filename: 'welcome.pdf',
  content: fs.readFileSync('./welcome.pdf'), // Buffer
  contentType: 'application/pdf',
};

const email: EmailOptions = {
  to: ['alice@example.com'],
  cc: ['bob@example.com'],
  subject: 'Welcome!',
  body: 'Hello Alice, welcome aboard.',
  html: '<p>Hello <strong>Alice</strong>, welcome aboard.</p>',
  attachments: [attachment],
};

const result = await sendEmail(email);

if (result.success) {
  console.log(`Email sent, messageId: ${result.messageId}`);
} else {
  console.error(`Failed to send email: ${result.error}`);
}
```

### 3. Sending an HTML Email with CC, BCC, and Attachments

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

| Parameter               | Type                     | Description                                          |
|-------------------------|--------------------------|------------------------------------------------------|
| `options`               | `EmailOptions`           | Email configuration object.                         |
| `options.to`            | `string[]`               | **Required.** List of primary recipients.           |
| `options.subject`       | `string`                 | **Required.** Email subject line.                   |
| `options.body`          | `string`                 | **Required.** Plain‑text body of the email.         |
| `options.html?`         | `string`                 | Optional HTML version of the body.                  |
| `options.cc?`           | `string[]`               | Optional list of CC recipients.                     |
| `options.bcc?`          | `string[]`               | Optional list of BCC recipients.                    |
| `options.attachments?`  | `Attachment[]`           | Optional array of file attachments.                 |

### `sendBulkEmails(recipients: string[], template: Omit<EmailOptions, 'to'>)`

| Parameter               | Type                     | Description                                          |
|-------------------------|--------------------------|------------------------------------------------------|
| `recipients`            | `string[]`               | **Required.** Array of email addresses to send to.   |
| `template`              | `Omit<EmailOptions,'to'>`| **Required.** Email options that apply to every recipient (subject, body, html, cc, bcc, attachments). |
| Returns                 | `Promise<EmailResult[]>` | Resolves with an array of results, one per recipient. |

---

## Types

```ts
export interface Attachment {
  /** Name of the file, e.g., "invoice.pdf". */
  filename: string;
  /** File content as a Buffer. */
  content: Buffer;
  /** MIME type, e.g., "application/pdf". */
  contentType: string;
}

export interface EmailOptions {
  /** Primary recipients. */
  to: string[];
  /** Optional CC recipients. */
  cc?: string[];
  /** Optional BCC recipients. */
  bcc?: string[];
  /** Email subject line. */
  subject: string;
  /** Plain‑text body. */
  body: string;
  /** Optional HTML body. */
  html?: string;
  /** Optional attachments. */
  attachments?: Attachment[];
}

export interface EmailResult {
  /** `true` if the email was accepted by the provider. */
  success: boolean;
  /** Provider‑specific message identifier (if any). */
  messageId?: string;
  /** Error description when `success` is `false`. */
  error?: string;
}
```

--- 

*All code examples assume an async context (e.g., top‑level `await` in an ES module or within an `async` function).*