from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from .models import Art
from .forms import UserInfo
import stripe

# TODO This will need to be moved to os.environ eventually.
# These are test keys from Stripe. "Live" versions can be added later for real payments.
stripe_keys = {
  'secret_key': 'sk_test_WX4SzxB1PPRyRDvnvN5Xv0vS',
  'publishable_key': 'pk_test_qiC7dKkruip7ESWN86opGEUA'
}


def buy_painting(request, image_pk):
    ''' Collects the users infor '''
    selection = Art.objects.get(id=image_pk)

    price = selection.price
    price_stripe = price * 100
    price_charge = int(price_stripe)

    title = selection.title

    stripe.api_key = stripe_keys['secret_key']

    key = stripe_keys['publishable_key']

    form = UserInfo()

    if request.method == 'POST':

        # form_post = UserInfo(request.POST)

        name=request.POST['stripeShippingName'],
        address=request.POST['stripeShippingAddressLine1'],
        city=request.POST['stripeShippingAddressCity'],
        zip_code=request.POST['stripeShippingAddressZip'],

        print(address)

        customer = stripe.Customer.create(
        email=request.POST['stripeEmail'],
        source=request.POST['stripeToken'],
        )


        charge = stripe.Charge.create(
        customer=customer.id,
        amount=price_charge,
        currency='usd',
        description='We thank you for your purchase. Please enjoy ' + title,
        receipt_email=customer.email

    )

        return render(request, 'order_summary.html', {'title' : selection.title, 'price' : price})


    return render(request, 'customer_form.html', {'form' : form, 'image_pk' : image_pk, 'key' : key, 'price' : price, 'price_stripe' : price_stripe})

# def buy_painting_stripe(request, image_pk):
#
#     selection = Art.objects.get(id=image_pk)
