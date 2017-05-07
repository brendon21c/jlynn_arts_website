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

        body = """ From: {}  \n Street Address: {} \n
        Apt: {} \n City: {} \n State: {} \n Zip Code: {} \n
        Phone: {}  """.format(name, customer.street_address, customer.apt_number, customer.city,
        customer.state, customer.zip_code, customer.phone_number)

        msg = Message("Shipping info for {}".format(title))
        msg.fromaddr = ("Brendon", "brennon.mckeever@gmail.com")
        msg.to = "brendon21c@gmail.com"
        msg.body = body

        mail = Mail("smtp.gmail.com", port=587, username="brennon.mckeever", password="Daeda!us1983",
            use_tls=False, use_ssl=False, debug_level=None)

        mail.send(msg)

    except Exception as e:

        logging.exception("error sending email")






    # using tutorial from: http://naelshiab.com/tutorial-send-email-python/

    # fromaddr = "brennon.mckeever@gmail.com"
    # toaddr = "brendon21c@gmail.com"
    # msg = MIMEMultipart()
    # msg['From'] = fromaddr
    # msg['To'] = toaddr
    # msg['Subject'] = "Shipping info for {}".format(title)
    #
    # body = """ From: {}  \n Street Address: {} \n
    # Apt: {} \n City: {} \n State: {} \n Zip Code: {} \n
    # Phone: {}  """.format(name, customer.street_address, customer.apt_number, customer.city,
    #  customer.state, customer.zip_code, customer.phone_number)
    #
    #
    # msg.attach(MIMEText(body, 'plain'))
    #
    # server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.ehlo()
    # server.starttls()
    # # TODO add to os.environ later.
    # server.login(fromaddr, "Daeda!us1983")
    # #server.login(fromaddr, os.environ['GMAIL_LOGIN'])
    # text = msg.as_string()
    # server.sendmail(fromaddr, toaddr, "hello")
    # server.quit()
