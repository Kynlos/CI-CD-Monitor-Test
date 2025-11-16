---
title: Notifications
layout: default
---

# email-service.ts

*Auto-generated from `./email-service.ts`*

# Email Service Module

The **email-service.ts** module provides a lightweight, type‑safe API for sending single or bulk emails.  
It validates recipients, supports plain‑text and HTML bodies, optional CC/BCC, and attachments.  
The actual transport is abstracted behind `sendViaProvider`, which can be swapped out for a real provider (SendGrid, Mailgun, SES, etc.) without changing the public API.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `EmailOptions` | *interface* | Configuration object for a single email. |
| `Attachment` | *interface* | Represents an email attachment. |
| `EmailResult` | *interface* | Result returned after attempting to send an email. |
| `sendEmail(options: EmailOptions): Promise<EmailResult>` | *function* | Sends a single email. |
| `sendBulkEmails(recipients: string[], template: Omit<EmailOptions, 'to'>): Promise<EmailResult[]>` | *function* | Sends the same template to many recipients. |

---

## Usage Examples

### 1. Sending a single email

```ts
import { sendEmail, EmailOptions } from './email-service';

const email: EmailOptions = {
  to: ['alice@example.com', 'bob@example.com'],
  subject: 'Welcome to our service',
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
  html: '<h1>Monthly Newsletter</h1><p>Here is our monthly newsletter.</p>',
};

const results = await sendBulkEmails(recipients, template);

results.forEach((res, idx) => {
  if (res.success) {
    console.log(`Email to ${recipients[idx]} sent: ${res.messageId}`);
  } else {
    console.warn(`Email to ${recipients[idx]} failed: ${res.error}`);
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
| `options.cc` | `string[]` | Optional carbon‑copy recipients. |
| `options.bcc` | `string[]` | Optional blind‑carbon‑copy recipients. |
| `options.attachments` | `Attachment[]` | Optional list of attachments. |

### `sendBulkEmails(recipients, template)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `recipients` | `string[]` | List of email addresses to send the template to. |
| `template` | `Omit<EmailOptions, 'to'>` | Email configuration **excluding** the `to` field. The function will inject each recipient as the sole `to` address. |

---

## Return Values

### `sendEmail`

Returns a `Promise<EmailResult>`:

| Property | Type | Description |
|----------|------|-------------|
| `success` | `boolean` | `true` if the email was sent successfully. |
| `messageId` | `string` | **Optional.** Identifier returned by the provider (e.g., SendGrid message ID). Present only when `success` is `true`. |
| `error` | `string` | **Optional.** Human‑readable error message. Present only when `success` is `false`. |

### `sendBulkEmails`

Returns a `Promise<EmailResult[]>` – an array of results, one per recipient, preserving the order of the input `recipients` array.

---

## Notes & Extensibility

- **Validation**: The module validates that at least one recipient is provided and that all email addresses match a simple regex.  
- **Provider abstraction**: `sendViaProvider` is a stub that returns a fake message ID. Replace it with a real implementation (e.g., SendGrid, SES) to send actual emails.  
- **Attachments**: Accepts either a `Buffer` or a `string` for `content`. The `contentType` must be a valid MIME type.  
- **Error handling**: All errors are caught and returned in the `EmailResult.error` field, making it safe to call from async contexts without throwing.

Feel free to extend the module (e.g., add DKIM signing, retry logic, or template rendering) while keeping the public API stable.
