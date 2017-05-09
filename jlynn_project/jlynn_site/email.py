import logging
from .models import Customer, Art
import os
from sender import Mail, Message



def email_shipping_info(customer, image_pk):

    # Needed to get title of piece.
    selection = Art.objects.get(id=image_pk)

    title = selection.title

    name = customer.first_name + " " + customer.last_name

    # Email Jess shipping information, Had to do it this way since Stripe's shipping
    # process won't work for this format.
    try:

        SMTP_HOST = 'smtp.gmail.com'
        SMTP_USER = 'brennon.mckeever@gmail.com'
        SMTP_PASS = 'Daeda!us1983'
        SMTP_ADDRESS = 'brennon.mckeever@gmail.com'

        body = """ From: {}  \n Street Address: {} \n
        Apt: {} \n City: {} \n State: {} \n Zip Code: {} \n
        Phone: {}  """.format(name, customer.street_address, customer.apt_number, customer.city,
        customer.state, customer.zip_code, customer.phone_number)

        msg = Message("Shipping info for {}".format(title))
        msg.to = "artbyjessicamckeever@gmail.com"
        msg.body = body

        mail = Mail(host=SMTP_HOST, username=SMTP_USER, password=SMTP_PASS,port=465,
            use_ssl=True,fromaddr=SMTP_ADDRESS)

        mail.send(msg)

    except Exception as e:

        logging.exception("error sending email")
