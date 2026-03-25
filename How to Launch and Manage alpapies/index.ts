/**
 * Flexible Payment System
 * Supports multiple payment processors: Stripe, PayFast, Paystack, PayPal
 */

export interface PaymentProcessor {
  name: string;
  createPayment(params: CreatePaymentParams): Promise<PaymentResult>;
  verifyWebhook(payload: any, signature: string): Promise<WebhookEvent>;
  getPaymentStatus(paymentId: string): Promise<PaymentStatus>;
}

export interface CreatePaymentParams {
  amount: number; // in cents
  currency: string;
  orderId: string;
  customerEmail: string;
  customerName: string;
  returnUrl: string;
  cancelUrl: string;
  items: Array<{
    name: string;
    quantity: number;
    price: number;
  }>;
}

export interface PaymentResult {
  success: boolean;
  paymentUrl?: string;
  paymentId?: string;
  error?: string;
}

export interface WebhookEvent {
  type: 'payment.success' | 'payment.failed' | 'payment.pending';
  paymentId: string;
  orderId: string;
  amount: number;
  currency: string;
  customerEmail: string;
  metadata?: Record<string, any>;
}

export interface PaymentStatus {
  status: 'pending' | 'completed' | 'failed' | 'cancelled';
  paymentId: string;
  amount: number;
  currency: string;
}

export type PaymentProcessorType = 'stripe' | 'payfast' | 'paystack' | 'paypal';

/**
 * Payment processor factory
 */
export function getPaymentProcessor(type: PaymentProcessorType): PaymentProcessor {
  switch (type) {
    case 'stripe':
      return new StripeProcessor();
    case 'payfast':
      return new PayFastProcessor();
    case 'paystack':
      return new PaystackProcessor();
    case 'paypal':
      return new PayPalProcessor();
    default:
      throw new Error(`Unknown payment processor: ${type}`);
  }
}

// Stripe Processor
class StripeProcessor implements PaymentProcessor {
  name = 'Stripe';

  async createPayment(params: CreatePaymentParams): Promise<PaymentResult> {
    // Stripe implementation will be added when user provides API keys
    return {
      success: false,
      error: 'Stripe not configured. Please add API keys in Settings → Payment',
    };
  }

  async verifyWebhook(payload: any, signature: string): Promise<WebhookEvent> {
    throw new Error('Stripe not configured');
  }

  async getPaymentStatus(paymentId: string): Promise<PaymentStatus> {
    throw new Error('Stripe not configured');
  }
}

// PayFast Processor (South Africa)
class PayFastProcessor implements PaymentProcessor {
  name = 'PayFast';
  private merchantId: string;
  private merchantKey: string;
  private passphrase: string;
  private sandbox: boolean;

  constructor() {
    // These will be loaded from environment variables
    this.merchantId = process.env.PAYFAST_MERCHANT_ID || '';
    this.merchantKey = process.env.PAYFAST_MERCHANT_KEY || '';
    this.passphrase = process.env.PAYFAST_PASSPHRASE || '';
    this.sandbox = process.env.NODE_ENV !== 'production';
  }

  async createPayment(params: CreatePaymentParams): Promise<PaymentResult> {
    if (!this.merchantId || !this.merchantKey) {
      return {
        success: false,
        error: 'PayFast not configured. Please add credentials in Settings → Payment',
      };
    }

    const baseUrl = this.sandbox
      ? 'https://sandbox.payfast.co.za/eng/process'
      : 'https://www.payfast.co.za/eng/process';

    // Build payment data
    const paymentData: Record<string, string> = {
      merchant_id: this.merchantId,
      merchant_key: this.merchantKey,
      return_url: params.returnUrl,
      cancel_url: params.cancelUrl,
      notify_url: `${params.returnUrl.split('/').slice(0, 3).join('/')}/api/payments/payfast/webhook`,
      m_payment_id: params.orderId,
      amount: (params.amount / 100).toFixed(2), // Convert cents to ZAR
      item_name: params.items.map(i => i.name).join(', ') || 'Order',
      item_description: `Order #${params.orderId}`,
      email_address: params.customerEmail,
    };

    // Add customer name
    const nameParts = params.customerName.split(' ');
    paymentData.name_first = nameParts[0] || '';
    paymentData.name_last = nameParts.slice(1).join(' ') || '';

    // Generate signature
    const signature = this.generateSignature(paymentData);

    // Build form HTML for redirect
    const formFields = Object.entries({ ...paymentData, signature })
      .map(([key, value]) => `<input type="hidden" name="${key}" value="${value}" />`)
      .join('\n');

    const formHtml = `
      <form id="payfast_form" action="${baseUrl}" method="post">
        ${formFields}
      </form>
      <script>document.getElementById('payfast_form').submit();</script>
    `;

    return {
      success: true,
      paymentUrl: baseUrl,
      paymentId: params.orderId,
      error: undefined,
    };
  }

  async verifyWebhook(payload: any, signature: string): Promise<WebhookEvent> {
    const calculatedSignature = this.generateSignature(payload);
    
    if (calculatedSignature !== signature) {
      throw new Error('Invalid webhook signature');
    }

    const paymentStatus = payload.payment_status?.toUpperCase();
    let type: 'payment.success' | 'payment.failed' | 'payment.pending';
    
    switch (paymentStatus) {
      case 'COMPLETE':
        type = 'payment.success';
        break;
      case 'FAILED':
      case 'CANCELLED':
        type = 'payment.failed';
        break;
      default:
        type = 'payment.pending';
    }

    return {
      type,
      paymentId: payload.pf_payment_id,
      orderId: payload.m_payment_id,
      amount: parseFloat(payload.amount_gross) * 100, // Convert to cents
      currency: 'ZAR',
      customerEmail: payload.email_address,
      metadata: {
        pfPaymentId: payload.pf_payment_id,
        amountFee: payload.amount_fee,
        amountNet: payload.amount_net,
      },
    };
  }

  async getPaymentStatus(paymentId: string): Promise<PaymentStatus> {
    // PayFast doesn't have a direct API to check status
    // Status is typically tracked via webhooks
    throw new Error('PayFast status check not implemented. Use webhooks for status updates.');
  }

  private generateSignature(data: Record<string, string>): string {
    // Remove signature field if present
    const signatureData = { ...data };
    delete signatureData.signature;

    // Sort keys and create parameter string
    const paramString = Object.keys(signatureData)
      .sort()
      .map(key => {
        const value = signatureData[key];
        // Skip empty values
        if (value === '' || value === null || value === undefined) {
          return null;
        }
        return `${key}=${encodeURIComponent(value).replace(/%20/g, '+')}`;
      })
      .filter(Boolean)
      .join('&');

    // Add passphrase if configured
    const stringToHash = this.passphrase
      ? `${paramString}&passphrase=${encodeURIComponent(this.passphrase).replace(/%20/g, '+')}`
      : paramString;

    // Generate MD5 hash
    const crypto = require('crypto');
    return crypto.createHash('md5').update(stringToHash).digest('hex');
  }
}

// Paystack Processor
class PaystackProcessor implements PaymentProcessor {
  name = 'Paystack';

  async createPayment(params: CreatePaymentParams): Promise<PaymentResult> {
    // Paystack implementation will be added
    return {
      success: false,
      error: 'Paystack not configured. Please add API key in Settings → Payment',
    };
  }

  async verifyWebhook(payload: any, signature: string): Promise<WebhookEvent> {
    throw new Error('Paystack not configured');
  }

  async getPaymentStatus(paymentId: string): Promise<PaymentStatus> {
    throw new Error('Paystack not configured');
  }
}

// PayPal Processor
class PayPalProcessor implements PaymentProcessor {
  name = 'PayPal';

  async createPayment(params: CreatePaymentParams): Promise<PaymentResult> {
    // PayPal implementation will be added
    return {
      success: false,
      error: 'PayPal not configured. Please add credentials in Settings → Payment',
    };
  }

  async verifyWebhook(payload: any, signature: string): Promise<WebhookEvent> {
    throw new Error('PayPal not configured');
  }

  async getPaymentStatus(paymentId: string): Promise<PaymentStatus> {
    throw new Error('PayPal not configured');
  }
}
