from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from .models import Art
from .forms import UserInfo
import stripe
import six
import easypost


# TODO This will need to be moved to os.environ eventually.
# These are test keys from Stripe. "Live" versions can be added later for real payments.
stripe_keys = {
  'secret_key': 'sk_test_WX4SzxB1PPRyRDvnvN5Xv0vS',
  'publishable_key': 'pk_test_qiC7dKkruip7ESWN86opGEUA'
}



def purchase(request, image_pk):

    stripe.api_key = stripe_keys['secret_key']

    key = stripe_keys['publishable_key']


    if request.method == 'POST':

        selection = Art.objects.get(id=image_pk)

        title = selection.title

        # information for Stripe
        price = selection.price
        price_stripe = price * 100 # price needs to be in cents
        price_charge = int(price_stripe) + selection.shipping_cost

        shipping_price = selection.shipping_cost * 100

        # this is for Stripe
        total_amount = float(price_stripe) + float(shipping_price)

        price_display = int(price) + float(selection.shipping_cost)


        customer = stripe.Customer.create(
            email=request.POST['stripeEmail'],
            source=request.POST['stripeToken'],
        )

        customer_email = customer['email']

        charge = stripe.Charge.create(
            customer=customer['id'],
            amount=total_amount,
            currency='usd',
            description='We thank you for your purchase. Please enjoy ' + title,
            receipt_email=customer_email

        )

        return render(request, 'order_receipt.html', {'title' : title, 'price' : price_display})


    return render(request, 'customer_purchase.html')
