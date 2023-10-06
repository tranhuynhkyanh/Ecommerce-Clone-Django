from django.db import models
import uuid
from userauth.models import User
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from django.urls import reverse
STATUS_CHOICE = (
    ('process','Processing'),
    ('shipped','Shipped'),
    ('delivered','Delivered')
)
STATUS = (
    ('draft','Draft'),
    ('disable','Disabled'),
    ('rejected','Rejected')
)
RATING = (
    (1,'★☆☆☆☆'),
    (2,'★★☆☆☆'),
    (3,'★★★☆☆'),
    (4,'★★★★☆'),
    (5,'★★★★★')
)
# Create your models here.

def user_directory_path(instance,filename):
    return 'user_{0}/{1}'.format(instance.id,filename)

             # -------------------------     Tag --------------------------------#
             # -------------------------     Tag --------------------------------#
             # -------------------------     Tag --------------------------------#
class Tag(models.Model):
    title = models.CharField(max_length=75,verbose_name="Tag")
    slug = models.SlugField(null=False,unique=True)

    def get_absolute_url(self):
        return reverse("tags", kwargs={"slug": self.slug})
    
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "Tags"
     
            # -------------------------     Vendor --------------------------------#
            # -------------------------     Vendor --------------------------------#
            # -------------------------     Vendor --------------------------------#
class Vendor(models.Model):
    vid =  ShortUUIDField(unique = True,length = 10,max_length=20,prefix="ven",alphabet="abcdefgh123456")
    title = models.CharField(max_length=100)
    image= models.ImageField(upload_to=user_directory_path)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=100,default='113 Vo Thi Sau Street.')
    contact = models.CharField(max_length=100,default='+84 (39) 7581458')
    chat_resp_time = models.CharField(max_length=100,default="100")
    shipping_on_time = models.CharField(max_length=100,default="100")
    rating = models.CharField(max_length=100,default="100")
    days_return = models.CharField(max_length=100,default="100")
    class Meta:
        verbose_name_plural = "Vendors"
    def vendor_image(self):
        return mark_safe('<img src="%s width="50" height="50" />' % (self.image.url))        
             # -------------------------     Category --------------------------------#
             # -------------------------     Category --------------------------------#
             # -------------------------     Category --------------------------------#

class Category(models.Model):
    cid =  ShortUUIDField(unique = True,length = 10,max_length=20,prefix="cat",alphabet="abcdefgh123456")
    title = models.CharField(max_length=100)
    image= models.ImageField(upload_to="category")
    class Meta:
        verbose_name_plural = "Categories"
    def category_image(self):
        return mark_safe('<img src="%s width="50" height="50" />' % (self.image.url))
    def __str__(self):
        return self.title   
    

             # -------------------------    Product, Product Inventory, Product Images --------------------------------#
             # -------------------------    Product, Product Inventory, Product Images --------------------------------#
             # -------------------------    Product, Product Inventory, Product Images --------------------------------#
class Product(models.Model):
    pid =  ShortUUIDField(unique = True,length = 10,max_length=20,prefix="pro",alphabet="abcdefgh123456")
    title = models.CharField(max_length=100,default="MSI Laptop")
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,db_constraint=False)
    image = models.ImageField(upload_to=user_directory_path,default="MSILaptop.jpg")
    description = models.CharField(blank=True,default="This is the product",max_length=300)
    price = models.DecimalField(max_digits=999999999,decimal_places=0,default=1000)
    old_price = models.DecimalField(max_digits=999999999,decimal_places=0,default=2000)
    specifications = models.TextField(null=True,blank=True)
    tags = models.ManyToManyField(Tag)
    product_status = models.TextField(choices=STATUS,max_length=10,default="Draft",null=True)
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=True)
    digital = models.BooleanField(default=True)
    sku = ShortUUIDField(unique = True,length = 4,max_length=20,prefix="sku",alphabet="1234567890")
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE,null=True)
    autocomplete_fields = ["title"]
    class Meta:
        verbose_name_plural = "Products"
    def product_image(self):
        return mark_safe('<img src="%s width="50" height="50" />' % (self.image.url))
    def __str__(self):
        return self.title
    def get_percentage_discount(self):
        return (self.old_price / self.price) * 100
    def get_absolute_url(self):
        return reverse("product-detail", kwargs={"pid": self.pid})

    

class ProductInventory(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(auto_now_add=True)
    def get_qty(self):
        return self.quantity
class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-images",default="product.jpg")
    product= models.OneToOneField(Product,on_delete=models.SET_NULL,null=True)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Product Images"

             # -------------------------     CartOder , CartOderItem --------------------------------#
             # -------------------------     CartOder , CartOderItem --------------------------------#
             # -------------------------     CartOder , CartOderItem --------------------------------#

class ProductCart(models.Model):
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=9999999999999999,decimal_places=0,default=2000)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ManyToManyField(ProductCart)

class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    address = models.CharField(max_length=100,null=True)
    phone = models.BigIntegerField(null=True)
    status = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Address"


class Order(models.Model):
    invoice_no = models.CharField(max_length=200)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9999999999999999,decimal_places=0,default=2000)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.TextField(choices=STATUS_CHOICE,max_length=30)
    destination = models.ForeignKey(Address,on_delete=models.CASCADE)
    image = models.ImageField(max_length=200,null=True)
    class Meta:
        verbose_name_plural = "Orders"

class OrderItems(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    item = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(max_length=200)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=99999999999999,decimal_places=0,default=1000)
    total = models.DecimalField(max_digits=99999999999999,decimal_places=0,default=1000)
    
    class Meta:
        verbose_name_plural = "Order Items"
    def product_image(self):
        return mark_safe('<img src="%s width="50" height="50" />' % (self.image.url))
    def get_user(self):
        return self.order.user
             # -------------------------     Product Review, Wishlist, Address --------------------------------#
             # -------------------------     Product Review, Wishlist, Address --------------------------------#
             # -------------------------     Product Review, Wishlist, Address --------------------------------#

class ProductReview(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING,default=None)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Product Reviews"
    def __str__(self):
        return self.product.title
    def get_rating(self):
        return self.rating

class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Wishlists"

