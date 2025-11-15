# email-service.ts

*Auto-generated from `./email-service.ts`*

# Email Service Module

The **email-service.ts** module provides a simple, type‑safe API for sending single or bulk emails.  
It validates recipients, supports plain‑text and HTML bodies, optional CC/BCC, and attachments.  
The actual sending is delegated to a provider‑specific implementation (`sendViaProvider`), which is currently a stub but can be replaced with a real service such as SendGrid, Mailgun, SES, etc.

---

## Exports

| Export | Type | Description |
|--------|------|-------------|
| `EmailOptions` | *interface* | Configuration object for a single email. |
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
      filename: 'terms.pdf',
      content: Buffer.from('PDF content here', 'utf-8'),
      contentType: 'application/pdf',
    },
  ],
};

const result = await sendEmail(options);

if (result.success) {
  console.log(`Email sent, message ID: ${result.messageId}`);
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
    console.log(`Email to ${recipients[idx]} sent (ID: ${res.messageId})`);
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
| `options.body` | `string` | **Required.** Plain‑text body of the email. |
| `options.html` | `string` | Optional HTML body. |
| `options.cc` | `string[]` | Optional carbon‑copy recipients. |
| `options.bcc` | `string[]` | Optional blind carbon‑copy recipients. |
| `options.attachments` | `Attachment[]` | Optional list of attachments. |

### `sendBulkEmails(recipients: string[], template: Omit<EmailOptions, 'to'>)`

| Parameter | Type | Description |
|-----------|------|-------------|
| `recipients` | `string[]` | Array of email addresses to send the template to. |
| `template` | `Omit<EmailOptions, 'to'>` | Email template that will be applied to each recipient. All fields except `to` are reused. |

---

## Return Values

### `sendEmail`

| Property | Type | Description |
|----------|------|-------------|
| `success` | `boolean` | `true` if the email was sent successfully. |
| `messageId` | `string` | **Optional.** Unique identifier returned by the provider. Present only when `success` is `true`. |
| `error` | `string` | **Optional.** Error message if the send failed. Present only when `success` is `false`. |

### `sendBulkEmails`

Returns an array of `EmailResult` objects, one per recipient, preserving the order of the `recipients` array. Each element follows the same structure as the result of `sendEmail`.

---

## Extending the Provider

The module currently uses a stub `sendViaProvider` that simply returns a fake message ID.  
To integrate with a real provider:

```ts
async function sendViaProvider(options: EmailOptions): Promise<string> {
  // Example with SendGrid
  const sgMail = require('@sendgrid/mail');
  sgMail.setApiKey(process.env.SENDGRID_API_KEY);

  const msg = {
    to: options.to,
    cc: options.cc,
    bcc: options.bcc,
    from: 'no-reply@example.com',
    subject: options.subject,
    text: options.body,
    html: options.html,
    attachments: options.attachments?.map(att => ({
      content: att.content instanceof Buffer ? att.content.toString('base64') : Buffer.from(att.content).toString('base64'),
      filename: att.filename,
      type: att.contentType,
      disposition: 'attachment',
      contentId: att.filename,
    })),
  };

  const response = await sgMail.send(msg);
  return response[0].headers['x-message-id'];
}
```

Replace the stub with the above implementation (or any other provider) and the rest of the module will work unchanged.