from .tasks import send_booking_confirmation_email
from django.db import transaction
import os
import uuid
import json
import requests
from rest_framework import viewsets
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Booking, Payment, Listing
from .serializers import ListingSerializer, BookingSerializer
from dotenv import load_dotenv
load_dotenv()


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save()
        # Queue the email AFTER the transaction commits (avoids race conditions)
        transaction.on_commit(
            lambda: send_booking_confirmation_email.delay(booking.id))


KEY = os.environ.get("CHAPA_SECRET_KEY")
BASE = "https://api.chapa.co/v1"


@csrf_exempt
def initiate_payment(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    if not KEY:
        return JsonResponse({"detail": "CHAPA_SECRET_KEY missing"}, status=500)

    body = json.loads(request.body or "{}")
    booking = get_object_or_404(Booking, id=body.get("booking_id"))
    amount = str(body.get("amount") or booking.listing.price)

    tx_ref = f"booking-{booking.id}-{uuid.uuid4().hex[:8]}"
    return_url = f"{'https' if request.is_secure() else 'http'}://{request.get_host()}{reverse('payments-verify')}?tx_ref={tx_ref}"

    r = requests.post(
        f"{BASE}/transaction/initialize",
        json={
            "amount": amount,
            "currency": "ETB",
            "tx_ref": tx_ref,
            "return_url": return_url,
            "email": "test@example.com",
            "first_name": booking.user,
            "last_name": "Customer",
        },
        headers={"Authorization": f"Bearer {KEY}",
                 "Content-Type": "application/json"},
        timeout=20,
    )
    data = r.json()
    url = (data.get("data") or {}).get("checkout_url")

    Payment.objects.create(booking=booking, amount=amount,
                           tx_ref=tx_ref, checkout_url=url)
    return JsonResponse({"tx_ref": tx_ref, "checkout_url": url}, status=201)


def verify_payment(request):
    if not KEY:
        return JsonResponse({"detail": "CHAPA_SECRET_KEY missing"}, status=500)
    tx_ref = request.GET.get("tx_ref")
    if not tx_ref:
        return JsonResponse({"detail": "tx_ref required"}, status=400)

    payment = get_object_or_404(Payment, tx_ref=tx_ref)
    r = requests.get(f"{BASE}/transaction/verify/{tx_ref}",
                     headers={"Authorization": f"Bearer {KEY}"}, timeout=20)
    j = r.json()
    ok = j.get("status") == "success" and (
        j.get("data") or {}).get("status") == "success"
    payment.status = Payment.STATUS_COMPLETED if ok else Payment.STATUS_FAILED
    payment.save(update_fields=["status"])

    return JsonResponse({"tx_ref": tx_ref, "status": payment.status})
