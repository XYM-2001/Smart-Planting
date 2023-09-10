from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import JsonResponse
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import os
from django.contrib.auth.decorators import login_required
from authentication.models import User
# Create your views here.


stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    user = request.user
    user = get_object_or_404(User, pk=request.session['user_id'])
    #total = str(user.get_cart_totalprice())
    #total = total.replace('.','')
    #total = int(total)
    total = 1000
    #Here is just for smart curtains
    #total = request.GET.get('total')
    #Here is just for smart curtains
    if (request.GET.get('total')):
        total = request.GET.get('total')
    
    # Create a PaymentIntent for Card Payment with dummy amount and currency
    card_payment_intent = stripe.PaymentIntent.create(
        amount=total,
        currency="usd",
        payment_method_types=["card", "alipay", "wechat_pay"],
    )
    request.session['ongoing_amount'] = total
    return render(request, "main/checkout.html", {
        "client_secret": card_payment_intent.client_secret,
        "amount": total
    })


@csrf_exempt
@require_http_methods(["POST"])
def create_wechat_pay_payment_intent(request):
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = request.user
            #total = str(user.get_cart_totalprice())
            #total = total.replace('.','')
            #total = int(total)
            total = 1000

            # Create a PaymentIntent for WeChat Pay with dummy amount and currency
            wechat_payment_intent = stripe.PaymentIntent.create(
                amount=total,
                currency="usd",
                payment_method_types=["wechat_pay"],
                shipping={
                    'name': data['name'],
                    'address': {
                        'line1': data['address']['line1'],
                        'line2': data['address']['line2'],
                        'state': data['address']['state'],
                        'postal_code': data['address']['postal_code'],
                        'country': data['address']['country'],
                    },
                },
            )

            return JsonResponse({
                "client_secret": wechat_payment_intent.client_secret
            })

        except Exception as e:
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Invalid request method"})


@csrf_exempt
@require_http_methods(["POST"])
def create_alipay_payment_intent(request):
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = request.user
            #total = str(user.get_cart_totalprice())
            #total = total.replace('.','')
            #total = int(total)
            total = 1000

            # Create a PaymentIntent for Alipay with dummy amount and currency
            alipay_payment_intent = stripe.PaymentIntent.create(
                amount=total,
                currency="usd",
                payment_method_types=["alipay"],
                shipping={
                    'name': data['name'],
                    'address': {
                        'line1': data['address']['line1'],
                        'line2': data['address']['line2'],
                        'state': data['address']['state'],
                        'postal_code': data['address']['postal_code'],
                        'country': data['address']['country'],
                    },
                },
            )

            return JsonResponse({
                "client_secret": alipay_payment_intent.client_secret
            })

        except Exception as e:
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Invalid request method"})

def success(request):
    user = get_object_or_404(User, pk=request.session['user_id'])
    price = request.session["ongoing_amount"]
    if price == 100:
        user.status = "Premium"
    elif price == 200:
        user.status = "Premium Plus"
    user.save()
    return render(request, 'authentication/success.html',{"name":user.name})

def cancel(request):
    return render(request, 'authentication/cancel.html')