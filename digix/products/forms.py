from . models import Category,Product,Variant,Variant_Images
from django import forms

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Category Name','class': 'p-3'}),
        }


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),  # Replace 'Category' with your actual Category model.
        empty_label="Select Category",
        widget=forms.Select(attrs={'class': 'p-2'}),)
    class Meta:
        model=Product
        fields=['name','category','brand']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Product Name'}),
            
                'brand': forms.TextInput(attrs={'placeholder': 'Enter Brand Name'}),
        }



class VariantForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),  # Replace 'Category' with your actual Category model.
        empty_label="Select Product",
        widget=forms.Select(attrs={'class': 'p-2'}),)
    
    tv_mount = forms.ChoiceField(
        choices=Variant.tv_mount_choices,
        required=False,
        widget=forms.Select(attrs={'placeholder': 'Select TV Mount' ,'class':'p-2'}),
    )

    class Meta:
        model=Variant
        fields=['product','name','ram','storage','color','mr_price','selling_price','screen_resolution','no_of_usb_ports','no_of_hdmi_ports','tv_mount']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Variant Name'}),
            'ram': forms.TextInput(attrs={'placeholder': 'Ram'}),
            'storage': forms.TextInput(attrs={'placeholder': 'Storage'}),
            'color': forms.TextInput(attrs={'placeholder': 'Color of variant'}),
            'mr_price': forms.TextInput(attrs={'placeholder': 'MRP'}),
            'selling_price': forms.TextInput(attrs={'placeholder': 'Selling Price'}),
            'screen_resolution': forms.TextInput(attrs={'placeholder': 'Screen Resolution'}),
            'no_of_usb_ports': forms.TextInput(attrs={'placeholder': 'Number of HDMI ports'}),
            'no_of_hdmi_ports':forms.TextInput(attrs=({'placeholder':'Number of HDMI ports'}))
            


        }
class VariantImagesForm(forms.ModelForm):
    class Meta:
        model=Variant_Images
        fields='__all__'