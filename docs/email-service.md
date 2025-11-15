# email-service.ts

*Auto-generated from `./email-service.ts`*

# Email Service Module

A lightweight, type‑safe email helper that validates recipients, supports attachments, and can send single or bulk emails.  
The module is intentionally provider‑agnostic – the actual transport logic is abstracted behind `sendViaProvider`, which you can replace with a real provider (SendGrid, Mailgun, SES, etc.) without touching the public API.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `EmailOptions` | *interface* | Configuration object for a single email. |
| `Attachment` | *interface* | Representation of an email attachment. |
| `EmailResult` | *interface* | Result returned after attempting to send an email. |
| `sendEmail(options: EmailOptions): Promise<EmailResult>` | *function* | Sends a single email. |
| `sendBulkEmails(recipients: string[], template: Omit<EmailOptions, 'to'>): Promise<EmailResult[]>` | *function* | Sends the same template to many recipients, returning an array of results. |

---

## Overview

- **Validation** – Checks that at least one recipient exists and that all email addresses (to, cc, bcc) match a simple RFC‑5322‑like regex.
- **Attachments** – Supports binary (`Buffer`) or string content with MIME type.
- **Bulk sending** – Calls `sendEmail` sequentially for each recipient; you can replace this with parallelism if needed.
- **Extensibility** – Replace `sendViaProvider` with a real provider implementation; the rest of the API remains unchanged.

---

## Usage Examples

> **Tip:** Import the module with named imports to keep the bundle size minimal.

```ts
import {
  sendEmail,
  sendBulkEmails,
  EmailOptions,
  Attachment,
  EmailResult
} from './email-service';
```

### 1. Send a single email

```ts
const email: EmailOptions = {
  to: ['alice@example.com'],
  subject: 'Welcome!',
  body: 'Hello Alice, welcome to our platform.',
  html: '<p>Hello <strong>Alice</strong>, welcome to our platform.</p>',
  cc: ['bob@example.com'],
  attachments: [
    {
      filename: 'welcome.pdf',
      content: Buffer.from('PDF content here', 'utf-8'),
      contentType: 'application/pdf'
    }
  ]
};

const result: EmailResult = await sendEmail(email);

if (result.success) {
  console.log(`Email sent! Message ID: ${result.messageId}`);
} else {
  console.error(`Failed to send email: ${result.error}`);
}
```

### 2. Send bulk emails

```ts
const recipients = [
  'alice@example.com',
  'bob@example.com',
  'carol@example.com'
];

const template: Omit<EmailOptions, 'to'> = {
  subject: 'Monthly Newsletter',
  body: 'Here is our monthly newsletter.',
  html: '<h1>Monthly Newsletter</h1><p>Here is our monthly newsletter.</p>'
};

const results = await sendBulkEmails(recipients, template);

results.forEach((res, idx) => {
  const recipient = recipients[idx];
  if (res.success) {
    console.log(`✅ Sent to ${recipient} (ID: ${res.messageId})`);
  } else {
    console.warn(`❌ Failed to send to ${recipient}: ${res.error}`);
  }
});
```

### 3. Custom provider implementation

Replace the stubbed `sendViaProvider` with your own logic:

```ts
// In a separate file, e.g., provider.ts
import { EmailOptions } from './email-service';

export async function sendViaProvider(options: EmailOptions): Promise<string> {
  // Example with SendGrid
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
      filename: att.filename,
      content: att.content.toString('base64'),
      type: att.contentType,
      disposition: 'attachment'
    }))
  };

  const response = await sgMail.send(msg);
  return response[0].headers['x-message-id'] ?? 'unknown';
}
```

Then import this provider in your main service file and replace the stub.

---

## Parameters

### `sendEmail(options: EmailOptions)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `options` | `EmailOptions` | Full email configuration. |
| `options.to` | `string[]` | **Required**. List of primary recipients. |
| `options.subject` | `string` | Email subject line. |
| `options.body` | `string` | Plain‑text body. |
| `options.html` | `string` | Optional HTML body. |
| `options.cc` | `string[]` | Optional carbon‑copy recipients. |
| `options.bcc` | `string[]` | Optional blind‑carbon‑copy recipients. |
| `options.attachments` | `Attachment[]` | Optional list of attachments. |

### `sendBulkEmails(recipients: string[], template: Omit<EmailOptions, 'to'>)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `recipients` | `string[]` | Array of email addresses to send the template to. |
| `template` | `Omit<EmailOptions, 'to'>` | Email configuration **without** the `to` field; the function will inject each recipient individually. |

---

## Return Values

### `sendEmail`

| Property | Type | Description |
|----------|------|-------------|
| `success` | `boolean` | `true` if the email was sent successfully. |
| `messageId` | `string | undefined` | Provider‑generated message ID (present only on success). |
| `error` | `string | undefined` | Human‑readable error message (present only on failure). |

### `sendBulkEmails`

Returns an array of `EmailResult` objects, one per recipient, preserving the order of the input `recipients` array. Each element follows the same structure as `sendEmail`’s return value.

---

## Extending the API

- **Parallel bulk sending** – Replace the `for…of` loop with `Promise.all` if you want concurrent sends.
- **Retry logic** – Wrap `sendEmail` in a retry helper to handle transient failures.
- **Custom validation** – Replace `isValidEmail` with a more robust validator if needed.

---

## License

MIT © 2025

---