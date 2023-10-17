from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from django.template.loader import render_to_string
from .models import Product,ProductImages,Vendor,Category,Order,OrderItems,Cart,ProductInventory,ProductCart,Address,ProductReview,Wishlist
from django.db.models import Q
from django.http import JsonResponse
from userauth.models import Follow
from django.contrib import messages
from django.db.models import Avg,Sum
from .function import get_rating,top_selling
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def index(request):
    new_product = Product.objects.all().order_by('-id')
    category = Category.objects.all()
    tops = top_selling()
    context = {
        'new_products' : new_product,
        'categories' : category,
        'tops' : tops
    }
    return render(request,'index.html',context)


                    ### -------------------------       Url: /store  ----------------------- ###

def StoreView(request):
    products = Product.objects.all()
    category = Category.objects.all()
    brand = Vendor.objects.all()
    paginator = Paginator(products,9)

    top_products = top_selling()
    # Get the requested page number
    page = request.GET.get('page')
    
    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, show the first page
        paginated_products = paginator.page(1)

    except EmptyPage:
        # If the page is out of range, show the last page
        paginated_products = paginator.page(paginator.num_pages)
    context ={
        'products' : paginated_products,
        'categories' : category,
        'brands': brand,
        'tops': top_products,
 
    }
    return render(request,'store.html',context)


def CategoryView(request,cid):
    category = get_object_or_404(Category,cid=cid)
    products = Product.objects.filter(category=category).all()
    top_products = top_selling()
    context ={
        'products' : products,
        'categories': {},
        'category_': category,
        'tops': top_products
    }

    return render(request,'store.html',context)

def ProductView(request,pid):
    product = get_object_or_404(Product,pid=pid)
    cate = product.category
    product_images = ProductImages.objects.filter(product=product).first()
    product_related = Product.objects.filter(category=cate).exclude(pid=pid).all()
    vendor = Vendor.objects.filter(product=product).first()
    reviews = ProductReview.objects.filter(product=product).all()
    paginator = Paginator(reviews,3)
    page = request.GET.get('page')
    
    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, show the first page
        paginated_products = paginator.page(1)

    except EmptyPage:
        # If the page is out of range, show the last page
        paginated_products = paginator.page(paginator.num_pages)

    rating = reviews.aggregate(Avg('rating'))
    inventory = ProductInventory.objects.get(product=product)
    if inventory.quantity == 0:
        product.in_stock = False
    product.save()
    ratings = get_rating(reviews)
    sold = OrderItems.objects.filter(item=product).values('quantity').aggregate(Sum('quantity'))['quantity__sum']
    try:
        percentage = ProductReview.get_percentage(reviews)
    except:
        percentage = {}
    context = {
        'sold':sold if sold else 0,
        'product': product,
        'imgs'  : product_images,
        'vendor' : vendor,
        'products_related' : product_related,
        'cate' : cate,
        'reviews': paginated_products,
        'rating': rating,
        'range' : range(5),
        'ratings': ratings,
        'percentage': percentage,
        'inventory' : inventory
    }
    return render(request,'product.html',context)



def VendorView(request,vid):
    vendor = get_object_or_404(Vendor,vid=vid)
    if request.user != vendor.user:
        review_vendor = ProductReview.objects.filter(product__in=Product.objects.filter(vendor=vendor)).aggregate(Avg('rating'))
        total_review = ProductReview.objects.filter(product__in=Product.objects.filter(vendor=vendor)).all().count()
        total_sold = OrderItems.objects.filter(item__in=Product.objects.filter(vendor=vendor)).values('quantity').aggregate(Sum('quantity'))['quantity__sum']
        products = Product.objects.filter(vendor=vendor).all()
        paginator = Paginator(products, 9)

        # Get the requested page number
        page = request.GET.get('page')

        try:
            paginated_products = paginator.page(page)
        except PageNotAnInteger:
            # If the page parameter is not an integer, show the first page
            paginated_products = paginator.page(1)

        except EmptyPage:
            # If the page is out of range, show the last page
            paginated_products = paginator.page(paginator.num_pages)
        new_products = Product.objects.filter(vendor=vendor).all().order_by("-id")
        items_sell = OrderItems.objects.all()
        try : 
            is_followed = Follow.objects.get(follower=request.user,following=vendor.user)
            is_followed = True
        except:
            is_followed = False
        context = {
            'total_review':total_review if total_review else 0,
            'vendor' : vendor,
            'products' : paginated_products,
            'is_followed': is_followed,
            'new_products': new_products,
            'review_vendor': review_vendor if not review_vendor else 0,
            'total_sold' : total_sold if total_sold else 0,
 
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
            if product.price != None:
                total_price += product.price
            else:
                total_price += product.old_price
    except:
        products = {}
        total_price = 0
    context = {
        'products' : products,
        'price': total_price,
        'address':address,
    }
    return render (request,"checkout.html",context)


@login_required
def OrderDetailView(request,invoice):
    order = Order.objects.get(invoice_no = invoice)
    order_items = OrderItems.objects.filter(order=order).all()

    context = {
        "order":order,
        "order_items":order_items,
    }
    return render(request,"payment-completed.html",context)
@login_required
def PayMentCompletedView(request):
    context= request.POST

    return render(request,"payment-completed.html",{'context':context})
@login_required
def WishListView(request):
    products = Product.objects.filter(id__in=Wishlist.objects.filter(user=request.user).values_list('product'))
    context = {
        'products': products
    }
    return render(request,"wishlist.html",context)