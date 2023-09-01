from django.shortcuts import redirect, render
from products.forms import CategoryForm,ProductForm,VariantImagesForm,VariantForm
from django.contrib import messages
from products.models import Category,Product,Variant

# Create your views here.
def admin_home(request):
    return render(request,'digix_admin/index.html')


def admin_login(request):
    return render(request,'digix_admin/login.html')

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            
            form.save()
            return redirect('digix_admin:all_category')
        else:
            messages.warning(request,form.errors)
            return render(request,'digix_admin/add_form.html',{'element':'Category Form','form':form})
    form = CategoryForm()
    return render(request,'digix_admin/add_form.html',{'form':form,'element':'Category'})

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


def add_variant(request):
    if request.method == 'POST':
        form = VariantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('digix_admin:all_variants')
        else:
            messages.warning(request,form.errors)
            
            return render(request,'digix_admin/add_form.html',{'form':form,'element':'Variant'})
    form = VariantForm()
    return render(request,'digix_admin/add_form.html',{'form':form,'element':'Variant'})




def all_category(request):
    categories = Category.objects.all()
    
    return render(request,'digix_admin/category.html',{'categories':categories})


def all_products(request):
    products = Product.objects.all()
    return render(request,'digix_admin/product.html',{'products':products})

def all_variants(request):
    variants = Variant.objects.all()
    return render(request,'digix_admin/variant.html',{'variants':variants})