from django.shortcuts import render,get_object_or_404,redirect
from django.template.loader import render_to_string
from .models import Product,ProductImages,Vendor,Category,Order,OrderItems,Cart,ProductInventory,ProductCart,Address,ProductReview,Wishlist
from django.db.models import Q
from django.http import JsonResponse
from userauth.models import Follow
from django.contrib import messages
from django.db.models import Avg
from django.contrib.auth.decorators import login_required


#------------------------------------------------------- Product ----------------------------------------------------------------#
#------------------------------------------------------- Product ----------------------------------------------------------------#
@login_required
def add_review(request):
    pid = request.GET.get("pid")
    product = Product.objects.get(pid=pid)
    orders = Order.objects.filter(user=request.user).all()
    is_buy = OrderItems.objects.filter(item=product).filter(order__in=orders).first()
    if is_buy:
        is_reviewed = ProductReview.objects.filter(user=request.user,product=product).first()
        if not is_reviewed:
            review = request.GET.get("review")
            rating = request.GET.get("stars")
            ProductReview.objects.create(user=request.user,product=product,review = review,rating=rating)
            return JsonResponse({'message':"Review completed"})
        else:
            return JsonResponse({'message':"Already had reviewed"})
    else:
        return JsonResponse({'message':"You need to buy this before"})

@login_required
def filter_product(request):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")
    products= Product.objects.all()
    if len(categories)>0:
        products = products.filter(category__id__in=categories).distinct()
    if len(vendors)>0:
        products = products.filter(vendor__id__in=vendors).distinct()
    data = render_to_string("filtered/product-list.html",{'products':products})
    return JsonResponse({'data':data})

@login_required
def check_product(request):
    pid =  request.GET.get("pid") 
    qty = request.GET.get("qty") 
    product = get_object_or_404(Product,pid=pid)
    product_inventory = ProductInventory.objects.get(product=product)
    qty_product = product_inventory.get_qty()
    print(pid,qty)
    if qty_product < int(qty):
        messages = "Số lượng vượt quá kho hàng !!! Vui lòng chọn ít hơn " + str(qty_product+1)
    else:
        messages = ""
    price = product.price * int(qty)
    return JsonResponse({'messages':messages,
                         'price':price})
@login_required
def add_to_wishlist(request,pid):
    
    return

def get_rating(reviews):
    ratings = [0,0,0,0,0]
    for review in reviews:
        ratings[review.rating-1] += 1
    return ratings

#------------------------------------------------------- Search ----------------------------------------------------------------#
#------------------------------------------------------- Search ----------------------------------------------------------------#

def search(request):
    query = request.GET.get("q", "")
    if query == "":
        return JsonResponse({'results': []})
    products = Product.objects.filter(
        Q(title__icontains=query)
    )
    response = {
        "results": [
            {
                "id": product.pid,
                "title": product.title,
                "image": product.image.url,
                "price":product.price,
                "url":product.get_absolute_url(),
            }
            for product in products
        ]
    }

    return JsonResponse(response)

def search_vendor(request):
    query = request.GET.get("q", "")
    title = request.GET.get("vendor")
    if query == "":
        return JsonResponse({'results': []})
    vendor = get_object_or_404(Vendor,title=title)
    product = Product.objects.filter(vendor=vendor).all()
    products = product.filter(
        Q(title__icontains=query)
    )
    response = {
        "results": [
            {
                "id": product.pid,
                "title": product.title,
                "image": product.image.url,
                "price":product.price,
                "url":product.get_absolute_url(),
            }
            for product in products
        ]
    }

    return JsonResponse(response)

#------------------------------------------------------- Cart ----------------------------------------------------------------#
#------------------------------------------------------- Cart ----------------------------------------------------------------#
@login_required
def add_to_cart(request):
    
    qty = request.GET.get('qty')
    pid = request.GET.get('pid')
   # print(qty,pid)
    product = get_object_or_404(Product,pid=pid)
    price = int(qty) * int(product.price)
    cart = Cart.objects.filter(user=request.user).first()
    print(cart)
    if not cart :
        cart = Cart.objects.create(user=request.user)
    is_add = ProductCart.objects.filter(product=product,user=request.user).first()
    if not is_add:
        product_cart = ProductCart.objects.create(product=product,qty=qty,price=price,user=request.user)
        cart.product.add(product_cart) 
    else :
        is_add.qty += int(qty)
        is_add.price += int(price)
        is_add.save()
    cart.save()
    messages.success(request, "Đã thêm sản phẩm vào giỏ hàng!")
    return JsonResponse({'messages':"Đã thêm sản phẩm vào giỏ hàng!"})
@login_required
def delete_from_cart(request,pid):
    product = get_object_or_404(Product,pid=pid)
    cart = Cart.objects.filter(user=request.user).first()
    products = cart.product.all()
    product_remove = products.get(product=product)
    product_remove.delete()
    return render(request,'cart-order.html',{"cartItems":products})
@login_required
def update_from_cart(request):
    qty = request.GET.get('qty')
    pid = request.GET.get('pid')
    product = get_object_or_404(Product,pid=pid)
    price = int(qty) * int(product.price)
    is_add = ProductCart.objects.filter(product=product).first()
    is_add.qty = qty
    is_add.price = price
    is_add.save()
    cart = Cart.objects.filter(user=request.user).first()
    products = cart.product.all()
    return render(request,'cart-order.html',{"cartItems":products})

#------------------------------------------------------- Order ----------------------------------------------------------------#
#------------------------------------------------------- Order ----------------------------------------------------------------#
@login_required
def order_create(request):
    cart = Cart.objects.filter(user=request.user).first()
    address = Address.objects.filter(user= request.user).first()
    if cart:
        total_price = 0
        invoice = "INVOICE_NO-" + str(Order.objects.count())
        products = cart.product.all()
        order = Order.objects.create(
            user=request.user,
            invoice_no=invoice,
            price= total_price,
            product_status="Processing",
            destination = address,
            image = products[0].product.image,
            )
        for product in products:
            inventory = ProductInventory.get(product=product)
            inventory.quantity -= product.qty
            inventory.save()
            OrderItems.objects.create(
                order = order,
                item = product.product,
                image = product.product.image,
                quantity = product.qty,
                price = (product.price/product.qty),
                total = product.price
            )
            ProductCart.objects.filter(product=product.product,user=request.user).first().delete()
            total_price += product.price
        
        order.price = total_price
        order.save()
        cart.delete()

        order_items = OrderItems.objects.filter(order=order).all()
        context = {
            "order":order,
            "order_items":order_items
        }
        return render(request,"payment-completed.html",context)
    else:
        return redirect('index')
    

