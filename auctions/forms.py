from django import forms
from .models import Category

class NewListing(forms.Form):
    category_list = Category.objects.all()
    category_choices = [(category.name, category.name) for category in category_list]
    title = forms.CharField(label="Title")
    description = forms.CharField(label="Description")
    image = forms.CharField(label="Image URL")
    price = forms.FloatField(label="price")
    option_field = forms.ChoiceField(choices=category_choices, label="Choose a Category")


class BidForm(forms.Form):
    amount = forms.DecimalField(label='Bid Amount', min_value=0.01)