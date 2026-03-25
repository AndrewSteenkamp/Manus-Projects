# PayFast Integration Notes

## Key Information from Documentation

### Payment Flow
1. Customer submits checkout form
2. Form redirects to PayFast (https://www.payfast.co.za/eng/process for live, https://sandbox.payfast.co.za/eng/process for sandbox)
3. Customer completes payment on PayFast
4. PayFast sends ITN (Instant Transaction Notification) to notify_url
5. Customer redirected to return_url (success) or cancel_url (cancelled)

### Required Fields
- `merchant_id`: 8 character merchant ID from PayFast account
- `merchant_key`: Merchant key from PayFast account  
- `amount`: Amount in ZAR (decimal)
- `item_name`: Product/order name
- `signature`: MD5 hash for security

### Optional But Important Fields
- `return_url`: Where to redirect after successful payment
- `cancel_url`: Where to redirect if payment cancelled
- `notify_url`: Webhook URL for ITN (Instant Transaction Notification)
- `m_payment_id`: Our internal order/payment ID
- `email_address`: Customer email
- `name_first`, `name_last`: Customer name

### Security Signature Generation
1. Concatenate all non-blank form fields as `name=value&name=value`
2. Order fields as they appear in the documentation
3. URL encode the string
4. Append passphrase if configured
5. Generate MD5 hash

### ITN (Webhook) Response Fields
- `m_payment_id`: Our payment ID (echoed back)
- `pf_payment_id`: PayFast payment ID
- `payment_status`: COMPLETE, FAILED, PENDING, CANCELLED
- `amount_gross`: Total amount
- `amount_fee`: PayFast fee
- `amount_net`: Net amount after fees
- `signature`: Security signature to verify

### Testing
- Sandbox URL: https://sandbox.payfast.co.za/eng/process
- Create sandbox account at https://sandbox.payfast.co.za
- Test cards and accounts provided in sandbox

### Payment Methods Supported
- EFT (ef)
- Credit card (cc)
- Debit card (dc)
- Masterpass (mp)
- Mobicred (mc)
- SnapScan (ss)
- Zapper (zp)
- Apple Pay (ap)
- Google Pay (gp)
- Capitec Pay (cp)
- And more...

## Implementation Plan
1. Add PayFast processor implementation in server/payments/payfast.ts
2. Generate payment form with signature
3. Redirect customer to PayFast
4. Handle ITN webhook at /api/payments/payfast/webhook
5. Verify signature and update payment status
6. Redirect customer back to success/cancel page
