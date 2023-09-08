from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from products.models import Variant_Images
from products.forms import CategoryForm,ProductForm,VariantForm
from django.contrib import messages
from products.models import Category,Product,Variant

#for variant images and variant adding we are using 'transactions' in db
from django.db import transaction

#admin home 
def admin_home(request):
    return render(request,'digix_admin/index.html')

#admin login
def admin_login(request):
    return render(request,'digix_admin/login.html')

#add new category

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            
            form.save()
            return redirect('digix_admin:all_category')
        else:
            #if error show it in the page 
            messages.warning(request,form.errors)
            return render(request,'digix_admin/add_form.html',{'element':'Category Form','form':form})
    form = CategoryForm()
    return render(request,'digix_admin/add_form.html',{'form':form,'element':'Category'})

#add new product
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('digix_admin:all_products')
        else:
            messages.warning(request,form.errors)
            
            return render(request,'digix_admin/add_form.html',{'form':form,'element':'Product'})
    form = ProductForm()
    return render(request,'digix_admin/add_form.html',{'form':form,'element':'Product'})


#addding new variant with images corresponding to the variant object
def add_variant(request):
    if request.method == 'POST':
        form = VariantForm(request.POST)
        

        if form.is_valid():

            try:

                with transaction.atomic():
                    
                    #variant object is saved only if the five image field is accepted image field can be empty
                    variant=form.save()

                    #passing each image to Variant Image model
                    #five image field
                           
                            
                    for i in range(1, 6):
                        #getting each image from request.FILES
                        uploaded_file = request.FILES.get(f'image{i}')
                        if uploaded_file:
                            try:
                                variant_image = Variant_Images(variant=variant, image=uploaded_file)
                                variant_image.full_clean()  # Validate the uploaded file 
                                variant_image.save()

                            except ValidationError as e:
                                #error occur while accepting image
                                messages.error(request, e)

                    return redirect('digix_admin:all_variants')
                

            except Exception as e:
                #error occuring in transaction
                messages.error(request,e)
                return render(request,'digix_admin/add_form.html',{'form':form,'element':'Variant'})      

            
            
        else:
            messages.warning(request,form.errors)
            
            return render(request,'digix_admin/add_form.html',{'form':form,'element':'Variant'})
    
    #new form send wile accessing the page using get request
    form = VariantForm()
    return render(request,'digix_admin/add_form.html',{'form':form,'element':'Variant'})



#get all categories
def all_category(request):
    categories = Category.objects.all()
    
    
    return render(request,'digix_admin/category.html',{'categories':categories})

#get all products
def all_products(request):
    products = Product.objects.all()
    return render(request,'digix_admin/product.html',{'products':products})

#get all variants
def all_variants(request):
    variants = Variant.objects.all()
    return render(request,'digix_admin/variant.html',{'variants':variants})


#delete category
def  delete_category(request,id):
    cat_obj= Category.objects.get(id=id)
    cat_obj.delete()
    return redirect("digix_admin:all_category")


def  delete_product(request,id):
    cat_obj= Product.objects.get(id=id)
    cat_obj.delete()
    return redirect("digix_admin:all_products")


def  delete_variant(request,id):
    cat_obj=Variant.objects.get(id=id)
    cat_obj.delete()
    return redirect("digix_admin:all_variants")


#update category object
def category_update(request, id):
    #will raise exception if object not found
    category = get_object_or_404(Category, id=id)
    
    if request.method == 'POST':
        #passing the new form values with existing instance
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('digix_admin:all_category')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'digix_admin/add_form.html', {'form': form, 'element': category,'update':True})



def product_update(request, id):
    product = get_object_or_404(Product, id=id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('digix_admin:all_products')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'digix_admin/add_form.html', {'form': form, 'element': product,'update':True})

# Retrieve the Variant instance to be updated using its primary key (id)
def variant_update(request, id):
    variant = Variant.objects.get(pk=id)

    if request.method == 'POST':
        # Create a VariantForm instance with the data from the request, including uploaded files, and bind it to the existing Variant instance
        form = VariantForm(request.POST, request.FILES, instance=variant)
        if form.is_valid():
            # Check if new images have been uploaded
            new_images = []

            # Loop through image fields (image1, image2, ..., image5)
            for i in range(1, 6):
                image_field_name = f'image{i}'
                try:
                    # Attempt to retrieve an uploaded image from request.FILES
                    image = request.FILES.get(image_field_name, None)
                    if image:
                        new_images.append(image)
                except ValidationError as e:
                    # If there's a validation error (unlikely in this context), show an error message and return to the form
                    messages.error(request, e)
                    return render(request, 'digix_admin/add_form.html', {'form': form, 'element': 'Variant', 'update': True})

            if new_images:
                # Delete existing images associated with the variant
                variant.variant_images.all().delete()

                # Create new Variant_Images instances for the variant with the new images
                for image in new_images:
                    Variant_Images.objects.create(variant=variant, image=image)

            # Save the updated variant with or without new images
            form.save()
            return redirect('digix_admin:all_variants')
        else:
            # If the form is not valid, display form errors and return to the form
            messages(request, form.errors)
            return render(request, 'digix_admin/add_form.html', {'form': form, 'element': 'Variant', 'update': True})

    else:
        # If it's a GET request, create a VariantForm instance pre-filled with the existing variant data
        form = VariantForm(instance=variant)

    # Render the form page for updating the variant
    return render(request, 'digix_admin/add_form.html', {'form': form, 'element': 'Variant', 'update': True})
