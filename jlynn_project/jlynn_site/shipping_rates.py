from .models import Customer, Art
import six
import easypost
import smtplib
import os
import logging


# using EasyPost get shipping rate or return none if there is a problem.
def get_shipping_rates(customer, image_pk):

    # Needed to get dimensions on piece.
    selection = Art.objects.get(id=image_pk)

    name = customer.first_name + " " + customer.last_name

    try:

        # Wording here is important.
        easypost.api_key = 'L2wIMpaqVZOPRtXNH05MuQ'
        #easypost.api_key = os.environ['EASYPOST_API_KEY']'AR6L28Kttru4eqIytIie1w'

        # creating final dimensions for package. The 8 represents the extra amount for packaging.
        length = selection.length + 8
        width = selection.width + 8
        height = selection.height + 8
        weight = selection.weight


        # EasyPost information
        to_address = easypost.Address.create(
            name = name,
            street1 = customer.street_address,
            street2 = customer.apt_number,
            city = customer.city,
            state = customer.state,
            zip = customer.zip_code,
            country = "US",
            phone = customer.phone_number
        )

        print(to_address)

        from_address = easypost.Address.create(
            name = "Jessica McKeever",
            street1 = "2518 Highway 100 south",
            street2 = "Apt 732",
            city = "Minneapolis",
            state = "MN",
            zip = "55416",
            country = "US",
            phone = "999-999-9999"
        )

        print(from_address)

        # create parcel

        parcel = easypost.Parcel.create(
            length = length,
            width = width,
            height = height,
            weight = weight
        )

        print(parcel)

        # create shipment
        shipment = easypost.Shipment.create(
            to_address = to_address,
            from_address = from_address,
            parcel = parcel
        )

        print(shipment)

        # buy postage label with one of the rate objects
        # EasyPost does not have a easy way of getting the charge amount without going to the dashboard.
        shipment.buy(rate=shipment.lowest_rate(carriers=['USPS'], services=['Priority']))

        # selection.shipping_cost = shipping_price
        # selection.save()


    except Exception as e:

        logging.exception("error processing shipping")
        pass
