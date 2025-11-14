# email-service.ts

*Auto-generated from `email-service.ts`*

Email Service Module
====================
## Overview
The Email Service Module is responsible for handling email sending and notifications. It provides a simple and efficient way to send emails to one or multiple recipients.

## Exports
The module exports the following functions, classes, and interfaces:

* `EmailOptions` interface: Configuration options for sending an email
* `Attachment` interface: Represents an email attachment
* `EmailResult` interface: Result of an email send operation
* `sendEmail` function: Sends an email to one or multiple recipients
* `sendBulkEmails` function: Sends bulk emails to multiple recipients using a template

## Usage Examples
### Sending a Single Email
```typescript
import { sendEmail, EmailOptions } from './email-service';

const options: EmailOptions = {
  to: ['recipient@example.com'],
  subject: 'Hello from Email Service',
  body: 'This is a test email',
};

sendEmail(options).then((result) => {
  if (result.success) {
    console.log(`Email sent successfully with message ID: ${result.messageId}`);
  } else {
    console.error(`Error sending email: ${result.error}`);
  }
});
```

### Sending Bulk Emails
```typescript
import { sendBulkEmails } from './email-service';

const recipients = ['recipient1@example.com', 'recipient2@example.com'];
const template = {
  subject: 'Hello from Email Service',
  body: 'This is a test email',
};

sendBulkEmails(recipients, template).then((results) => {
  results.forEach((result, index) => {
    if (result.success) {
      console.log(`Email sent successfully to ${recipients[index]} with message ID: ${result.messageId}`);
    } else {
      console.error(`Error sending email to ${recipients[index]}: ${result.error}`);
    }
  });
});
```

## Parameters
### `EmailOptions` Interface
* `to`: Array of recipient email addresses (required)
* `subject`: Email subject (required)
* `body`: Email body (required)
* `html`: Email HTML content (optional)
* `cc`: Array of CC recipient email addresses (optional)
* `bcc`: Array of BCC recipient email addresses (optional)
* `attachments`: Array of email attachments (optional)

### `Attachment` Interface
* `filename`: Attachment file name (required)
* `content`: Attachment content (required)
* `contentType`: Attachment content type (required)

### `sendEmail` Function
* `options`: `EmailOptions` object (required)

### `sendBulkEmails` Function
* `recipients`: Array of recipient email addresses (required)
* `template`: `EmailOptions` object without `to` property (required)

## Return Values
### `sendEmail` Function
* `EmailResult` object with the following properties:
	+ `success`: Boolean indicating whether the email was sent successfully
	+ `messageId`: Message ID of the sent email (if successful)
	+ `error`: Error message (if failed)

### `sendBulkEmails` Function
* Array of `EmailResult` objects, one for each recipient

### `EmailResult` Interface
* `success`: Boolean indicating whether the email was sent successfully
* `messageId`: Message ID of the sent email (if successful)
* `error`: Error message (if failed)