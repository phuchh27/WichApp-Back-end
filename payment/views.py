from django.shortcuts import render

# Create your views here.
# payment/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe

from stores.models import Store
from authentication.models import User

stripe.api_key = "YOUR_STRIPE_SECRET_KEY"

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    if event.type == "checkout.session.completed":
        session = event.data.object
        user = User.objects.get(email=session.customer_email)
        
        # Create the store for the user and save payment_id
        store = Store.objects.create(user=user, payment_id=session.id)
        store.save()

    return JsonResponse({"status": "success"})
