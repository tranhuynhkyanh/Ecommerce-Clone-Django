from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from django.template.loader import render_to_string
from .models import Product,ProductImages,Vendor,Category,Order,OrderItems,Cart,ProductInventory,ProductCart,Address,ProductReview,Wishlist
from django.db.models import Q
from django.http import JsonResponse
from userauth.models import Follow
from django.contrib import messages
from django.db.models import Avg
from .function import get_rating
from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    new_product = Product.objects.all().order_by('-id')
    context = {
        'new_products' : new_product
    }
    return render(request,'index.html',context)


                    ### -------------------------       Url: /store  ----------------------- ###
@login_required
def StoreView(request):
    products = Product.objects.all()
    category = Category.objects.all()
    brand = Vendor.objects.all()
    
    context ={
        'products' : products,
        'categories' : category,
        'brands': brand
    }
    return render(request,'store.html',context)

@login_required
def CategoryView(request,cid):
    category = get_object_or_404(Category,cid=cid)
    products = Product.objects.filter(category=category).all()
    context ={
        'products' : products,
        'categories': {},
        'category_': category
    }

    return render(request,'store.html',context)
@login_required
def ProductView(request,pid):
    product = get_object_or_404(Product,pid=pid)
    cate = product.category
    product_images = ProductImages.objects.filter(product=product).first()
    product_related = Product.objects.filter(category=cate).exclude(pid=pid).all()
    vendor = Vendor.objects.filter(product=product).first()
    reviews = ProductReview.objects.filter(product=product).all()
    rating = reviews.aggregate(Avg('rating'))
    ratings = get_rating(reviews)
    context = {
        'product': product,
        'imgs'  : product_images,
        'vendor' : vendor,
        'products_related' : product_related,
        'cate' : cate,
        'reviews': reviews,
        'rating': rating,
        'range' : range(5),
        'ratings': ratings
    }
    return render(request,'product.html',context)


@login_required
def VendorView(request,vid):
    vendor = get_object_or_404(Vendor,vid=vid)
    if request.user != vendor.user:
        products = Product.objects.filter(vendor=vendor).all()
        new_products = Product.objects.filter(vendor=vendor).all().order_by("-id")
        items_sell = OrderItems.objects.all()
        try : 
            is_followed = Follow.objects.get(follower=request.user,following=vendor.user)
            is_followed = True
        except:
            is_followed = False
        context = {
            'vendor' : vendor,
            'products' : products,
            'is_followed': is_followed,
            'new_products': new_products,
        }
        return render (request,'vendor.html',context)



                    ### ----------------            Search            --------------- ####

                            ### <----------------            Search            ---------------> ####


@login_required
def CartView(request):
    try :
        cart_items = Cart.objects.filter(user=request.user).first()
        products = cart_items.product.all()
    except:
        products = {}
    context = {
        'cartItems' : products
    }
    return render(request,'cart-order.html',context)

@login_required
def CheckoutView(request):
    try:
        cart = Cart.objects.filter(user=request.user).first()
        products = cart.product.all()
        address = Address.objects.get(user=request.user)
        total_price = 0
        for product in products:
            total_price += product.price
        host = request.get_host()
        paypal_dict = {
        "business": "thkyanhlxag@gmail.com",
        "amount": 1,
        "item_name": "Testing",
        "invoice": "",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment-completed')),
        "cancel_return": request.build_absolute_uri(reverse('index')),
         }
        form = PayPalPaymentsForm(initial=paypal_dict)
    except:
        products = {}
        total_price = 0
    context = {
        'products' : products,
        'price': total_price,
        'address':address,
        'form' : form
    }
    return render (request,"checkout.html",context)


@login_required
def OrderDetailView(request,invoice):
    order = Order.objects.get(invoice_no = invoice)
    order_items = OrderItems.objects.filter(order=order).all()

    context = {
        "order":order,
        "order_items":order_items,
        'form':form
    }
    return render(request,"payment-completed.html",context)
@login_required
def PayMentCompletedView(request):
    context= request.POST

    return render(request,"payment-completed.html",{'context':context})
