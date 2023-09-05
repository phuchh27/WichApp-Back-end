import stripe
from .models import PaymentSession

def create_payment_session(user):
    # Create a Stripe Payment Session and return the payment link
    # You can customize the payment session as needed
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        customer_email=user.email,
        line_items=[{
            "price": "price_1NkoKbIwb6jW5a5oAO45uXtP",
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://localhost:4200/ohome/store?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url="http://localhost:4200/payment",
    )
    # payment_intent_id = session.payment_intent
    # Save the payment session data in your database for future reference
    PaymentSession.objects.create(user=user, session_id=session.id)
    
    return session.url

#create function verify session_id and user from data base with session_id and user request if have session_id return true if not return false.

def verify_payment_session(session_id, user):
    # Verify the payment session
    # You can customize the payment session as needed
    session = stripe.checkout.Session.retrieve(session_id)
    if session.customer_email == user.email:
        return True
    else:
        return False



    
    
