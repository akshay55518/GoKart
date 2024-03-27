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
    cartitem=0
    wishlistitem=0
    if request.user.is_authenticated:
        cartitem=len(Cart.objects.filter(user=request.user))
        wishlistitem=len(WishListItem.objects.filter(user=request.user))
    banner=Banner.objects.all()
    category=Category.objects.all()
    product=Product.objects.all()
    obj={'category':category,'product':product,'banner':banner,'id':id}
    return render(request,'app/home.html',locals())

def aboutus(request):
    cartitem=0
    wishlistitem=0
    if request.user.is_authenticated:
        cartitem=len(Cart.objects.filter(user=request.user))
        wishlistitem=len(WishListItem.objects.filter(user=request.user))
    category=Category.objects.all()
    return render(request,'app/about-us.html',locals())

def contactus(request):
    cartitem=0
    wishlistitem=0
    if request.user.is_authenticated:
        cartitem=len(Cart.objects.filter(user=request.user))
        wishlistitem=len(WishListItem.objects.filter(user=request.user))
    category=Category.objects.all()
    return render(request,'app/contact-us.html',locals())

def category(request,val):
    cartitem=0
    wishlistitem=0
    if request.user.is_authenticated:
        cartitem=len(Cart.objects.filter(user=request.user))
        wishlistitem=len(WishListItem.objects.filter(user=request.user))
    product=Product.objects.filter(category=val)
    c=Category.objects.filter(id=val)
    category=Category.objects.all()
    return render(request,'app/category.html',locals())

def product_detail(request,pk):
    cartitem=0
    wishlistitem=0
    if request.user.is_authenticated:
        cartitem=len(Cart.objects.filter(user=request.user))
        wishlistitem=len(WishListItem.objects.filter(user=request.user))
        wishlist=WishListItem.objects.filter(user=request.user, product=pk).exists()
    else:
        wishlist=False
    product=Product.objects.get(pk=pk)
    reduction=product.selling_price-product.discount_price
    percent=(reduction/product.selling_price)*100
    review=Review.objects.filter(product=pk)
    reviews = product.reviews.order_by('-created_at')[:5]
    average_rating = review.aggregate(Avg('rating'))['rating__avg']
    category=Category.objects.all()
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
        return redirect(product_detail, pk)
    
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.user == review.user:
        review.delete()
        return redirect(product_detail, pk) 

@login_required(login_url='login')
def profileview(request):
    cartitem=0
    wishlistitem=0
    if request.user.is_authenticated:
        cartitem=len(Cart.objects.filter(user=request.user))
        wishlistitem=len(WishListItem.objects.filter(user=request.user))
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
        category=Category.objects.all()
        return render(request,"app/profile-view.html", locals())

@login_required(login_url='login')
def address(request):
    cartitem=0
    wishlistitem=0
    if request.user.is_authenticated:
        cartitem=len(Cart.objects.filter(user=request.user))
        wishlistitem=len(WishListItem.objects.filter(user=request.user))
    add=Customer.objects.filter(user=request.user)
    category=Category.objects.all()
    return render(request,'app/address.html',locals()) 

@login_required(login_url='login')
def updateaddress(request,pk):
    cartitem=0
    wishlistitem=0
    if request.user.is_authenticated:
        cartitem=len(Cart.objects.filter(user=request.user))
        wishlistitem=len(WishListItem.objects.filter(user=request.user))
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
        category=Category.objects.all()
        return render(request,'app/address-update.html',locals())
    
@login_required(login_url='login')
def deleteaddress(request,pk):
    obj=Customer.objects.get(pk=pk)
    obj.delete()
    messages.warning(request,"Address deleted Successfully")
    return redirect('address')
    
#cart section
@login_required(login_url='login')
def add_to_cart(request):
    cartitem=0
    wishlistitem=0
    if request.user.is_authenticated:
        cartitem=len(Cart.objects.filter(user=request.user))
        wishlistitem=len(WishListItem.objects.filter(user=request.user))
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect(product_detail,product_id)


@login_required(login_url='login')
def show_cart(request):
    cartitem=0
    wishlistitem=0
    if request.user.is_authenticated:
        cartitem=len(Cart.objects.filter(user=request.user))
        wishlistitem=len(WishListItem.objects.filter(user=request.user))
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
    category=Category.objects.all()
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
    cartitem=0
    wishlistitem=0
    if request.user.is_authenticated:
        cartitem=len(Cart.objects.filter(user=request.user))
        wishlistitem=len(WishListItem.objects.filter(user=request.user))
    if request.method=='GET':
        user=request.user
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
        category=Category.objects.all()
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
        category=Category.objects.all()
        return redirect('order_success')
    else:
        messages.error(request, 'No items found in the cart.')
        return redirect('checkout')
    
def order_success(request):
    cartitem=0
    wishlistitem=0
    if request.user.is_authenticated:
        cartitem=len(Cart.objects.filter(user=request.user))
        wishlistitem=len(WishListItem.objects.filter(user=request.user))
    category=Category.objects.all()
    return render(request, 'app/order_placed.html',locals())

           
def orders(request):
    cartitem=0
    wishlistitem=0
    if request.user.is_authenticated:
        cartitem=len(Cart.objects.filter(user=request.user))
        wishlistitem=len(WishListItem.objects.filter(user=request.user))
    user=request.user
    order=OrderPlaced.objects.filter(user=user)
    category=Category.objects.all()
    return render(request, "app/orders.html", locals())

def wishlist(request):
    cartitem=0
    wishlistitem=0
    if request.user.is_authenticated:
        cartitem=len(Cart.objects.filter(user=request.user))
        wishlistitem=len(WishListItem.objects.filter(user=request.user))
    product=Product.objects.all()
    wishlist_items=WishListItem.objects.filter(user=request.user)
    category=Category.objects.all()
    return render(request,'app/wishlist.html',locals())

def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = WishListItem.objects.get_or_create(user=request.user,product=product)
    if created:
        pass
    return redirect(product_detail, product_id)

def remove_from_wishlist(request, wishlist_item_id):
    wishlist_item = get_object_or_404(WishListItem, id=wishlist_item_id, user=request.user)
    wishlist_item.delete()
    return redirect('wishlist')

def search_results(request):
    cartitem=0
    wishlistitem=0
    if request.user.is_authenticated:
        cartitem=len(Cart.objects.filter(user=request.user))
        wishlistitem=len(WishListItem.objects.filter(user=request.user))
    query=request.GET.get('search')
    if query:
        results=Product.objects.filter(
            models.Q(title__icontains=query) |
            models.Q(selling_price__icontains=query)
            )
    else:
        results=None
    category=Category.objects.all()
    return render(request,'app/search_results.html',locals())

    
#admin section
@login_required
def admin_dashboard(request):
    users=User.objects.all()
    orders=OrderPlaced.objects.all()
    return render(request,'admin/admin-dashboard.html',locals())
    
def add_banner(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        banner_image = request.FILES.get('banner_image')
        banner = Banner(title=title, banner_image=banner_image)
        banner.save()
        return redirect('add_banner') 
    else:
        banner=Banner.objects.all()
        return render(request, 'admin/add_banner.html',locals())
    
def delete_banner(request, banner_id):
    banner= get_object_or_404(Banner, id=banner_id)
    if request.method == 'POST':
        banner.delete()
    return redirect('add_banner') 
    
def add_category(request):
    if request.method == 'POST':
        id=request.POST.get('id')
        title = request.POST.get('title')
        category_image = request.FILES.get('category_image')
        category = Category(id=id,title=title, category_image=category_image)
        category.save()
        return redirect('add_category')  
    else:
        category=Category.objects.all()
        return render(request, 'admin/add_category.html',locals())
    
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
    return redirect('add_category')  
    
def add_brand(request):
    if request.method == 'POST':
        id=request.POST.get('id')
        brand_name=request.POST.get('brand_name')
        brand_logo=request.FILES.get('brand_logo')
        brand=Brand(id=id,brand_name=brand_name, brand_logo=brand_logo)
        brand.save()
        return redirect('add_brand')  
    else:
        brand=Brand.objects.all()
        return render(request, 'admin/add_brand.html',locals())

def delete_brand(request, brand_id):
    brand= get_object_or_404(Brand, id=brand_id)
    if request.method == 'POST':
        brand.delete()
    return redirect('add_brand') 

def add_product(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        selling_price = request.POST.get('selling_price')
        discount_price = request.POST.get('discount_price')
        description = request.POST.get('description')
        composition = request.POST.get('composition')
        category_id = request.POST.get('category')
        brand_id = request.POST.get('brand')
        quantity = request.POST.get('quantity')
        product_image = request.FILES.get('product_image')
        product = Product(
            title=title,
            selling_price=selling_price,
            discount_price=discount_price,
            description=description,
            composition=composition,
            category_id=category_id,
            brand_id=brand_id,
            quantity=quantity,
            product_image=product_image
        )
        product.save()
        return redirect('add_product')  
    else:
        brand=Brand.objects.all()
        category=Category.objects.all()
        product=Product.objects.all()
        return render(request, 'admin/add_product.html',locals())
    
def delete_product(request, product_id):
    product= get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
    return redirect('add_product')

def order_status(request):
    order=OrderPlaced.objects.all()
    return render(request,'admin/order_status.html', locals())

def update_order_status(request, order_id):
    order = get_object_or_404(OrderPlaced, id=order_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        order.status = status
        order.save()
        return redirect(order_status)  
    return render(request, 'admin_order_detail.html', locals())