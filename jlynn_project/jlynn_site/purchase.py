from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from .models import Art
from .forms import UserInfo
import stripe
import six
import easypost
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Wording here is important.
easypost.api_key = 'AR6L28Kttru4eqIytIie1w'

# TODO This will need to be moved to os.environ eventually.
# These are test keys from Stripe. "Live" versions can be added later for real payments.
stripe_keys = {
  'secret_key': 'sk_test_WX4SzxB1PPRyRDvnvN5Xv0vS',
  'publishable_key': 'pk_test_qiC7dKkruip7ESWN86opGEUA'
}


def buy_painting(request, image_pk):
    ''' Collects the users infor '''
    selection = Art.objects.get(id=image_pk)

    stripe.api_key = stripe_keys['secret_key']

    key = stripe_keys['publishable_key']

    # information for Stripe
    price = selection.price
    price_stripe = price * 100 # price needs to be in cents
    price_charge = int(price_stripe)

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

            length = selection.length + 8
            width = selection.width + 8
            height = selection.height + 8
            weight = selection.weight
            print(weight)

            # EasyPost information
            to_address = easypost.Address.create(
                verify=["delivery"],
                name = name_combined,
                street1 = street_address,
                street2 = apt_number,
                city = city,
                state = state,
                zip = zip_code,
                country = "US",
                phone = phone_number
            )

            from_address = easypost.Address.create(
                verify=["delivery"],
                name = "Jessica McKeever",
                street1 = "2518 Highway 100 south",
                street2 = "Apt 732",
                city = "Minneapolis",
                state = "MN",
                zip = "55416",
                country = "US",
                phone = "999-999-9999"
            )

            # create parcel
            try:
                parcel = easypost.Parcel.create(
                    predefined_package = "Parcel",
                    weight = weight
                )
            except easypost.Error as e:
                print(str(e))
                if e.param is not None:
                    print('Specifically an invalid param: %r' % e.param)

            parcel = easypost.Parcel.create(
                length = length,
                width = width,
                height = height,
                weight = weight
            )

            # create shipment
            shipment = easypost.Shipment.create(
                to_address = to_address,
                from_address = from_address,
                parcel = parcel
            )

            # buy postage label with one of the rate objects
            #shipment.buy(rate = shipment.lowest_rate(), insurance=price)

            try:

                rates = shipment.get_rates()

                rate = shipment.rates[1]
                shipping_price = float(rate["retail_rate"])

                selection.shipping_cost = shipping_price
                selection.save()

                # for display in Stripe pop up window
                total_amount = float(price_stripe) + float(shipping_price * 100)

                # Email Jess shipping information, Had to do it this way since Stripe's shipping
                # process won't work for this format.
                # using tutorial from: http://naelshiab.com/tutorial-send-email-python/

                fromaddr = "brennon.mckeever@gmail.com"
                toaddr = "jessi.one82@gmail.com"
                msg = MIMEMultipart()
                msg['From'] = fromaddr
                msg['To'] = toaddr
                msg['Subject'] = "Shipping info for sale of  " + " " + title

                body = """ From: {}  \n Street Address: {} \n
                Apt: {} \n City: {} \n State: {} \n Zip Code: {} \n
                Phone: {}  """.format(name_combined, street_address, apt_number, city, state, phone_number, zip_code)

                msg.attach(MIMEText(body, 'plain'))

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                # TODO add to os.environ later.
                server.login(fromaddr, "Daeda!us1983")
                text = msg.as_string()
                server.sendmail(fromaddr, toaddr, text)
                server.quit()

                return render(request, 'customer_purchase.html', {'image_pk' : image_pk, 'key' : key, 'title' : selection.title, 'price' : price, 'ship_price' : shipping_price,
                'total_amount' : total_amount})

            except Exception as e:

                print('no rates given, possible because its Sunday.')
                pass

            # Email Jess shipping information, Had to do it this way since Stripe's shipping
            # process won't work for this format.
            # using tutorial from: http://naelshiab.com/tutorial-send-email-python/

            fromaddr = "brennon.mckeever@gmail.com"
            toaddr = "jessi.one82@gmail.com"
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = "Shipping info for {}".format(title)

            body = """ From: {}  \n Street Address: {} \n
            Apt: {} \n City: {} \n State: {} \n Zip Code: {} \n
            Phone: {}  """.format(name_combined, street_address, apt_number, city, state, zip_code, phone_number)


            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            # TODO add to os.environ later.
            server.login(fromaddr, "Daeda!us1983")
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()

            shipping_price = selection.shipping_cost

            # for display in Stripe pop up window
            total_amount = float(price_stripe) + float(shipping_price * 100)


        return render(request, 'customer_purchase.html', {'image_pk' : image_pk, 'key' : key, 'title' : selection.title, 'price' : price, 'ship_price' : shipping_price,
        'total_amount' : total_amount})


    return render(request, 'customer_form.html', {'form' : form, 'image_pk' : image_pk, 'key' : key, 'price' : price, 'price_stripe' : price_stripe})

# def buy_painting_stripe(request, image_pk):
#
#     selection = Art.objects.get(id=image_pk)
