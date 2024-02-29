from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Category,Banner,Customer,WishListItem
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate
from .forms import CustomerRegistrationForm,CustomerProfileForm,MyPasswordResetForm,LoginForm
from django.contrib.auth import logout
from .models import *
from django import utils
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Q
from Ecommerce.settings import RAZOR_API_KEY,RAZOR_API_SECRET_KEY
import razorpay

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
    
# def login(request):
#     return render(request,'app/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def get_password_reset_url(request):
    # email=MyPasswordResetForm()
    base64_encoded_id = utils.http.urlsafe_base64_encode(utils.encoding.force_bytes(request.id))
    token = PasswordResetTokenGenerator().make_token(request)
    reset_url_args = {'uidb64': base64_encoded_id, 'token': token}
    reset_path = reverse('password_reset_confirm', kwargs=reset_url_args)
    reset_url = f'{settings.BASE_URL}{reset_path}'
    return reset_url
    # return render(request,'app/password_reset_done.html',locals())
    
    
    
# Create your views here.
def home(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    totalitem1=0
    if request.user.is_authenticated:
        totalitem1=len(WishListItem.objects.filter(user=request.user))
    banner=Banner.objects.all()
    category=Category.objects.all()
    product=Product.objects.all()
    # id=Product.objects.filter().values('id')
    obj={'category':category,'product':product,'banner':banner,'id':id}
    return render(request,'app/home.html',locals())

def aboutus(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    totalitem1=0
    if request.user.is_authenticated:
        totalitem1=len(WishListItem.objects.filter(user=request.user))
    return render(request,'app/about-us.html',locals())

def contactus(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    totalitem1=0
    if request.user.is_authenticated:
        totalitem1=len(WishListItem.objects.filter(user=request.user))
    return render(request,'app/contact-us.html',locals())

def category(request,val):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    totalitem1=0
    if request.user.is_authenticated:
        totalitem1=len(WishListItem.objects.filter(user=request.user))
    product=Product.objects.filter(category=val)
    if val=='Mo':
        name='MobilePhone'
    elif val=='El':
        name="Electronics"
    elif  val=="Fa":
        name="Fashion"
    elif val=='Ap':
        name="Appliances"
    elif val=='Gr':
        name="Groceries"
    elif val=='Me':
        name="Medicine"
    else:
        name="Others"
    return render(request,'app/category.html',locals())

def productdetail(request,pk):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    totalitem1=0
    if request.user.is_authenticated:
        totalitem1=len(WishListItem.objects.filter(user=request.user))
    product=Product.objects.get(pk=pk)
    return render(request,'app/product-detail.html',locals())

def profileview(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    totalitem1=0
    if request.user.is_authenticated:
        totalitem1=len(WishListItem.objects.filter(user=request.user))
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
            return redirect('address')
        else:
            messages.warning(request,"Please correct the error ")
            return redirect(profileview)
    else:
        form=CustomerProfileForm()
        return render(request,"app/profile-view.html", locals())
    
def address(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    totalitem1=0
    if request.user.is_authenticated:
        totalitem1=len(WishListItem.objects.filter(user=request.user))
    add=Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',locals()) 

def updateaddress(request,pk):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    totalitem1=0
    if request.user.is_authenticated:
        totalitem1=len(WishListItem.objects.filter(user=request.user))
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
    
def deleteaddress(request,pk):
    obj=Customer.objects.get(pk=pk)
    obj.delete()
    messages.warning(request,"Address deleted Successfully")
    return redirect('address')
    
#cart section
def add_to_card(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    totalitem1=0
    if request.user.is_authenticated:
        totalitem1=len(WishListItem.objects.filter(user=request.user))
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')
    

def show_cart(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    totalitem1=0
    if request.user.is_authenticated:
        totalitem1=len(WishListItem.objects.filter(user=request.user))
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value=p.quantity*p.product.discount_price
        amount=amount+value
    if amount>1000:
        totalamount=amount
    else:
        totalamount=amount+40
    return render(request,'app/add-tocart.html',locals())

def remove_from_cart(request,cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect(show_cart)


def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discount_price
            amount=amount+value
        if amount>1000:
            totalamount=amount
        else:
            totalamount=amount+100
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value=p.quantity*p.product.discount_price
            amount=amount+value
        if amount>1000:
            totalamount=amount
        else:
            totalamount=amount+100
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)

# def remove_cart(request):
#     if request.method=='GET':
#         prod_id=request.GET['prod_id']
#         c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
#         c.delete()
#         user=request.user
#         cart=Cart.objects.filter(user=user)
#         amount=0
#         for p in cart:
#             value=p.quantity*p.product.discount_price
#             amount=amount+value
#         if amount>1000:
#             totalamount=amount
#         else:
#             totalamount=amount+100
#         data={
#             'amount':amount,
#             'totalamount':totalamount
#         }
#         return JsonResponse(data)
    
    
client=razorpay.Client(auth=(RAZOR_API_KEY,RAZOR_API_SECRET_KEY))
def checkout(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    totalitem1=0
    if request.user.is_authenticated:
        totalitem1=len(WishListItem.objects.filter(user=request.user))
    if request.method=='GET':
        user=request.user
        print(user)
        customer=Customer.objects.filter(user=user)
        cart_item=Cart.objects.filter(user=user)
        famount=0
        for p in cart_item:
            value=p.quantity*p.product.discount_price
            famount=famount+value
        if famount>1000:
            totalamount=famount
        elif famount==0:
            totalamount=0
        else:
            totalamount=famount+100
        totalamount1=totalamount*100
        order_amount=float(totalamount1)
        api_key=RAZOR_API_KEY
        # order_currency='INR'
        # order_receipt='order_rcptid_12'
        # payment_id=request.GET.get('payment_id')
        # notes={'Shipping address':customer}
        # payment_order=client.order.create(dict(amount=order_amount,currency=order_currency,receipt=order_receipt,payment_capture=1))
        
        data={'amount': order_amount,'currency':'INR','receipt':'order_rcptid_12'}
        payment_order=client.order.create(data=data)
        print(payment_order)
        
        payment_order_id=payment_order['id']
        order_id=payment_order_id
        # print(order_id)
        # order_status=payment_order['status']
        # print(payment_order)
        # payment=Payment(user=user,amount=order_amount,razorpay_order_id=order_id,razorpay_payment_status=order_status,)
        # payment.save()
        # print(payment)
        order_status=payment_order['status']
        if order_status=='created':
            payment=Payment(
                user=user,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status,
            )
            payment.save()
        return render(request,'app/checkout.html',locals())

def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    user=request.user
    customer=Customer.objects.get(id=cust_id)
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid=True
    payment.razorpay_payment_id=payment_id
    payment.save()
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.delete()
    return redirect('orders')

def wishlist(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    totalitem1=0
    if request.user.is_authenticated:
        totalitem1=len(WishListItem.objects.filter(user=request.user))
    product=Product.objects.all()
    wishlist_items=WishListItem.objects.filter(user=request.user)
    return render(request,'app/wishlist.html',locals())

def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = WishListItem.objects.get_or_create(user=request.user,product=product)
    if created:
        pass
    return redirect('wishlist')

def remove_from_wishlist(request, wishlist_item_id):
    wishlist_item = get_object_or_404(WishListItem, id=wishlist_item_id, user=request.user)
    wishlist_item.delete()
    return redirect('wishlist')

def search_results(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    totalitem1=0
    if request.user.is_authenticated:
        totalitem1=len(WishListItem.objects.filter(user=request.user))
    query=request.GET.get('search')
    if query:
        results=Product.objects.filter(title__icontains=query)
    else:
        results=None
    return render(request,'app/search_results.html',locals())

    

#admin section
# @login_required
def admin_dashboard(request):
    if request.user=='admin':
        return render(request,'admin/admin-dashboard.html',locals())
    