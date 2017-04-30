from django import forms


class UserInfo(forms.Form):
    """Collects the user's name and shipping information"""

    #email_address = forms.CharField(label='Email Address', max_length=100)
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    street_address = forms.CharField(label='Street Address', max_length=100)
    apt_number = forms.CharField(label='Apt Number', max_length=10)
    city = forms.CharField(label='City', max_length=50)
    state = forms.CharField(label='State', max_length=20)
    zip_code = forms.CharField(label='Zipcode', max_length=5)
    phone_number = forms.CharField(label='Phone Number', max_length=20)
