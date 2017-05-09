from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from .models import Art
from .forms import UserInfo
import stripe
import six
import easypost
import os


def purchase(request, image_pk):

    # These are test keys from Stripe. "Live" versions can be added later for real payments.

    stripe.api_key = os.environ['STRIPE_SECRET_KEY']

    key = os.environ['STRIPE_PUBLISHABLE_KEY']



    if request.method == 'POST':

        selection = Art.objects.get(id=image_pk)

        title = selection.title

        # information for Stripe
        price = selection.price
        price_stripe = price * 100 # price needs to be in cents
        price_charge = int(price_stripe) + selection.shipping_cost

        shipping_price = selection.shipping_cost * 100

        # this is for Stripe
        total_amount = int (float(price_stripe) + float(shipping_price))

        price_display = int(price) + float(selection.shipping_cost)


        # Create Stripe customer
        customer = stripe.Customer.create(
            email=request.POST['stripeEmail'],
            source=request.POST['stripeToken'],
        )


        # Process Charge.
        charge = stripe.Charge.create(
            customer=customer['id'],
            amount=total_amount,
            currency='usd',
            description='We thank you for your purchase.'
        )

        return render(request, 'order_receipt.html', {'title' : title, 'price' : price_display})


    return render(request, 'customer_purchase.html')
