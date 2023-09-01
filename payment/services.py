import stripe
from .models import PaymentSession

def create_payment_session(user):
    # Create a Stripe Payment Session and return the payment link
    # You can customize the payment session as needed
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        customer_email=user.email,
        line_items=[{
            "price": "YOUR_PRICE_ID",
            "quantity": 1,
        }],
        mode="payment",
        success_url="YOUR_SUCCESS_URL",
        cancel_url="YOUR_CANCEL_URL",
    )
    
    # Save the payment session data in your database for future reference
    PaymentSession.objects.create(user=user, session_id=session.id)
    
    return session.url
    
