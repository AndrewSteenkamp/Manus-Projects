# South African Payment Integration Research

## Payment Gateway Options

### 1. PayFast (Recommended)
- **Most Popular**: South Africa's leading payment gateway
- **Integration Methods**:
  - Custom Integration (Form POST)
  - API Integration
  - Onsite Payments (no redirect)
  - Recurring Billing
- **Payment Methods**: All major credit cards, mobile wallets, QR codes
- **Fees**: Competitive SA rates
- **Documentation**: https://developers.payfast.co.za/

**Key Integration Requirements:**
- Merchant ID
- Merchant Key
- Security signature (MD5 hash with passphrase)
- Notify URL for ITN (Instant Transaction Notifications)
- Return/Cancel URLs

### 2. Peach Payments
- **Enterprise-Grade**: Payment orchestration platform
- **Features**: Multiple payment methods, APIs for custom integration
- **Good For**: Larger businesses, complex payment flows
- **Documentation**: https://developer.peachpayments.com/

### 3. FNB Business Banking
- **Direct Banking Integration**: FNB offers API and Host-to-Host services
- **Use Case**: Direct bank account integration, reconciliation
- **Benefits**: Minimal human intervention, automated processes
- **Link**: https://www.fnb.co.za/integration-channel/

## Recommended Approach for User

**Phase 1: Immediate (Low Cost)**
- Use PayFast for client payments
- Simple form integration (no monthly fees, just transaction fees)
- Can start accepting payments within 24 hours of account approval

**Phase 2: Scale**
- Integrate FNB APIs for automated reconciliation
- Add Peach Payments for international clients
- Implement recurring billing for subscription services

## Implementation Priority
1. ✅ PayFast custom integration (immediate revenue)
2. FNB business account setup (user will handle)
3. Automated payment tracking in CFO agent
4. Invoice generation with payment links
