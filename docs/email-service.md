# email-service.ts

*Auto-generated from `./email-service.ts`*

# Email Service Module

The **email-service.ts** module provides a simple, type‑safe API for sending single or bulk emails.  
It validates recipients, supports plain‑text and HTML bodies, optional CC/BCC, and attachments.  
The actual transport is abstracted behind `sendViaProvider`, which can be swapped out for a real provider (SendGrid, Mailgun, SES, etc.) without changing the public API.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `EmailOptions` | *interface* | Configuration for a single email. |
| `Attachment` | *interface* | Represents an email attachment. |
| `EmailResult` | *interface* | Result of an email send operation. |
| `sendEmail` | *function* | Sends a single email. |
| `sendBulkEmails` | *function* | Sends the same template to multiple recipients. |

---

## Usage Examples

### 1. Sending a single email

```ts
import { sendEmail, EmailOptions } from './email-service';

const options: EmailOptions = {
  to: ['alice@example.com'],
  subject: 'Welcome!',
  body: 'Hello Alice, welcome to our platform.',
  html: '<p>Hello <strong>Alice</strong>, welcome to our platform.</p>',
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
  console.log(`Email sent, id: ${result.messageId}`);
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
    console.log(`Sent to ${recipients[idx]}: ${res.messageId}`);
  } else {
    console.warn(`Failed for ${recipients[idx]}: ${res.error}`);
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
| `options.bcc` | `string[]` | Optional. Blind carbon‑copy recipients. |
| `options.attachments` | `Attachment[]` | Optional. List of attachments. |

### `sendBulkEmails(recipients: string[], template: Omit<EmailOptions, 'to'>)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `recipients` | `string[]` | Array of email addresses to send the template to. |
| `template` | `Omit<EmailOptions, 'to'>` | Email template that will be merged with each recipient. |

---

## Return Values

### `sendEmail`

Returns a `Promise<EmailResult>`:

| Property | Type | Description |
|----------|------|-------------|
| `success` | `boolean` | `true` if the email was sent successfully. |
| `messageId` | `string` | **Optional**. Identifier returned by the provider. |
| `error` | `string` | **Optional**. Error message if `success` is `false`. |

### `sendBulkEmails`

Returns a `Promise<EmailResult[]>` – an array of results, one per recipient, preserving the order of the input `recipients` array.

---

## Types

### `EmailOptions`

```ts
interface EmailOptions {
  to: string[];          // Primary recipients
  subject: string;       // Email subject
  body: string;          // Plain‑text body
  html?: string;         // Optional HTML body
  cc?: string[];         // Optional CC recipients
  bcc?: string[];        // Optional BCC recipients
  attachments?: Attachment[]; // Optional attachments
}
```

### `Attachment`

```ts
interface Attachment {
  filename: string;      // File name shown to the recipient
  content: Buffer | string; // File content (binary or base64 string)
  contentType: string;   // MIME type (e.g., 'application/pdf')
}
```

### `EmailResult`

```ts
interface EmailResult {
  success: boolean;      // Operation status
  messageId?: string;    // Provider‑generated ID (if successful)
  error?: string;        // Error message (if failed)
}
```

---

## Extending the Provider

The `sendViaProvider` function is a stub that returns a fake message ID.  
Replace it with real integration logic:

```ts
async function sendViaProvider(options: EmailOptions): Promise<string> {
  const response = await sendGridClient.send({
    personalizations: [{ to: options.to.map(email => ({ email })) }],
    subject: options.subject,
    content: [
      { type: 'text/plain', value: options.body },
      ...(options.html ? [{ type: 'text/html', value: options.html }] : []),
    ],
    attachments: options.attachments?.map(att => ({
      filename: att.filename,
      content: att.content.toString('base64'),
      type: att.contentType,
      disposition: 'attachment',
    })),
  });

  return response.body.messageId; // or whatever the provider returns
}
```

---

### Notes

- **Validation**: The module checks for at least one recipient and validates all email addresses with a simple regex.  
- **Error handling**: All errors are caught and returned in the `EmailResult` object, allowing callers to handle failures gracefully.  
- **Bulk sending**: `sendBulkEmails` sends emails sequentially. For high‑volume scenarios, consider parallelizing with `Promise.all` and throttling to respect provider limits.  

Feel free to extend or replace the provider logic while keeping the public API unchanged.