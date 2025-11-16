# email-service.ts

*Auto-generated from `./email-service.ts`*

# Email Service Module (`email-service.ts`)

## Overview
The **Email Service** module provides a lightweight, type‑safe API for sending single or bulk emails.  
- Validates recipients and email addresses.  
- Supports plain‑text and HTML bodies, CC/BCC, and file attachments.  
- Returns a clear success/failure result with a message ID or error message.  
- Uses a stubbed provider (`sendViaProvider`) that can be swapped out for a real service (SendGrid, Mailgun, SES, etc.).

> **Tip:** Replace `sendViaProvider` with your preferred provider SDK for production use.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `EmailOptions` | *interface* | Configuration for a single email. |
| `Attachment` | *interface* | Represents an email attachment. |
| `EmailResult` | *interface* | Result of an email send operation. |
| `sendEmail` | *function* | Sends a single email. |
| `sendBulkEmails` | *function* | Sends the same template to many recipients. |

> *Internal helpers (`isValidEmail`, `sendViaProvider`) are not exported.*

---

## Usage Examples

### 1. Sending a single email

```ts
import { sendEmail, EmailOptions } from './email-service';

const email: EmailOptions = {
  to: ['alice@example.com', 'bob@example.com'],
  subject: 'Welcome!',
  body: 'Hello, welcome to our platform.',
  html: '<p>Hello, <strong>welcome</strong> to our platform.</p>',
  cc: ['carol@example.com'],
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

const recipients = ['alice@example.com', 'bob@example.com', 'carol@example.com'];

const template: Omit<EmailOptions, 'to'> = {
  subject: 'Monthly Newsletter',
  body: 'Here is our monthly newsletter.',
  html: '<h1>Monthly Newsletter</h1><p>Enjoy!</p>',
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
    to: ['invalid-email'],
    subject: 'Test',
    body: 'Testing',
  });

  if (!result.success) {
    throw new Error(result.error);
  }
} catch (err) {
  console.error('Email failed:', err.message);
}
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
| `options.attachments` | `Attachment[]` | Optional array of attachments. |

### `sendBulkEmails(recipients: string[], template: Omit<EmailOptions, 'to'>)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `recipients` | `string[]` | List of email addresses to send the template to. |
| `template` | `Omit<EmailOptions, 'to'>` | Email body, subject, etc. (no `to` field). |

---

## Return Values

### `sendEmail`

```ts
Promise<EmailResult>
```

| Property | Type | Description |
|----------|------|-------------|
| `success` | `boolean` | `true` if the email was queued/sent successfully. |
| `messageId` | `string | undefined` | Unique ID returned by the provider (present only when `success` is `true`). |
| `error` | `string | undefined` | Human‑readable error message (present only when `success` is `false`). |

### `sendBulkEmails`

```ts
Promise<EmailResult[]>
```

An array of `EmailResult` objects, one per recipient, preserving the order of `recipients`.

---

## Internal Helpers (Not exported)

| Function | Purpose |
|----------|---------|
| `isValidEmail(email: string): boolean` | Simple regex validation of an email address. |
| `sendViaProvider(options: EmailOptions): Promise<string>` | Stub that simulates sending an email and returns a fake message ID. Replace with real provider logic. |

---

## Extending the Module

1. **Replace the provider**  
   Swap `sendViaProvider` with your provider’s SDK (e.g., SendGrid’s `send` method).  
   ```ts
   async function sendViaProvider(options: EmailOptions): Promise<string> {
     const response = await sendgridClient.send({
       personalizations: [{ to: options.to.map(email => ({ email })) }],
       subject: options.subject,
       content: [
         { type: 'text/plain', value: options.body },
         ...(options.html ? [{ type: 'text/html', value: options.html }] : []),
       ],
       attachments: options.attachments?.map(att => ({
         content: att.content instanceof Buffer ? att.content.toString('base64') : Buffer.from(att.content).toString('base64'),
         filename: att.filename,
         type: att.contentType,
         disposition: 'attachment',
       })),
     });
     return response[0].messageId; // or whatever the provider returns
   }
   ```

2. **Parallel bulk sending**  
   `sendBulkEmails` currently sends sequentially. For higher throughput, use `Promise.all` or a concurrency limiter.

3. **Add logging**  
   Wrap `sendEmail` in a logger to capture metrics or audit trails.

---

## Importing the Module

```ts
import { sendEmail, sendBulkEmails, EmailOptions } from './email-service';
```

> The module uses ES module syntax (`export`). If you’re using CommonJS, adjust the import accordingly.

---

## Summary

- **`EmailOptions`** – fully typed email payload.  
- **`Attachment`** – file metadata + content.  
- **`EmailResult`** – clear success/failure indicator.  
- **`send