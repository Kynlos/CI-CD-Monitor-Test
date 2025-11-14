/**
 * Email Service Module
 * Handles sending emails and notifications
 */

export interface EmailOptions {
  to: string[];
  subject: string;
  body: string;
  html?: string;
  cc?: string[];
  bcc?: string[];
  attachments?: Attachment[];
}

export interface Attachment {
  filename: string;
  content: Buffer | string;
  contentType: string;
}

export interface EmailResult {
  success: boolean;
  messageId?: string;
  error?: string;
}

/**
 * Send an email
 * @param options - Email configuration
 * @returns Result of the email send operation
 */
export async function sendEmail(options: EmailOptions): Promise<EmailResult> {
  // Validate recipients
  if (!options.to || options.to.length === 0) {
    return {
      success: false,
      error: 'No recipients specified'
    };
  }

  // Validate email addresses
  const invalidEmails = [...options.to, ...(options.cc || []), ...(options.bcc || [])]
    .filter(email => !isValidEmail(email));
  
  if (invalidEmails.length > 0) {
    return {
      success: false,
      error: `Invalid email addresses: ${invalidEmails.join(', ')}`
    };
  }

  try {
    // Send email via provider
    const messageId = await sendViaProvider(options);
    
    return {
      success: true,
      messageId
    };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error'
    };
  }
}

/**
 * Send bulk emails to multiple recipients
 * @param recipients - Array of recipient email addresses
 * @param template - Email template to use
 * @returns Array of results for each email
 */
export async function sendBulkEmails(
  recipients: string[],
  template: Omit<EmailOptions, 'to'>
): Promise<EmailResult[]> {
  const results: EmailResult[] = [];
  
  for (const recipient of recipients) {
    const result = await sendEmail({
      ...template,
      to: [recipient]
    });
    results.push(result);
  }
  
  return results;
}

// Helper functions
function isValidEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

async function sendViaProvider(options: EmailOptions): Promise<string> {
  // Simulate sending via email provider (SendGrid, Mailgun, etc.)
  return `msg_${Date.now()}`;
}
