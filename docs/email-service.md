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
```

### 3. Sending Bulk Emails with a Template

```ts
import { sendBulkEmails, EmailOptions } from './email-service';

const recipients = [
  'user1@example.com',
  'user2@example.com',
  'user3@example.com',
];

const template: Omit<EmailOptions, 'to'> = {
  subject: 'Weekly Newsletter',
  body: 'Hello, this is our weekly newsletter.',
  html: '<h1>Weekly Newsletter</h1><p>Enjoy!</p>',
};

const results = await sendBulkEmails(recipients, template);

results.forEach((res, idx) => {
  if (res.success) {
    console.log(`Email ${idx + 1} sent: ${res.messageId}`);
  } else {
    console.error(`Email ${idx + 1} failed: ${res.error}`);
  }
});
```

---

## Parameters

### `sendEmail(options: EmailOptions)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `options` | `EmailOptions` | Email configuration object. |
| `options.to` | `string[]` | **Required**. List of primary recipients. |
| `options.subject` | `string` | **Required**. Email subject line. |
| `options.body` | `string` | **Required**. Plain‑text body. |
| `options.html` | `string` | Optional. HTML body. |
| `options.cc` | `string[]` | Optional. Carbon‑copy recipients. |
| `options.bcc` | `string[]` | Optional. Blind‑carbon‑copy recipients. |
| `options.attachments` | `Attachment[]` | Optional. List of attachments. |

### `sendBulkEmails(recipients: string[], template: Omit<EmailOptions, 'to'>)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `recipients` | `string[]` | Array of email addresses to send the template to. |
| `template` | `Omit<EmailOptions, 'to'>` | Email template (subject, body, etc.) that will be applied to each recipient. |

---

## Return Values

### `sendEmail`

Returns a `Promise<EmailResult>`:

| Property | Type | Description |
|----------|------|-------------|
| `success` | `boolean` | `true` if the email was sent successfully. |
| `messageId` | `string` | **Optional**. Identifier returned by the provider (e.g., SendGrid message ID). |
| `error` | `string` | **Optional**. Human‑readable error message if `success` is `false`. |

### `sendBulkEmails`

Returns a `Promise<EmailResult[]>` – an array of results, one per recipient, preserving the order of the input array.

---

## Notes & Best Practices

- **Validation**: The module performs basic email format validation. It will reject the send if any address is malformed.
- **Attachments**: `content` can be a `Buffer` (binary data) or a `string` (e.g., base64). Set `contentType` accordingly.
- **Async/Await**: Both functions are asynchronous; use `await` or `.then()` to handle the returned promises.
- **Error Handling**: Always check `result.success` before assuming the email was delivered. The `error` field contains a descriptive message.
- **Extensibility**: Replace `sendViaProvider` with a real provider implementation to integrate with SendGrid, Mailgun, SES, etc. The public API remains unchanged.

---

## API Reference

### `interface EmailOptions`

```ts
export interface EmailOptions {
  to: string[];               // Primary recipients
  subject: string;            // Email subject
  body: string;               // Plain‑text body
  html?: string;              // Optional HTML body
  cc?: string[];              // Optional CC recipients
  bcc?: string[];             // Optional BCC recipients
  attachments?: Attachment[]; // Optional attachments
}
```

### `interface Attachment`

```ts
export interface Attachment {
  filename: string;           // File name to appear in the email
  content: Buffer | string;   // File data (Buffer or string)
  contentType: string;        // MIME type (e.g., 'application/pdf')
}
```

### `interface EmailResult`

```ts
export interface EmailResult {
  success: boolean;   // true if email was sent
  messageId?: string; // provider‑specific ID
  error?: string;     // error message if success is false
}
```

### `async function sendEmail(options: EmailOptions): Promise<EmailResult>`

Sends a single email after validating recipients and addresses. Returns a detailed result object.

### `async function sendBulkEmails(recipients: string[], template: Omit<EmailOptions, 'to'>): Promise<EmailResult[]>`

Iterates over `recipients`, sending the same `template` to each. Returns an array of `EmailResult` objects in the same order as the input list.

---