from django.contrib import admin
from .models import Product, Category, Vendor, ProductImages,ProductReview, Order,OrderItems,Wishlist,Address,Tag,ProductInventory,ProductCart,Cart
# Register your models here.

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['title','price','vendor','featured','in_stock']

class ProductInventoryAdmin(admin.ModelAdmin):
    list_display = ['product','quantity']

class TagAdmin(admin.ModelAdmin):
    list_display = ['title','slug']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','category_image']
     
class VendorAdmin(admin.ModelAdmin):
    list_display = ['title','vendor_image']

class OrderAdmin(admin.ModelAdmin):
    list_editable = ['paid_status','product_status']
    list_display = ['user','invoice_no','price','paid_status','order_date','product_status','destination']

class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order','item','image','quantity','price','total']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user','product','review','rating']

class WishListAdmin(admin.ModelAdmin):
    list_display = ['user','product','date']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user','address','status']

class ProductCartAdmin(admin.ModelAdmin):
    list_display = ['product','qty','price']


admin.site.register(Product,ProductAdmin)
admin.site.register(ProductInventory,ProductInventoryAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Vendor,VendorAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItems,OrderItemsAdmin)
admin.site.register(ProductReview,ProductReviewAdmin)
admin.site.register(Wishlist,WishListAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(ProductCart,ProductCartAdmin)
admin.site.register(Cart)