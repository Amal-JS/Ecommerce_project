from django import forms
from . models import Coupons,Offers

class CoupounForm(forms.ModelForm):
    class Meta:
        model = Coupons
        fields = '__all__'
        widgets = {
            'valid_to': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize labels for the form fields
        self.fields['code'].label = 'Coupon Code'
        self.fields['discount_percentage'].label = 'Discount Percentage'
        self.fields['cart_min_amount'].label = 'Minimum Cart Amount'
        self.fields['is_active'].label = 'Is Active'
        self.fields['is_deleted'].label = 'Is Deleted'
        self.fields['coupoun_type'].label = 'Coupon Type'
        self.fields['coupoun_applied_to'].label = 'Coupon Applied To'
        self.fields['count'].label = 'Count'
        self.fields['cart_max_amount'].label = 'Cart Maximum Amount'
        self.fields['discount_amount'].label = 'Discount Amount'

        # Make all fields not required
        for field_name, field in self.fields.items():
            field.required = False


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offers
        fields = ['name',  'category', 'variant', 'discount_percentage', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customize labels for the form fields
        self.fields['name'].label = 'Offer Name'
        self.fields['variant'].label = 'Product Variant'
        self.fields['category'].label = 'Product Category'
        self.fields['discount_percentage'].label = 'Discount Percentage'
       
        self.fields['start_date'].label = 'Start Date'
        self.fields['end_date'].label = 'End Date'

        # Make all fields not required
        for field_name, field in self.fields.items():
            field.required = False
