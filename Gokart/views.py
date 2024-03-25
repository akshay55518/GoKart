from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.views import PasswordResetDoneView
from .models import Product,Category,Banner,Customer,WishListItem
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .forms import CustomerRegistrationForm,CustomerProfileForm,MyPasswordResetForm
from .models import *
from django import utils
from django.conf import settings
from django.db.models import Avg
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required

#user autentication
class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'auth/signin.html',locals())
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Contragulation! User registered successfull")
        else:
            messages.warning(request,"Error in Registration")
        return render(request,'auth/signin.html',locals())
    
def user_login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'yeah your already login')
        return redirect(home)
    if request.method == "POST": 
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username, password=password)
        print(user)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect(admin_dashboard)
        elif user is not None:
            login(request, user)
            return redirect(home)
        else:
            messages.warning(request, f'user is not match please create a account ')
    return render(request,'auth/login.html',locals())

def logout_view(request):
    logout(request)
    return redirect(user_login)

def get_password_reset_url(request):
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
    review=Review.objects.filter(product=pk)
    reviews = product.reviews.order_by('-created_at')[:5] # get the top 5 reviews for this product
    average_rating = review.aggregate(Avg('rating'))['rating__avg']
    return render(request,'app/product-detail.html',locals())


def add_review(request,pk):
    if request.method == 'POST':
        rating = request.POST['rating']
        comment = request.POST['comment']
        user = request.user
        product= Product.objects.get(id=pk)
        review=Review.objects.create(
            product=product, 
            user=user, 
            rating=rating, 
            comment=comment
            )
        return render(request, 'app/product-detail.html',locals())
    
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user == review.user:
        review.delete()
        return redirect('productdetail', pk=pk)  # Redirect to the product detail page

@login_required(login_url='login')
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

@login_required(login_url='login')
def address(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    totalitem1=0
    if request.user.is_authenticated:
        totalitem1=len(WishListItem.objects.filter(user=request.user))
    add=Customer.objects.filter(user=request.user)
    return render(request,'app/address.html',locals()) 

@login_required(login_url='login')
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
    
@login_required(login_url='login')
def deleteaddress(request,pk):
    obj=Customer.objects.get(pk=pk)
    obj.delete()
    messages.warning(request,"Address deleted Successfully")
    return redirect('address')
    
#cart section
@login_required(login_url='login')
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
    
@login_required(login_url='login')
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

    


def checkout(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    totalitem1=0
    if request.user.is_authenticated:
        totalitem1=len(WishListItem.objects.filter(user=request.user))
    if request.method=='GET':
        user=request.user
        # print(user)
        customer=Customer.objects.filter(user=user)
        # print(customer)
        cart_item=Cart.objects.filter(user=user)
        # print(cart_item)
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
        # print(order_amount)
        # print(p.quantity)
        return render(request,'app/checkout.html',locals())

def orderplaced(request):
    if request.method == 'POST':
        user=request.user
        cust_id = request.POST.get('custid')
        total_amount = request.POST.get('totalamount')
        cart_item=Cart.objects.filter(user=user).first()
        cart_items=Cart.objects.filter(user=user)
        for p in cart_items:
            quantity=p.quantity
            product=p.product
        order = OrderPlaced.objects.create(
            user=user,
            customer_id=cust_id,
            product=product,  
            quantity=quantity,  
            status='Pending',   
        )
        cart_item.delete()
        messages.success(request, 'Order placed successfully!')
        return redirect('order_success')
    else:
        messages.error(request, 'No items found in the cart.')
        return redirect('checkout')
    
def order_success(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    totalitem1=0
    if request.user.is_authenticated:
        totalitem1=len(WishListItem.objects.filter(user=request.user))
    return render(request, 'app/order_placed.html',locals())

           
def orders(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    totalitem1=0
    if request.user.is_authenticated:
        totalitem1=len(WishListItem.objects.filter(user=request.user))
    user=request.user
    order=OrderPlaced.objects.filter(user=user)
    return render(request, "app/orders.html", locals())

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
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt  # This decorator is used to exempt CSRF protection for this view
# def add_to_wishlist(request):
#     if request.method == 'POST':
#         product_id = request.POST.get('product_id')  # Assuming 'product_id' is sent in the request data
#         product = get_object_or_404(Product, id=product_id)
#         # Check if the product is already in the wishlist
#         if Wishlist.objects.filter(product=product, user=request.user).exists():
#             # If already in the wishlist, remove it
#             Wishlist.objects.filter(product=product, user=request.user).delete()
#             return JsonResponse({'success': False})
#         else:
#             # If not in the wishlist, add it
#             Wishlist.objects.create(product=product, user=request.user)
#             return JsonResponse({'success': True})
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=400)

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
        results=Product.objects.filter(
            models.Q(title__icontains=query) |
            models.Q(selling_price__icontains=query)
            )
    else:
        results=None
    return render(request,'app/search_results.html',locals())

    
#admin section
# @login_required
def admin_dashboard(request):
    users=User.objects.all()
    orders=OrderPlaced.objects.all()
    return render(request,'admin/admin-dashboard.html',locals())
    