from django.shortcuts import render,get_object_or_404,redirect
from django.template.loader import render_to_string
from .models import Product,ProductImages,Vendor,Category,Order,OrderItems,Cart,ProductInventory,ProductCart,Address,ProductReview,Wishlist
from django.db.models import Q,Count, Window,Sum,Case,When
from django.core.paginator import Paginator,Paginator, EmptyPage, PageNotAnInteger
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


def filter_product(request):
    categories = request.GET.getlist("filter_category[]")
    vendors = request.GET.getlist("filter_vendor[]")
    products= Product.objects.all()
    sort = request.GET.get("sort")
    price_min = request.GET.get("priceMin").replace(".00","") if request.GET.get("priceMin") else 10000
    price_max = request.GET.get("priceMax").replace(".00","") if request.GET.get("priceMax") else 10000000
    products = Product.objects.filter(Q(price__range=(price_min, price_max), old_price__isnull=False) | Q(old_price__range=(price_min, price_max)))

   
    if len(categories)>0:
        products = products.filter(category__id__in=categories)
    if len(vendors)>0:
        products = products.filter(vendor__id__in=vendors)
    if sort == "0":
       
        products= products.order_by(Case(
            When(price__isnull=False,then="price"),
            default ="old_price"))  
    else:
       
        products= products.order_by(-Case(
            When(price__isnull=False,then="price"),
            default ="old_price"))
    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, show the first page
        paginated_products = paginator.page(1)

    except EmptyPage:
        # If the page is out of range, show the last page
        paginated_products = paginator.page(paginator.num_pages)
    if 'page=' in request.get_full_path():
        category_q = Category.objects.filter(id__in=categories).values_list("cid",flat=True)
        vendor_q = Vendor.objects.filter(id__in=vendors).values_list("vid",flat=True)
        category = Category.objects.all()
        brand = Vendor.objects.all()
        top_products = top_selling()
        price = [price_min,price_max]
        context ={
        'vendor_q': vendor_q,
        'category_q' : category_q,
        'products' : paginated_products,
        'categories' : category,
        'brands': brand,
        'tops': top_products,
        'price_q':price,
        'sort':sort
         }
        return render(request,"filtered/store-filter.html",context=context)
    else:
        data = render_to_string("filtered/product-list.html",{'products':paginated_products},request=request)
        return JsonResponse({'data':data})

def filter_price(request):
    pass
    #data = render_to_string("filtered/product-list.html",{'products':products})
    #return JsonResponse({'data':data})

def top_selling():
    order_items = OrderItems.objects.annotate(
        quantity_ordered=Count('quantity'),
        rank=Window(expression=Count('quantity'), order_by=Count('quantity').desc())
    ).order_by('-rank')
    return Product.objects.filter(id__in=order_items.values_list('item'))

@login_required
def check_product(request):
    pid =  request.GET.get("pid") 
    qty = request.GET.get("qty") 
    mode = request.GET.get("mode")
    product = get_object_or_404(Product,pid=pid)
    #Check if cart:
    if mode == "1":
        product_inven_cart = 0
    else:
        product_in_cart = get_object_or_404(ProductCart,user=request.user,product=product)
        product_inven_cart = product_in_cart.qty if product_in_cart else 0
    product_inventory = ProductInventory.objects.get(product=product)
    qty_product = product_inventory.get_qty()
    print(pid,qty)
    if qty_product < int(qty) + product_inven_cart :
        messages = "Số lượng vượt quá kho hàng !!! Vui lòng chọn ít hơn " + str(qty_product+1) if product_inven_cart ==0 else "Số lượng kho không đủ nếu thêm! Kiểm tra số lượng sản phẩm trong giỏ hàng."
    else:
        messages = ""
    if product.price != None:
        price = int(qty) * int(product.price)
    else:
        price = int(qty) * int(product.old_price)
    return JsonResponse({'messages':messages,
                         'price':price})


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
                "image": product.image.url if product.image else product.image_url,
                "price":product.price if product.price else product.old_price,
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
                "image": product.image.url if product.image else product.image_url,
                "price":product.price if product.price else product.old_price,
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
    if product.price != None:
        price = int(qty) * int(product.price)
    else:
        price = int(qty) * int(product.old_price)
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
    if product.price != None:
        price = int(qty) * int(product.price)
    else:
        price = int(qty) * int(product.old_price)
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
            image = products[0].product.image if products[0].product.image else products[0].product.image_url,
            )
        for product in products:
            inventory = ProductInventory.objects.get(product=product.product)
            inventory.quantity -= product.qty
            inventory.save()
            if inventory == 0:
                product.product.in_stock= False
            if product.price != None:
                price = product.price
            else:
                price = product.old_price
            OrderItems.objects.create(
                order = order,
                item = product.product,
                image = product.product.image,
                quantity = product.qty,
                price = (price/product.qty),
                total = price
            )
            ProductCart.objects.filter(product=product.product,user=request.user).first().delete()
            total_price += price
        
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
    
def delete_order(request,invoice):
    order = Order.objects.get(invoice_no=invoice)
    order_items = OrderItems.objects.filter(order=order)
    for item in order_items:
        product_restock = ProductInventory.objects.get(product=item.item)
        product_restock.quantity += item.quantity
        product_restock.save()
    order.delete()
    
    return redirect("userauth:profile")

@login_required
def add_to_wishlist(request):
    pid = request.GET.get('pid')
    w = Wishlist.objects.filter(product=Product.objects.get(pid=pid),user=request.user)
    if not w:
        Wishlist.objects.create(product=Product.objects.get(pid=pid),user=request.user)

    return JsonResponse({"message":"Da them san pham vao danh sach yeu thich"}) 

@login_required
def remove_from_wishlist(request,pid):
    product_remove = Wishlist.objects.get(product=Product.objects.get(pid=pid))
    product_remove.delete()
    return redirect("wishlist")

def get_vendor_review(request,vid):
    reviews = ProductReview.objects.filter(product__in=Product.objects.filter(vendor=Vendor.objects.get(vid=vid)).all())
    print(reviews)