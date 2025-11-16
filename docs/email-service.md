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
  html: '<h1>Monthly Newsletter</h1><p>Here is our monthly newsletter.</p>',
};

const results = await sendBulkEmails(recipients, template);

results.forEach((res, idx) => {
  if (res.success) {
    console.log(`✅ ${recipients[idx]} → ${res.messageId}`);
  } else {
    console.warn(`❌ ${recipients[idx]} → ${res.error}`);
  }
});
```

### 3. Handling errors

```ts
import { sendEmail } from './email-service';

try {
  const result = await sendEmail({
    to: [], // intentionally empty
    subject: 'Test',
    body: 'Test body',
  });

  if (!result.success) {
    throw new Error(result.error);
  }
} catch (err) {
  console.error('Email failed:', err);
}
```

---

## Parameters

### `sendEmail(options: EmailOptions)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `options` | `EmailOptions` | Email configuration. |
| `options.to` | `string[]` | **Required.** Recipients’ email addresses. |
| `options.subject` | `string` | **Required.** Email subject line. |
| `options.body` | `string` | **Required.** Plain‑text body. |
| `options.html` | `string` | Optional HTML body. |
| `options.cc` | `string[]` | Optional CC recipients. |
| `options.bcc` | `string[]` | Optional BCC recipients. |
| `options.attachments` | `Attachment[]` | Optional list of attachments. |

### `sendBulkEmails(recipients: string[], template: Omit<EmailOptions, 'to'>)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `recipients` | `string[]` | Array of email addresses to send to. |
| `template` | `Omit<EmailOptions, 'to'>` | Email template (subject, body, etc.) that will be applied to each recipient. |

---

## Return Values

### `sendEmail`

Returns a `Promise<EmailResult>`:

| Property | Type | Description |
|----------|------|-------------|
| `success` | `boolean` | `true` if the email was sent successfully. |
| `messageId` | `string` | **Optional.** Identifier returned by the provider (e.g., SendGrid message ID). |
| `error` | `string` | **Optional.** Error message if `success` is `false`. |

### `sendBulkEmails`

Returns a `Promise<EmailResult[]>` – an array of results, one per recipient, preserving order.

---

## Internal Helpers (not exported)

| Function | Purpose |
|----------|---------|
| `isValidEmail(email: string): boolean` | Validates email format using a simple regex. |
| `sendViaProvider(options: EmailOptions): Promise<string>` | Simulates sending an email and returns a fake message ID. Replace with real provider integration. |

---

### Notes

- **Validation**: The module checks that at least one recipient is supplied and that all addresses (to, cc, bcc) match a basic email regex.  
- **Attachments**: `content` can be a `Buffer` or a `string`. The `contentType` must be a valid MIME type.  
- **Extensibility**: Swap out `sendViaProvider` with your provider’s SDK (SendGrid, Mailgun, SES, etc.) to add real delivery.  
- **Error handling**: All errors are caught and returned in the `EmailResult.error` field; no exceptions bubble up from `sendEmail` or `sendBulkEmails`.  

Feel free to extend the module with additional features such as retry logic, rate‑limiting, or templating engines.