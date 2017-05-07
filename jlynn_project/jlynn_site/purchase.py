from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from .models import Art, Customer
from .forms import UserInfo
import six
import os
import logging
import stripe
from .shipping_rates import get_shipping_rates
from .email import email_shipping_info


# Wording here is important.

# TODO This will need to be moved to os.environ eventually.
# These are test keys from Stripe. "Live" versions can be added later for real payments.
stripe_keys = {
  'secret_key': 'sk_test_WX4SzxB1PPRyRDvnvN5Xv0vS',
  'publishable_key': 'pk_test_qiC7dKkruip7ESWN86opGEUA'
}


def buy_painting(request, image_pk):
    ''' Collects the users infor '''

    # Needs to be here so information can be displayed on page.
    stripe.api_key = stripe_keys['secret_key']

    key = stripe_keys['publishable_key']

    # query Database and get the correct painting object.
    selection = Art.objects.get(id=image_pk)


    # information for Web page and Stripe to display properly.
    price = selection.price
    price_stripe = price * 100 # price needs to be in cents
    price_charge = int(price_stripe) # needs to be a Integer to be read.

    title = selection.title

    form = UserInfo()

    if request.method == 'POST':

        form_post = UserInfo(request.POST)

        if form_post.is_valid():

            first_name = form_post.cleaned_data['first_name']
            last_name = form_post.cleaned_data['last_name']
            name_combined = first_name + " " + last_name
            street_address = form_post.cleaned_data['street_address']
            apt_number = form_post.cleaned_data['apt_number']
            city = form_post.cleaned_data['city']
            state = form_post.cleaned_data['state']
            zip_code = form_post.cleaned_data['zip_code']
            phone_number = form_post.cleaned_data['phone_number']


            try:

                # I put this into a try catch because this throws an error if no customer is found.
                customer = Customer.objects.get(phone_number=phone_number)


            except Exception as e:

                customer = Customer(first_name=first_name,last_name=last_name,street_address=street_address,
                apt_number=apt_number,city=city,state=state,zip_code=zip_code,phone_number=phone_number)

                customer.save()

            customer = Customer.objects.get(phone_number=phone_number)

            get_shipping_rates(customer,image_pk)


            try:


                email_shipping_info(customer, image_pk)


            except Exception as e:

                logging.exception("error processing email")
                pass

            # Updated Shipping price information
            selection = Art.objects.get(id=image_pk)

            shipping_price = selection.shipping_cost

            # for display in Stripe pop up window
            total_amount = float(price_stripe) + float(shipping_price * 100)


            return render(request, 'customer_purchase.html', {'image_pk' : image_pk, 'key' : key, 'title' : selection.title, 'price' : price, 'ship_price' : shipping_price,
            'total_amount' : total_amount})


    return render(request, 'customer_form.html', {'form' : form, 'image_pk' : image_pk, 'key' : key, 'price' : price, 'price_stripe' : price_stripe})
