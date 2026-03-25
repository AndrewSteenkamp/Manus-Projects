# Payment Setup Guide
**How to Accept Real Payments (For Complete Beginners)**

This guide explains how to set up payment processing so customers can pay you with credit cards, bank transfers, and other methods.

---

## Why You Need Payment Processing

Right now, your website can:
- ✅ Show products
- ✅ Let customers add to cart
- ✅ Let customers checkout
- ❌ **Cannot accept real money**

To accept real payments, you need a **payment processor** - a company that handles the money transfer securely.

---

## Recommended Payment Processor: PayFast

### Why PayFast?
- ✅ **Made for South Africa** - Works with South African banks
- ✅ **Accepts all payment methods**:
  - Credit/Debit cards (Visa, Mastercard)
  - Instant EFT (bank transfer)
  - SnapScan
  - Zapper
  - Masterpass
- ✅ **Easy setup** - No technical knowledge needed
- ✅ **Reasonable fees** - 2.9% + R2.00 per transaction
- ✅ **Fast payouts** - Money in your bank within 2-3 days

### PayFast Fees Example:
```
Customer pays: R500.00
PayFast fee: R16.50 (2.9% + R2.00)
You receive: R483.50
```

---

## Setting Up PayFast (Step-by-Step)

### Step 1: Create PayFast Account

1. **Go to**: https://www.payfast.co.za
2. **Click**: "Sign Up" or "Get Started"
3. **Choose**: "Merchant Account" (not Personal)
4. **Fill in your details**:
   - Business name: Alpapies (or Elpapies)
   - Your name: Andrew Steenkamp
   - Email: ahsteenkamp@gmail.com
   - Phone: Your phone number
   - Business type: E-commerce / Online Store

### Step 2: Verify Your Identity

PayFast will ask for:
- **ID document** (South African ID or passport)
- **Proof of address** (utility bill, bank statement)
- **Bank account details** (where they'll pay you)

**Why?** This is required by law to prevent fraud.

### Step 3: Get Your API Keys

Once approved (usually 1-2 business days):

1. Log into PayFast dashboard
2. Go to "Settings" → "Integration"
3. You'll see:
   - **Merchant ID**: (e.g., 10012345)
   - **Merchant Key**: (e.g., a1b2c3d4e5f6)
   - **Passphrase**: (create a secure password)

**Important**: Keep these secret! Don't share them with anyone.

### Step 4: Give Me Your API Keys

Once you have them:
1. Tell me: "I have my PayFast keys"
2. I'll ask you to enter them securely
3. I'll integrate PayFast into your website
4. Takes about 5 minutes!

### Step 5: Test Payments

Before going live:
1. PayFast provides a "Sandbox" (test mode)
2. We'll test with fake credit cards
3. Make sure everything works
4. No real money involved

### Step 6: Go Live!

Once testing is done:
1. Switch from Sandbox to Live mode
2. Your website can now accept real payments!
3. Customers can pay with any method

---

## Alternative: Stripe (International Option)

### Why Stripe?
- ✅ **Global reach** - Accept payments from anywhere
- ✅ **More features** - Subscriptions, invoicing, etc.
- ✅ **Professional** - Used by major companies
- ❌ **Harder to set up in South Africa**
- ❌ **May need international bank account**

### Stripe Fees:
```
Customer pays: R500.00
Stripe fee: R17.00 (2.9% + R2.00) + currency conversion
You receive: ~R480.00
```

### When to Use Stripe:
- If you want to sell internationally
- If you plan to expand beyond South Africa
- If you need advanced features

### Setting Up Stripe:
1. Go to: https://stripe.com
2. Create account
3. Verify identity (may take longer for SA)
4. Get API keys
5. Give them to me
6. I'll integrate it

---

## Comparing Payment Options

| Feature | PayFast | Stripe |
|---------|---------|--------|
| **Best for** | South African customers | International customers |
| **Setup difficulty** | Easy | Medium |
| **Approval time** | 1-2 days | 3-7 days (SA) |
| **Fees** | 2.9% + R2 | 2.9% + R2 + FX |
| **Payment methods** | SA methods | Global cards |
| **Payout time** | 2-3 days | 7 days |
| **Support** | Local (SA) | International |

**My Recommendation**: Start with PayFast, add Stripe later if needed.

---

## What Happens After Setup

### Customer Experience:
1. Customer adds products to cart
2. Goes to checkout
3. Fills in shipping information
4. Clicks "Proceed to Payment"
5. **Redirected to PayFast payment page**
6. Chooses payment method (card, EFT, etc.)
7. Completes payment
8. **Redirected back to your site**
9. Sees "Order Confirmed" page
10. Receives confirmation email

### Your Experience:
1. Customer completes payment
2. **You get email notification**
3. Order appears in your admin dashboard
4. Status: "Paid" (not "Pending")
5. You forward order to ZQ Dropshipping
6. Money appears in your PayFast account
7. PayFast pays you (2-3 days later)
8. Money arrives in your bank account

---

## Security & Safety

### Is It Safe?
- ✅ **Yes!** PayFast is PCI-DSS compliant
- ✅ Customer card details never touch your website
- ✅ All payments encrypted
- ✅ Fraud protection included

### You Never See:
- Credit card numbers
- CVV codes
- Banking passwords

### You Only See:
- Order amount
- Customer name
- Payment status (paid/failed)

---

## Handling Failed Payments

### Why Payments Fail:
- Insufficient funds
- Expired card
- Incorrect details
- Bank declined

### What Happens:
1. Customer sees "Payment Failed" message
2. They can try again with different card/method
3. Order stays in cart
4. No order is created until payment succeeds

### What You Do:
- Nothing! System handles it automatically
- Customer can retry as many times as needed

---

## Refunds & Cancellations

### How to Issue a Refund:

**Via PayFast Dashboard:**
1. Log into PayFast
2. Go to "Transactions"
3. Find the payment
4. Click "Refund"
5. Enter amount (full or partial)
6. Confirm

**Money returns to customer's card/account within 5-7 days**

### Refund Fees:
- PayFast doesn't refund their fee
- Example: Customer paid R500, you refund R500, but you still paid R16.50 fee

---

## Monthly Statements

### PayFast Provides:
- Transaction reports
- Fee summaries
- Payout history
- Downloadable CSV files

### What to Track:
```
Month: January 2026
Total Sales: R25,000
PayFast Fees: R750
Net Revenue: R24,250
Number of Transactions: 47
Average Order: R531.91
```

---

## Common Questions

**Q: How long does PayFast approval take?**
A: Usually 1-2 business days. Can be faster if all documents are correct.

**Q: Do I need a registered business?**
A: No! You can use your personal details. But having a business helps.

**Q: What if a customer disputes a payment?**
A: PayFast handles disputes. They'll contact you for proof of delivery. Keep all tracking numbers!

**Q: Can I accept international cards?**
A: Yes! PayFast accepts Visa and Mastercard from anywhere.

**Q: How much does it cost to set up?**
A: R0! No setup fees. You only pay per transaction.

**Q: Can I use multiple payment processors?**
A: Yes! You can have both PayFast AND Stripe. Customer chooses at checkout.

**Q: What if I make a mistake?**
A: Don't worry! Refunds are easy. Just process it through PayFast dashboard.

---

## Next Steps

### Ready to Set Up Payments?

**Option 1: PayFast (Recommended)**
1. Go to https://www.payfast.co.za
2. Sign up for merchant account
3. Complete verification
4. Get your API keys
5. Tell me: "I have my PayFast keys ready"
6. I'll integrate it in 5 minutes!

**Option 2: Stripe**
1. Go to https://stripe.com
2. Create account
3. Complete verification (may take longer)
4. Get API keys
5. Tell me: "I have my Stripe keys ready"
6. I'll integrate it!

**Option 3: Both**
1. Set up both accounts
2. Give me both sets of keys
3. Customers can choose which to use
4. Maximum flexibility!

### Not Ready Yet?
That's okay! Your website works fine without payments. You can:
- Continue testing
- Add more products
- Show it to friends/family
- Set up payments when you're ready

---

## Need Help?

### If you're stuck:
- Tell me where you're stuck in the process
- I'll guide you through it step-by-step

### If you have questions:
- Ask me anything about payments
- I'll explain it in simple terms

### If something doesn't work:
- Don't panic!
- Tell me what happened
- I'll fix it immediately

---

**Remember**: You don't need to understand the technical details. Just get your PayFast account set up, give me the keys, and I'll handle the rest!

---

**Next Guide**: [Launch Checklist →](LAUNCH_CHECKLIST.md)
