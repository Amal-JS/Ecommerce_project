from django.shortcuts import render

# Create your views here.
def admin_home(request):
    return render(request,'digix_admin/index.html')


def admin_login(request):
    return render(request,'digix_admin/login.html')