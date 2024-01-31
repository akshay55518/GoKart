from django.shortcuts import render,redirect
from .models import Product,Category,Banner,Customer
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib.auth import logout

#user autentication
class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'app/registration.html',locals())
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Contragulation! User registered successfull")
        else:
            messages.warning(request,"Error in Registration")
        return render(request,'app/registration.html',locals())
    
def login(request):
    return render(request,'app/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
    
    
# Create your views here.
def home(request):
    banner=Banner.objects.all()
    category=Category.objects.all()
    product=Product.objects.all()
    # id=Product.objects.filter().values('id')
    obj={'category':category,'product':product,'banner':banner,'id':id}
    return render(request,'app/home.html',obj)

def aboutus(request):
    return render(request,'app/about-us.html')

def contactus(request):
    return render(request,'app/contact-us.html')

def category(request,val):
    product=Product.objects.filter(category=val)
    # title=Product.objects.filter(category=val).values('id')
    return render(request,'app/category.html',locals())

def productdetail(request,pk):
    product=Product.objects.get(pk=pk)
    return render(request,'app/product-detail.html',locals())

def profileview(request):
    if request.method=='POST':
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            address=form.cleaned_data['address']
            city=form.cleaned_data['city']
            mobile=form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=user,name=name,address=address,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Data saved successfully')
            return redirect(profileview)
        else:
            messages.warning(request,"Please correct the error ")
            return redirect(profileview)
    else:
        form=CustomerProfileForm()
        return render(request,"app/profile-view.html", locals())
    
def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',locals()) 

def updateaddress(request,pk):
    if request.method=='POST':
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            obj=Customer.objects.get(pk=pk)
            obj.name=form.cleaned_data['name']
            obj.address=form.cleaned_data['address']
            obj.city=form.cleaned_data['city']
            obj.mobile=form.cleaned_data['mobile']  
            obj.state=form.cleaned_data['state']
            obj.zipcode=form.cleaned_data['zipcode']
            obj.save()
            messages.success(request,'Address updated successfully!')
        else:
            messages.error(request,'Error in updating Address')
        return redirect('address')
    else:
        add=Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        return render(request,'app/address-update.html',locals())
    



    
                    


    
#admin section
# @login_required
def admin_dashboard(request):
    return render(request,'admin/admin-dashboard.html',locals())
    