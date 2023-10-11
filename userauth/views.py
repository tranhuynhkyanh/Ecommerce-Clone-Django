from django.shortcuts import render,redirect,get_object_or_404
from userauth.forms import UserRegisterForm,UserProfileForm,AddressEditForm
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.conf import settings
from core.models import Vendor,Product,Order,OrderItems,Address
from .models import Follow,User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

def handle_not_found(request, exception):
    return render(request, "404.html")
# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method=="POST":
        email = request.POST.get('your_name')
        password = request.POST.get('your_pass')
        try:
            user= User.objects.get(email=email)
        except:
            print("not exist")
            messages.warning(request,f"User with {email} does not exist")
        user = authenticate(request,email=email,password=password)
        if user is not None:
            print("Exist")
            login(request,user)
            messages.success(request,"You are logged in.")   
            return redirect("index")
        else:
            return render(request,'userauth/log-in.html')
    else:
        return render(request,'userauth/log-in.html')
    
@csrf_exempt
def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            repass = form.cleaned_data.get("password2")
            if password == repass:
                new_user = authenticate(username=username,email=email,password=password)
                login(request, new_user)
                messages.success(request, f'Your account was created!!')
                return redirect('index')
        
    else:
        form = UserRegisterForm()
    context = {
        'form': form
    }
    return render(request,"userauth/sign-up.html",context)
@login_required
def logout_view(request):   
    logout(request)
    return redirect('userauth:login')
@login_required
def follow(request,vid):
    user = request.user
    vendor = get_object_or_404(Vendor,vid=vid)
    try: 
        follow = Follow.objects.get(follower=user,following=vendor.user)
        follow.delete()
    except:
        follow = Follow.objects.create(follower=user,following=vendor.user)
        
    return redirect('vendor-detail',vendor.vid)
@login_required
def profile_view(request):
    try :
        vendor = Vendor.objects.get(user=request.user)
        products = Product.objects.filter(vendor=vendor).all()
        is_vendor = True
    except:
        products = {}
        is_vendor = False
    try:
        order = Order.objects.filter(user=request.user).all()
        
    except:
        order = {}
        item = {}
    user = User.objects.get(id = request.user.id)
    address = Address.objects.filter(user=user)
    context = {
        'is_vendor' : is_vendor,
        'products' : products,
        'orders': order,
        'user': user,
        'address': address
    }
    return render(request,"userauth/profile.html",context)
@login_required
def edit_profile(request):
    profile = User.objects.get(id=request.user.id)
    print(profile.first_name,profile.last_name,profile.image)
    address_user,created = Address.objects.get_or_create(user = request.user)
    if request.method == "POST":
        user_form = UserProfileForm(request.POST,request.FILES)
        address_form = AddressEditForm(request.POST)
        if user_form.is_valid() or address_form.is_valid():
            first_name = user_form.cleaned_data.get("first_name")
            last_name = user_form.cleaned_data.get("last_name")
            address= address_form.cleaned_data.get("address")
            phone= address_form.cleaned_data.get("phone")
            image = user_form.cleaned_data.get("image")
            print(first_name,last_name,address,phone)
            profile.first_name = first_name
            profile.last_name= last_name
            profile.image = image
            profile.save()
            address_user.address= address
            address_user.phone = phone
            address_user.save()
            vendor = Vendor.objects.get(user=request.user)
            products = Product.objects.filter(vendor=vendor).all()
            orders = Order.objects.filter(user=request.user).all()
            
            context = {
                'is_vendor' : True,
                'user' : request.user,
                'products' : products,
                'orders': orders,
                'address': address_user
               
            }
            return render(request,"userauth/profile.html",context)
    else:
        user_form = UserProfileForm()
        address_form = AddressEditForm()
    if created == False:
        address_user = {}
    context = {
        'profile':profile,
        'address': address_user,
        'user_form' : user_form,
        'address_form': address_form
    }
    return render(request,"userauth/profile-update.html",context)

def update_product_vendor(request):
    pass
def register_vendor(request):
    pass

def MessageView(request):
    return render(request,"chat.html")