#importing all the models
from . models import Category,Product,Variant,Variant_Images
from django import forms

from django.utils.translation import gettext_lazy as _


class CategoryForm(forms.ModelForm):
    is_available = forms.BooleanField(label='Available', widget=forms.CheckboxInput(attrs={'class': 'mx-2',}),required=False)
    class Meta:
        model=Category
        fields=['name','is_available']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Category Name','class': ''}),
        }


class ProductForm(forms.ModelForm):

    #select field for selecting category instance
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), 
        empty_label="Select Category",
        widget=forms.Select(attrs={'class': 'select_admin'}),)
    
    class Meta:
        model=Product
        fields=['name','category','brand']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Product Name'}),
            
            'brand': forms.TextInput(attrs={'placeholder': 'Enter Brand Name'}),
        }



class VariantForm(forms.ModelForm):

    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),  
        empty_label="Select Product",
        widget=forms.Select(attrs={'class': 'select_admin'}),)
    
    #choice field
    tv_mount = forms.ChoiceField(
        choices=Variant.tv_mount_choices,
        required=False,
        widget=forms.Select(attrs={'placeholder': 'Select TV Mount' ,'class':'select_admin'}),
    )
#=====================================================================================================
# image field only want to accept jpg or jpeg or svg file for that use 'accept' :'.jpg,.jpeg etc ' 
# in the attrs
#=====================================================================================================  
    image1 = forms.ImageField(
        label="Image 1",
        required=False,

        # The ClearableFileInput widget in Django provides a file input field with the option to clear
        #   the currently selected file, allowing users to remove a file 
        # if they change their mind or want to update it. It includes a checkbox and label that, when
        #   clicked, clears the file input.

        # Using ClearableFileInput can be beneficial in scenarios where you want to provide users with the ability
        # to easily remove a file they've selected, such as when they want to replace it with another file or 
        # if they've accidentally uploaded the wrong file.
        
        widget=forms.ClearableFileInput(attrs={'class': 'select_admin','accept': '.jpg, .jpeg, .svg'}),
    )
    image2 = forms.ImageField(
        label="Image 2",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'select_admin','accept': '.jpg, .jpeg, .svg'}),
    )
    image3 = forms.ImageField(
        label="Image 3",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'select_admin','accept': '.jpg, .jpeg, .svg'}),
    )
    image4 = forms.ImageField(
        label="Image 4",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'select_admin','accept': '.jpg, .jpeg, .svg'}),
    )
    image5 = forms.ImageField(
        label="Image 5",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'select_admin','accept': '.jpg, .jpeg, .svg'}),
    )

    is_available = forms.BooleanField(label='Available', widget=forms.CheckboxInput(attrs={'class': 'mx-2',}),required=False)

    class Meta:
        model=Variant
        fields=['product','name','ram','storage','color','mr_price','selling_price','is_available','stock','screen_resolution','description','no_of_usb_ports','no_of_hdmi_ports','tv_mount','image1','image2','image3','image4','image5',]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Variant Name'}),
            'ram': forms.NumberInput(attrs={'placeholder': 'Ram'}),
            'storage': forms.NumberInput(attrs={'placeholder': 'Storage'}),
            'color': forms.TextInput(attrs={'placeholder': 'Color of variant'}),
            'mr_price': forms.NumberInput(attrs={'placeholder': 'MRP'}),
            'selling_price': forms.NumberInput(attrs={'placeholder': 'Selling Price'}),
            'stock':forms.NumberInput(attrs={'placeholder':'Enter number of stocks'}),
            'description':forms.Textarea(attrs={'placeholder':'Enter the description for product'}),
            'screen_resolution': forms.NumberInput(attrs={'placeholder': 'Screen Resolution'}),
            'no_of_usb_ports': forms.NumberInput(attrs={'placeholder': '*If TV Number of HDMI ports '}),
            'no_of_hdmi_ports':forms.NumberInput(attrs=({'placeholder':'*If TV Number of HDMI ports  '})),
            'image1': forms.ImageField(),
            'image2': forms.ImageField(),
            'image3': forms.ImageField(),
            'image4': forms.ImageField(),
            'image5': forms.ImageField(),            
            }
        
    

class VariantImagesForm(forms.ModelForm):
    class Meta:
        model=Variant_Images
        fields='__all__'