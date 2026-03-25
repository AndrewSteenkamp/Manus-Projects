# 💰 Siener AI - Yoco Payment Integration Guide

**This guide replaces the Stripe section in the main deployment guide.**

---

## 🎯 Yoco Integration Overview

Yoco is a leading South African payment gateway, perfect for accepting card payments online. We will use Yoco's API to handle subscription payments for Siener AI.

### **Prerequisites:**
1.  **Yoco Account:** You must have a verified Yoco Business Account.
2.  **API Keys:** Get your **Secret Key** (`sk_...`) and **Public Key** (`pk_...`) from your Yoco Dashboard.

---

## 🛠️ PHASE 1: CODE ADJUSTMENTS (Yoco Integration)

### **Step 1.1: Update Dependencies**

Ensure your `requirements.txt` file includes the necessary libraries (this was already done):
```
flask
flask-cors
requests
python-dotenv
gunicorn
```
*Note: Yoco does not have an official Python SDK, so we will use the `requests` library to interact with their REST API.*

### **Step 1.2: Update Environment Variables**

In your `.env` file (on your server at `/var/www/siener-ai/config/.env`), ensure you have the following Yoco keys:

```
# Yoco Payment Gateway
YOCO_SECRET_KEY=sk_test_your-yoco-secret-key
YOCO_PUBLIC_KEY=pk_test_your-yoco-public-key
YOCO_WEBHOOK_SECRET=your-webhook-secret
```
*Remember to use your **Live** keys when going into production.*

### **Step 1.3: Backend Logic (app.py)**

The main change is in the backend logic to handle Yoco's tokenization and charge process.

**A. Payment Endpoint (`/api/yoco/charge`)**

Replace the existing Stripe charge logic with the following Yoco logic in your `app.py` file:

```python
import requests
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), 'config', '.env'))

YOCO_SECRET_KEY = os.getenv('YOCO_SECRET_KEY')
YOCO_CHARGE_URL = "https://online.yoco.com/v1/charges"

@app.route('/api/yoco/charge', methods=['POST'])
def yoco_charge():
    data = request.get_json()
    token = data.get('token')
    amount = data.get('amount') # Amount in cents (e.g., R499.00 -> 49900)
    currency = data.get('currency', 'ZAR')
    metadata = data.get('metadata', {})
    
    if not token or not amount:
        return jsonify({"success": False, "message": "Missing token or amount"}), 400

    headers = {
        "Authorization": f"Bearer {YOCO_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "token": token,
        "amountInCents": amount,
        "currency": currency,
        "metadata": metadata,
        "statementDescriptor": "Siener AI Subscription"
    }

    try:
        response = requests.post(YOCO_CHARGE_URL, headers=headers, json=payload)
        yoco_response = response.json()

        if response.status_code == 200 and yoco_response.get('status') == 'successful':
            # Update user subscription status in your database here
            user_id = metadata.get('user_id')
            # update_subscription_status(user_id, 'active', amount) 
            
            return jsonify({"success": True, "message": "Payment successful", "data": yoco_response})
        else:
            error_message = yoco_response.get('message', 'Payment failed')
            return jsonify({"success": False, "message": error_message, "data": yoco_response}), 400

    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500

```

**B. Webhook Endpoint (`/api/yoco/webhook`)**

Yoco webhooks are crucial for handling subscription renewals and failures.

```python
@app.route('/api/yoco/webhook', methods=['POST'])
def yoco_webhook():
    # Yoco webhook logic here
    data = request.get_json()
    event_type = data.get('event')
    
    # Verify webhook signature (Crucial for security)
    # Yoco recommends verifying the signature header
    
    if event_type == 'charge.succeeded':
        # Handle successful charge (e.g., subscription renewal)
        charge_id = data['data']['id']
        user_id = data['data']['metadata'].get('user_id')
        # update_subscription_renewal(user_id, charge_id)
        
    elif event_type == 'charge.failed':
        # Handle failed charge (e.g., subscription cancellation)
        user_id = data['data']['metadata'].get('user_id')
        # cancel_subscription(user_id)
        
    return jsonify({"status": "received"}), 200
```

---

## 💻 PHASE 2: FRONTEND ADJUSTMENTS (Yoco Pop-up)

The frontend needs to use the Yoco Pop-up SDK to securely collect card details.

### **Step 2.1: Add Yoco SDK to HTML**

In your main HTML file (e.g., `index.html` or the main template), add the Yoco SDK script:

```html
<!-- Yoco SDK Script -->
<script src="https://js.yoco.com/sdk/v1/yoco-sdk-web.js"></script>
```

### **Step 2.2: Implement Yoco Pop-up**

In your JavaScript/React component for the payment page, implement the Yoco Pop-up:

```javascript
// Get your public key from the environment variables (YOCO_PUBLIC_KEY)
const YOCO_PUBLIC_KEY = "pk_test_your-yoco-public-key"; 

// Initialize Yoco Pop-up
const yoco = new YocoSDK({
    publicKey: YOCO_PUBLIC_KEY,
});

function openYocoPayment(planAmountInCents, planName, userId) {
    yoco.showPopup({
        amountInCents: planAmountInCents,
        currency: 'ZAR',
        name: 'Siener AI Subscription',
        description: planName,
        callback: function (result) {
            if (result.error) {
                alert("Payment failed: " + result.error.message);
            } else {
                // Send the token to your backend for charging
                const token = result.id;
                
                fetch('/api/yoco/charge', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        token: token,
                        amount: planAmountInCents,
                        metadata: { user_id: userId, plan: planName }
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert("Subscription successful! Welcome to Siener AI.");
                        // Redirect to dashboard
                    } else {
                        alert("Payment processing failed on server: " + data.message);
                    }
                });
            }
        }
    });
}

// Example usage when user clicks a plan button
// openYocoPayment(49900, 'Professional Plan', 'user-123'); 
```

---

## 🚀 PHASE 3: DEPLOYMENT ADJUSTMENTS

### **Step 3.1: Rebuild and Redeploy**

1.  **Rebuild:** After making the code changes, rebuild your application.
2.  **Redeploy:** Follow the deployment guide (Phase 2) to push the updated code to your server.

### **Step 3.2: Configure Yoco Webhook**

1.  **Get Webhook URL:** Your webhook URL will be `https://your_domain.co.za/api/yoco/webhook`.
2.  **Yoco Dashboard:** Go to your Yoco Dashboard -> Settings -> Webhooks.
3.  **Add Endpoint:** Add your webhook URL and select the events you want to receive (e.g., `charge.succeeded`, `charge.failed`, `subscription.created`).
4.  **Get Webhook Secret:** Copy the provided Webhook Secret and update your server's `.env` file.

### **Step 3.3: Final Testing**

1.  **Test Payment:** Use a Yoco test card to ensure the entire flow (frontend pop-up -> backend charge -> database update) works.
2.  **Test Webhook:** Manually trigger a test webhook from the Yoco Dashboard to ensure your server receives and processes it correctly.

---

## 🏆 Conclusion

By implementing these changes, your Siener AI system will be fully integrated with **Yoco**, providing a reliable and familiar payment experience for your South African customers. This is a critical step for your local launch!
