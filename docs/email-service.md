# email-service.ts

*Auto-generated from `./email-service.ts`*

# Email Service Module (`email-service.ts`)

A lightweight, type‑safe email helper written in TypeScript.  
It validates recipients, supports optional CC/BCC, attachments, and HTML bodies, and returns a clear success/error result.  
The actual sending logic is abstracted in `sendViaProvider`, which is currently a stub that simulates a provider (SendGrid, Mailgun, etc.). Replace it with your real provider integration.

---

## Overview

- **Send a single email** with `sendEmail`.
- **Send bulk emails** to many recipients with `sendBulkEmails`.
- **Strong typing** for options, attachments, and results.
- **Built‑in validation** for email addresses.
- **Extensible** – swap out the provider logic without touching the public API.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `EmailOptions` | `interface` | Configuration for an email message. |
| `Attachment` | `interface` | Representation of an attachment. |
| `EmailResult` | `interface` | Result of a send operation. |
| `sendEmail` | `function` | Sends a single email. |
| `sendBulkEmails` | `function` | Sends the same template to many recipients. |

---

## Usage Examples

### 1. Sending a Simple Email

```ts
import { sendEmail, EmailOptions } from './email-service';

const options: EmailOptions = {
  to: ['alice@example.com'],
  subject: 'Hello World',
  body: 'This is a plain‑text email.',
};

const result = await sendEmail(options);
console.log(result); // { success: true, messageId: 'msg_1700000000000' }
```

### 2. Sending an Email with HTML, CC, BCC, and Attachments

```ts
import { sendEmail, EmailOptions, Attachment } from './email-service';
import fs from 'fs';

const attachment: Attachment = {
  filename: 'report.pdf',
  content: fs.readFileSync('./report.pdf'),
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
console.log(result);
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
  subject: 'Welcome!',
  body: 'Thank you for joining our platform.',
  html: '<h1>Welcome!</h1>',
};

const results = await sendBulkEmails(recipients, template);
console.log(results);
// [
//   { success: true, messageId: 'msg_1700000000001' },
//   { success: true, messageId: 'msg_1700000000002' },
//   { success: true, messageId: 'msg_1700000000003' }
// ]
```

### 4. Handling Errors

```ts
import { sendEmail } from './email-service';

const badOptions = {
  to: ['invalid-email'],
  subject: 'Test',
  body: 'Hello',
};

const result = await sendEmail(badOptions);
if (!result.success) {
  console.error('Failed to send email:', result.error);
}
```

---

## Parameters

### `sendEmail(options: EmailOptions)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `options` | `EmailOptions` | Email configuration object. |

#### `EmailOptions`

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `to` | `string[]` | ✅ | Recipients’ email addresses. |
| `subject` | `string` | ✅ | Email subject line. |
| `body` | `string` | ✅ | Plain‑text body. |
| `html` | `string` | ❌ | Optional HTML body. |
| `cc` | `string[]` | ❌ | Optional CC recipients. |
| `bcc` | `string[]` | ❌ | Optional BCC recipients. |
| `attachments` | `Attachment[]` | ❌ | Optional file attachments. |

#### `Attachment`

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `filename` | `string` | ✅ | File name to appear in the email. |
| `content` | `Buffer | string` | ✅ | File data. |
| `contentType` | `string` | ✅ | MIME type (e.g., `application/pdf`). |

### `sendBulkEmails(recipients: string[], template: Omit<EmailOptions, 'to'>)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `recipients` | `string[]` | Array of email addresses to send to. |
| `template` | `Omit<EmailOptions, 'to'>` | Email configuration without the `to` field; will be applied to each recipient. |

---

## Return Values

### `sendEmail`

| Property | Type | Description |
|----------|------|-------------|
| `success` | `boolean` | `true` if the email was sent, `false` otherwise. |
| `messageId` | `string` | Provider‑generated message ID (present only on success). |
| `error` | `string` | Human‑readable error message (present only on failure). |

### `sendBulkEmails`

Returns an array of `EmailResult` objects, one per recipient, preserving the order of `recipients`.

---

## Extending the Module

| Area | How to Extend |
|------|---------------|
| **Provider** | Replace `sendViaProvider` with real API calls (SendGrid, Mailgun, SES, etc.). Ensure it returns a string ID. |
| **Validation** | Swap `isValidEmail` for a more robust validator if needed. |
| **Concurrency** | `sendBulkEmails` currently sends sequentially. For high‑volume use, wrap the loop in `Promise.all` or a concurrency limiter. |
| **Logging** | Add logging inside `sendEmail` or `sendBulkEmails` for audit trails. |

---

## Importing

```ts
import {
  EmailOptions,
  Attachment,
  EmailResult,
