/**
 * Yoco Payment Integration for South African Rand payments
 * Handles subscription payments, webhooks, and transaction management
 */

import axios from "axios";

export interface YocoPaymentRequest {
  amount: number; // Amount in cents (ZAR)
  currency: string; // "ZAR"
  description: string;
  metadata?: Record<string, any>;
  successUrl?: string;
  cancelUrl?: string;
  failureUrl?: string;
}

export interface YocoPaymentResponse {
  id: string;
  status: string;
  amount: number;
  currency: string;
  redirectUrl?: string;
  metadata?: Record<string, any>;
}

export interface YocoWebhookPayload {
  type: string;
  payload: {
    id: string;
    status: string;
    amount: number;
    currency: string;
    metadata?: Record<string, any>;
  };
}

/**
 * Initialize Yoco payment for subscription
 */
export async function createYocoPayment(
  request: YocoPaymentRequest,
  apiKey: string
): Promise<YocoPaymentResponse | null> {
  try {
    // Yoco API endpoint for creating payments
    const response = await axios.post(
      "https://payments.yoco.com/api/checkouts",
      {
        amount: request.amount,
        currency: request.currency,
        successUrl: request.successUrl,
        cancelUrl: request.cancelUrl,
        failureUrl: request.failureUrl,
        metadata: request.metadata,
      },
      {
        headers: {
          Authorization: `Bearer ${apiKey}`,
          "Content-Type": "application/json",
        },
      }
    );

    return {
      id: response.data.id,
      status: response.data.status,
      amount: response.data.amount,
      currency: response.data.currency,
      redirectUrl: response.data.redirectUrl,
      metadata: response.data.metadata,
    };
  } catch (error: any) {
    console.error("[Yoco] Payment creation failed:", error.response?.data || error.message);
    return null;
  }
}

/**
 * Verify Yoco webhook signature
 */
export function verifyYocoWebhook(payload: string, signature: string, secret: string): boolean {
  // Yoco uses HMAC SHA256 for webhook verification
  const crypto = require("crypto");
  const hmac = crypto.createHmac("sha256", secret);
  hmac.update(payload);
  const calculatedSignature = hmac.digest("hex");

  return calculatedSignature === signature;
}

/**
 * Process Yoco webhook event
 */
export function processYocoWebhook(payload: YocoWebhookPayload): {
  paymentId: string;
  status: "completed" | "failed" | "pending";
  amount: number;
  metadata?: Record<string, any>;
} {
  const { type, payload: eventPayload } = payload;

  let status: "completed" | "failed" | "pending" = "pending";

  switch (type) {
    case "payment.succeeded":
      status = "completed";
      break;
    case "payment.failed":
      status = "failed";
      break;
    case "payment.pending":
      status = "pending";
      break;
    default:
      console.warn(`[Yoco] Unknown webhook type: ${type}`);
  }

  return {
    paymentId: eventPayload.id,
    status,
    amount: eventPayload.amount,
    metadata: eventPayload.metadata,
  };
}

/**
 * Get Yoco payment status
 */
export async function getYocoPaymentStatus(paymentId: string, apiKey: string): Promise<string | null> {
  try {
    const response = await axios.get(`https://payments.yoco.com/api/checkouts/${paymentId}`, {
      headers: {
        Authorization: `Bearer ${apiKey}`,
      },
    });

    return response.data.status;
  } catch (error: any) {
    console.error("[Yoco] Failed to get payment status:", error.response?.data || error.message);
    return null;
  }
}

/**
 * Refund Yoco payment
 */
export async function refundYocoPayment(paymentId: string, amount: number, apiKey: string): Promise<boolean> {
  try {
    await axios.post(
      `https://payments.yoco.com/api/refunds`,
      {
        checkoutId: paymentId,
        amount: amount,
      },
      {
        headers: {
          Authorization: `Bearer ${apiKey}`,
          "Content-Type": "application/json",
        },
      }
    );

    return true;
  } catch (error: any) {
    console.error("[Yoco] Refund failed:", error.response?.data || error.message);
    return false;
  }
}

/**
 * Calculate subscription price in cents
 */
export function calculateSubscriptionPrice(planPrice: number): number {
  // Convert Rand to cents (multiply by 100)
  return Math.round(planPrice * 100);
}

/**
 * Generate payment metadata for subscription
 */
export function generatePaymentMetadata(userId: number, planId: number, planName: string) {
  return {
    userId: userId.toString(),
    planId: planId.toString(),
    planName: planName,
    type: "subscription",
    timestamp: new Date().toISOString(),
  };
}
