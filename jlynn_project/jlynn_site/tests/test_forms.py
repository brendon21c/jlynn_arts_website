from django.test import TestCase
from django import forms

from ..forms import UserInfo

# Test that Customer shipping form is valid or not.

class NewUserShippingTests(TestCase):

    # All fields need to be entered for form to be valid, this should pass, all fields are entered.
    def test_all_fields_complete(self):

        form_data = {"first_name" : "bob", "last_name" : "villa", "street_address" : "123 fake st",
        "apt_number" : "1", "city" : "Los Angeles", "state" : "CA", "zip_code" : "90218",
        "phone_number" : "9993451256"}

        form = UserInfo(form_data)
        self.assertTrue(form.is_valid)

    # Test for empty fields in form, all fields need to be entered, this should fail.
    # adapting this from http://chimera.labs.oreilly.com/books/1234000000754/ch11.html#_testing_and_customising_form_validation
    def test_missing_fields(self):

        form_data = {"first_name" : " "}
        form = UserInfo(form_data)

        self.assertFalse(form.is_valid)
        self.assertEqual(form.errors["first_name"],
        ["You can't have an empty list item"])


    # I saw this from your LMN tests and wanted to try it, if somebody has a REALLY long last name
    # the form will not be valid, this should fail.
    def test_last_name_too_long(self):

        form_data = {"last_name" : "miller" * 100}
        form = UserInfo(form_data)

        self.assertFalse(form.is_valid)
        self.assertEqual(form.errors["last_name"],
        ["Name field exceeds max characters."])
