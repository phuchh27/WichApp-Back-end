import json
from django.shortcuts import render

# Create your views here.
# payment/views.py
from django.http import JsonResponse
from rest_framework.generics import CreateAPIView
from django.views.decorators.csrf import csrf_exempt
import stripe

from stores.models import Store
from authentication.models import User

from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeWebhookViewSet(CreateAPIView):
    def post(self, request, *args, **kwargs):
        payload = request.data
        event = None

        try:
            event = stripe.Event.construct_from(
                json.loads(payload), settings.STRIPE_SECRET_KEY
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
