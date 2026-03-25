import crypto from 'crypto';
import { PaymentProcessor, PaymentRequest, PaymentResponse } from './index';

export interface PayFastConfig {
  merchantId: string;
  merchantKey: string;
  passphrase: string;
  sandbox?: boolean;
}

export class PayFastProcessor implements PaymentProcessor {
  private config: PayFastConfig;

  constructor(config: PayFastConfig) {
    this.config = config;
  }

  async createPayment(request: PaymentRequest): Promise<PaymentResponse> {
    const baseUrl = this.config.sandbox
      ? 'https://sandbox.payfast.co.za/eng/process'
      : 'https://www.payfast.co.za/eng/process';

    // Build payment data
    const paymentData: Record<string, string> = {
      merchant_id: this.config.merchantId,
      merchant_key: this.config.merchantKey,
      return_url: request.returnUrl,
      cancel_url: request.cancelUrl,
      notify_url: request.notifyUrl,
      m_payment_id: request.orderId.toString(),
      amount: request.amount.toFixed(2),
      item_name: request.itemName,
      item_description: request.itemDescription || '',
    };

    // Add customer details if provided
    if (request.customerEmail) {
      paymentData.email_address = request.customerEmail;
    }
    if (request.customerName) {
      const nameParts = request.customerName.split(' ');
      paymentData.name_first = nameParts[0] || '';
      paymentData.name_last = nameParts.slice(1).join(' ') || '';
    }

    // Generate signature
    const signature = this.generateSignature(paymentData);
    paymentData.signature = signature;

    return {
      success: true,
      redirectUrl: baseUrl,
      formData: paymentData,
    };
  }

  async verifyWebhook(data: Record<string, any>): Promise<boolean> {
    const receivedSignature = data.signature;
    delete data.signature;

    const calculatedSignature = this.generateSignature(data);
    return receivedSignature === calculatedSignature;
  }

  async handleWebhook(data: Record<string, any>): Promise<{
    orderId: number;
    status: 'completed' | 'failed' | 'pending' | 'cancelled';
    processorPaymentId: string;
    amount: number;
  }> {
    const paymentStatus = data.payment_status?.toUpperCase();
    
    let status: 'completed' | 'failed' | 'pending' | 'cancelled';
    switch (paymentStatus) {
      case 'COMPLETE':
        status = 'completed';
        break;
      case 'FAILED':
        status = 'failed';
        break;
      case 'PENDING':
        status = 'pending';
        break;
      case 'CANCELLED':
        status = 'cancelled';
        break;
      default:
        status = 'pending';
    }

    return {
      orderId: parseInt(data.m_payment_id),
      status,
      processorPaymentId: data.pf_payment_id,
      amount: parseFloat(data.amount_gross),
    };
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
    const stringToHash = this.config.passphrase
      ? `${paramString}&passphrase=${encodeURIComponent(this.config.passphrase).replace(/%20/g, '+')}`
      : paramString;

    // Generate MD5 hash
    return crypto.createHash('md5').update(stringToHash).digest('hex');
  }
}

export function createPayFastProcessor(config: PayFastConfig): PayFastProcessor {
  return new PayFastProcessor(config);
}
