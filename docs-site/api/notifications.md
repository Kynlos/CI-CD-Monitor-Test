---
title: Notifications
layout: default
---

# email-service.ts

*Auto-generated from `./email-service.ts`*

# Email Service Module (`email-service.ts`)

## Overview
The **Email Service Module** provides a lightweight, type‑safe API for sending single or bulk emails.  
- Validates recipients (to, cc, bcc) using a simple regex.  
- Supports plain‑text and HTML bodies, optional CC/BCC, and file attachments.  
- Returns a clear success/failure result with a message ID or an error string.  
- The actual sending is delegated to `sendViaProvider`, which is currently a stub that simulates a provider (e.g., SendGrid, Mailgun).  
- Designed for use in Node.js/TypeScript projects that need a quick, testable email helper without pulling in heavy dependencies.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `EmailOptions` | *interface* | Configuration object for a single email. |
| `Attachment` | *interface* | Represents a file attachment. |
| `EmailResult` | *interface* | Result of an email send operation. |
| `sendEmail(options: EmailOptions): Promise<EmailResult>` | *function* | Sends a single email. |
| `sendBulkEmails(recipients: string[], template: Omit<EmailOptions, 'to'>): Promise<EmailResult[]>` | *function* | Sends the same template to many recipients, returning an array of results. |

> **Note:** `isValidEmail` and `sendViaProvider` are internal helpers and not exported.

---

## Usage Examples

### 1. Sending a Simple Email

```ts
import { sendEmail, EmailOptions } from './email-service';

const email: EmailOptions = {
  to: ['alice@example.com'],
  subject: 'Welcome!',
  body: 'Hello Alice, welcome to our platform.',
};

const result = await sendEmail(email);

if (result.success) {
  console.log(`Email sent, ID: ${result.messageId}`);
} else {
  console.error(`Failed to send email: ${result.error}`);
}
```

### 2. Email with CC, BCC, and Attachments

```ts
import { sendEmail, EmailOptions, Attachment } from './email-service';
import fs from 'fs';

const attachment: Attachment = {
  filename: 'report.pdf',
  content: fs.readFileSync('./report.pdf'), // Buffer
  contentType: 'application/pdf',
};

const email: EmailOptions = {
  to: ['bob@example.com'],
  cc: ['carol@example.com'],
  bcc: ['dave@example.com'],
  subject: 'Monthly Report',
  body: 'Please find the attached report.',
  html: '<p>Please find the attached report.</p>',
  attachments: [attachment],
};

const result = await sendEmail(email);
```

### 3. Sending Bulk Emails

```ts
import { sendBulkEmails, EmailOptions } from './email-service';

const recipients = [
  'user1@example.com',
  'user2@example.com',
  'user3@example.com',
];

const template: Omit<EmailOptions, 'to'> = {
  subject: 'Weekly Newsletter',
  body: 'Here is this week’s news...',
  html: '<h1>Weekly Newsletter</h1><p>Here is this week’s news...</p>',
};

const results = await sendBulkEmails(recipients, template);

results.forEach((res, idx) => {
  if (res.success) {
    console.log(`Email ${idx + 1} sent, ID: ${res.messageId}`);
  } else {
    console.error(`Email ${idx + 1} failed: ${res.error}`);
  }
});
```

---

## Parameters

### `EmailOptions`
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `to` | `string[]` | ✔ | Primary recipients. |
| `subject` | `string` | ✔ | Email subject line. |
| `body` | `string` | ✔ | Plain‑text body. |
| `html` | `string` | ✖ | Optional HTML body. |
| `cc` | `string[]` | ✖ | Carbon‑copy recipients. |
| `bcc` | `string[]` | ✖ | Blind carbon‑copy recipients. |
| `attachments` | `Attachment[]` | ✖ | List of files to attach. |

### `Attachment`
| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `filename` | `string` | ✔ | File name shown to the recipient. |
| `content` | `Buffer | string` | ✔ | File data; can be a `Buffer` or a base64/UTF‑8 string. |
| `contentType` | `string` | ✔ | MIME type (e.g., `application/pdf`). |

### `sendEmail(options: EmailOptions)`
- **`options`** – Email configuration object (see `EmailOptions`).

### `sendBulkEmails(recipients: string[], template: Omit<EmailOptions, 'to'>)`
- **`recipients`** – Array of email addresses to send the template to.  
- **`template`** – Email body, subject, attachments, etc., *excluding* the `to` field. The function will wrap each recipient in its own `EmailOptions` object.

---

## Return Values

### `EmailResult`
| Property | Type | Description |
|----------|------|-------------|
| `success` | `boolean` | `true` if the email was sent successfully. |
| `messageId` | `string | undefined` | Identifier returned by the provider (e.g., `msg_123456`). Present only on success. |
| `error` | `string | undefined` | Human‑readable error message. Present only on failure. |

### `sendEmail`
Returns a `Promise<EmailResult>`.

### `sendBulkEmails`
Returns a `Promise<EmailResult[]>`.  
The array order matches the input `recipients` array.

---

## Error Handling

- **No recipients** → `success: false`, `error: 'No recipients specified'`.
- **Invalid email address** → `success: false`, `error: 'Invalid email addresses: …'`.
- **Provider failure** → `success: false`, `error` contains the provider’s error message or `'Unknown error'`.

All errors are surfaced via the `error` property; the function never throws.

---

## Extending the Provider

Replace the stub `sendViaProvider` with real integration logic:

```ts
async function sendViaProvider(options: EmailOptions): Promise<string> {
  // Example using SendGrid
  const sgMail = require('@sendgrid/mail');
  sgMail.setApiKey(process.env.SENDGRID_API_KEY);

  const msg = {
    to: options.to,
    cc: options.cc,
    bcc: options.bcc,
    subject: options.subject,
    text: options.body,
    html: options.html,
    attachments: options.attachments?.map(att => ({
      content: att.content instanceof Buffer ? att.content.toString('base64') : att.content,
      filename: att.filename,
      type: att.contentType,
      disposition: 'attachment',
    })),
  };

  const response = await sgMail.send(msg);
  return response[0].headers['x-message-id'];
}
```

---

## Summary

- **`sendEmail`** – One‑off email with full validation and optional attachments.  
- **`sendBulkEmails`** – Re‑uses `sendEmail` to dispatch the same template to many recipients, returning a per‑recipient result.  
- **Type safety** – All inputs and outputs are strongly typed.  
- **Extensibility** – Swap out the provider stub for any real email service without touching the API surface.
