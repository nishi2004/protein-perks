"""
Payment Service - Razorpay integration for payment processing.
Handles order creation and payment verification.
"""
import razorpay
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Razorpay client
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "")

# Only initialize if keys are available
razorpay_client = None
if RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET:
    razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


def create_razorpay_order(amount: float, currency: str = "INR", receipt: str = None) -> dict:
    """
    Create a Razorpay order for payment.
    
    Args:
        amount: Order amount in rupees (will be converted to paise)
        currency: Currency code (default: INR)
        receipt: Receipt ID for reference
    
    Returns:
        Dict with order details including order_id
    
    Raises:
        Exception if Razorpay client not initialized or order creation fails
    """
    if not razorpay_client:
        raise Exception("Razorpay credentials not configured. Please add RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET to .env file")
    
    # Convert amount to paise (Razorpay uses smallest currency unit)
    amount_in_paise = int(amount * 100)
    
    order_data = {
        "amount": amount_in_paise,
        "currency": currency,
        "receipt": receipt or f"order_{int(amount)}",
        "payment_capture": 1  # Auto capture payment
    }
    
    try:
        order = razorpay_client.order.create(data=order_data)
        return order
    except Exception as e:
        raise Exception(f"Failed to create Razorpay order: {str(e)}")


def verify_payment_signature(order_id: str, payment_id: str, signature: str) -> bool:
    """
    Verify Razorpay payment signature for security.
    
    Args:
        order_id: Razorpay order ID
        payment_id: Razorpay payment ID
        signature: Payment signature from Razorpay
    
    Returns:
        True if signature is valid, False otherwise
    """
    if not razorpay_client:
        return False
    
    try:
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        
        # This will raise SignatureVerificationError if invalid
        razorpay_client.utility.verify_payment_signature(params_dict)
        return True
    except razorpay.errors.SignatureVerificationError:
        return False
    except Exception as e:
        print(f"Payment verification error: {str(e)}")
        return False


def get_razorpay_key_id() -> str:
    """
    Get Razorpay Key ID for frontend integration.
    
    Returns:
        Razorpay Key ID
    """
    return RAZORPAY_KEY_ID
