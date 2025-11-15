---
title: Email Service
layout: default
---

# email-service.ts

*Auto-generated from `./email-service.ts`*

# Email Service Module (`email-service.ts`)

## Overview
The **Email Service** module provides a simple, type‑safe API for sending single or bulk emails.  
- Validates recipient addresses and optional CC/BCC lists.  
- Supports plain‑text and HTML bodies, as well as attachments.  
- Returns a structured result indicating success, the provider’s message ID, or an error message.  
- Designed to be provider‑agnostic; the `sendViaProvider` helper can be swapped out for a real SMTP/SendGrid/Mailgun implementation.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `EmailOptions` | **Interface** | Configuration object for an email. |
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
| `recipients` | `string[]` | List of email addresses to send the template to. |
| `template` | `Omit<EmailOptions, 'to'>` | Email template without the `to` field; will be applied to each recipient. |

---

## Return Values

### `sendEmail`

Returns a `Promise<EmailResult>`:

| Property | Type | Description |
|----------|------|-------------|
| `success` | `boolean` | `true` if the email was accepted by the provider. |
| `messageId` | `string` | Provider‑generated message ID (present only when `success` is `true`). |
| `error` | `string` | Human‑readable error message (present only when `success` is `false`). |

### `sendBulkEmails`

Returns a `Promise<EmailResult[]>` – an array of results, one per recipient, preserving the order of the `recipients` array.

---

## Extending / Customizing

- **Provider Integration**: Replace the stub `sendViaProvider` with a real implementation (SendGrid, Mailgun, SMTP, etc.).  
- **Validation**: The current regex is simple; swap `isValidEmail` for a more robust validator if needed.  
- **Error Handling**: The returned `error` string can be logged or surfaced to the UI.  

---

### Quick Reference

```ts
// Interfaces
interface EmailOptions { /* ... */ }
interface Attachment { /* ... */ }
interface EmailResult { /* ... */ }

// Functions
async function sendEmail(options: EmailOptions): Promise<EmailResult>
async function sendBulkEmails(recipients: string[], template: Omit<EmailOptions, 'to'>): Promise<EmailResult[]>
```

Use these exports to build reliable, type‑safe email workflows in your TypeScript projects.
