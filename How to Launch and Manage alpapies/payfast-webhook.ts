import { Request, Response } from 'express';
import { getPaymentProcessor } from '../payments/index';
import { updatePaymentStatus } from '../db';

/**
 * PayFast ITN (Instant Transaction Notification) webhook handler
 * This endpoint receives payment notifications from PayFast
 */
export async function handlePayFastWebhook(req: Request, res: Response) {
  try {
    console.log('[PayFast Webhook] Received notification:', req.body);

    const payload = req.body;
    const signature = payload.signature;

    if (!signature) {
      console.error('[PayFast Webhook] Missing signature');
      return res.status(400).send('Missing signature');
    }

    // Get PayFast processor
    const processor = getPaymentProcessor('payfast');

    // Verify webhook signature
    let webhookEvent;
    try {
      webhookEvent = await processor.verifyWebhook(payload, signature);
    } catch (error) {
      console.error('[PayFast Webhook] Signature verification failed:', error);
      return res.status(400).send('Invalid signature');
    }

    console.log('[PayFast Webhook] Verified event:', webhookEvent);

    // Update payment status in database
    const orderId = parseInt(webhookEvent.orderId);
    const paymentStatus = webhookEvent.type === 'payment.success' ? 'completed' 
      : webhookEvent.type === 'payment.failed' ? 'failed' 
      : 'pending';

    await updatePaymentStatus(orderId, paymentStatus, webhookEvent.paymentId);

    console.log(`[PayFast Webhook] Updated order ${orderId} to status: ${paymentStatus}`);

    // Respond to PayFast
    res.status(200).send('OK');
  } catch (error) {
    console.error('[PayFast Webhook] Error processing webhook:', error);
    res.status(500).send('Internal server error');
  }
}
