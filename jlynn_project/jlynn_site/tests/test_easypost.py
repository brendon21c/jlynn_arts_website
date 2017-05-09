from django.test import TestCase
import easypost


# I modified these tests form easypost's github page. I wasn't sure how to do it otherwise.
# https://github.com/EasyPost/easypost-python/blob/master/tests/test_shipment.py
# All of these tests should pass, since the User enters the shipping information in the form, and
# here the info is being hard coded. The main point is to ensure Easypost os working.

class TestShipment(TestCase):

    easypost.api_key = 'L2wIMpaqVZOPRtXNH05MuQ'


    # Make sure shipment creation can send back rates. This should pass.
    def test_shipment_get_rates(self):

        # Entry information copied from easypost docs to save on typing.
        shipment = easypost.Shipment.create(

          to_address={
            "name": 'Dr. Steve Brule',
            "street1": '179 N Harbor Dr',
            "city": 'Redondo Beach',
            "state": 'CA',
            "zip": '90277',
            "country": 'US',
            "phone": '4153334444',
            "email": 'dr_steve_brule@gmail.com'
          },
          from_address={
            "name": 'EasyPost',
            "street1": '417 Montgomery Street',
            "street2": '5th Floor',
            "city": 'San Francisco',
            "state": 'CA',
            "zip": '94104',
            "country": 'US',
            "phone": '4153334444',
            "email": 'support@easypost.com'
          },
          parcel={
            "length": 20.2,
            "width": 10.9,
            "height": 5,
            "weight": 65.9
          }

        )

        # fetch rates from api call.
        rates = shipment.get_rates()
        self.assertTrue(rates is not None)


    # The program automatically pulls the Priority class rate to apply to shipping. This should pass.
    def test_for_retail_rate_price(self):

        # Entry information copied from easypost docs to save on typing.
        shipment = easypost.Shipment.create(

          to_address={
            "name": 'Dr. Steve Brule',
            "street1": '179 N Harbor Dr',
            "city": 'Redondo Beach',
            "state": 'CA',
            "zip": '90277',
            "country": 'US',
            "phone": '4153334444',
            "email": 'dr_steve_brule@gmail.com'
          },
          from_address={
            "name": 'EasyPost',
            "street1": '417 Montgomery Street',
            "street2": '5th Floor',
            "city": 'San Francisco',
            "state": 'CA',
            "zip": '94104',
            "country": 'US',
            "phone": '4153334444',
            "email": 'support@easypost.com'
          },
          parcel={
            "length": 20.2,
            "width": 10.9,
            "height": 5,
            "weight": 65.9
          }

        )

        rates = shipment.get_rates()
        rate = rates.rates[0]['retail_rate']

        self.assertTrue(rate is not None)

    # Test to ensure that the to address and the defualt buyer's address are the same. Easypost
    # should default these.
    def test_addresses_match(self):

        # Entry information copied from easypost docs to save on typing.
        shipment = easypost.Shipment.create(

          to_address={
            "name": 'Dr. Steve Brule',
            "street1": '179 N Harbor Dr',
            "city": 'Redondo Beach',
            "state": 'CA',
            "zip": '90277',
            "country": 'US',
            "phone": '4153334444',
            "email": 'dr_steve_brule@gmail.com'
          },
          from_address={
            "name": 'EasyPost',
            "street1": '417 Montgomery Street',
            "street2": '5th Floor',
            "city": 'San Francisco',
            "state": 'CA',
            "zip": '94104',
            "country": 'US',
            "phone": '4153334444',
            "email": 'support@easypost.com'
          },
          parcel={
            "length": 20.2,
            "width": 10.9,
            "height": 5,
            "weight": 65.9
          }

        )

        self.assertEqual(shipment.buyer_address.street1, shipment.to_address.street1)
        self.assertEqual(shipment.buyer_address.city, shipment.to_address.city)
        self.assertEqual(shipment.buyer_address.state, shipment.to_address.state)

    # Test to ensure that shipment needs all information, this should fail.
    def test_no_reciever_address_given(self):

        # No to address given.
        shipment = easypost.Shipment.create(

          to_address={
            "name": 'Dr. Steve Brule',
            "street1": ' ',
            "city": 'Redondo Beach',
            "state": 'CA',
            "zip": '90277',
            "country": 'US',
            "phone": '4153334444',
            "email": 'dr_steve_brule@gmail.com'
          },
          from_address={
            "name": 'EasyPost',
            "street1": '417 Montgomery Street',
            "street2": '5th Floor',
            "city": 'San Francisco',
            "state": 'CA',
            "zip": '94104',
            "country": 'US',
            "phone": '4153334444',
            "email": 'support@easypost.com'
          },
          parcel={
            "length": 20.2,
            "width": 10.9,
            "height": 5,
            "weight": 65.9
          }

        )

        self.assertFalse(shipment)
