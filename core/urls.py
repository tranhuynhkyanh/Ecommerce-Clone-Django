from django.urls import path,include
from .views import index,StoreView,ProductView,VendorView,CategoryView,CartView,CheckoutView,OrderDetailView,PayMentCompletedView,WishListView
from .function import search,search_vendor,filter_product,check_product,add_to_cart,delete_from_cart,update_from_cart,order_create,add_review,delete_order,add_to_wishlist,remove_from_wishlist
urlpatterns = [
    path("",index,name="index"),

    path("store/",StoreView,name="store"),
    path("filter-product/",filter_product,name="filter-product"),

    path("product/<pid>/",ProductView,name="product-detail"),
    path("check-product/",check_product,name="check-product"),
    path("add-to-cart/",add_to_cart,name="add-to-cart"),
    path("add-review/",add_review,name="add-review"),

    path("shop/<vid>/",VendorView,name="vendor-detail"),
    path("category/<cid>",CategoryView,name="category-detail"),


    path("cart/",CartView,name="cart-detail"),
    path("<pid>/delete-from-cart/",delete_from_cart,name="delete"),
    path("update-from-cart/",update_from_cart,name="update"),

    path("search/",search,name="search"),
    path("searchVendor/",search_vendor,name="searchVendor"),

    path("checkout/",CheckoutView,name="checkout"),
    path("order/",order_create,name="order"),
    path("order-detail/<invoice>",OrderDetailView,name="order-detail"),
    path("delete-order/<invoice>",delete_order,name="delete-order"),
    path("paypal/",include("paypal.standard.ipn.urls")),
    path("payment-completed/",PayMentCompletedView,name="payment-completed"),

    path("wishlist",WishListView,name="wishlist"),
    path("add-to-wishlist/",add_to_wishlist,name="add-to-wishlist"),
    path("remove-from-wishlist/<pid>",remove_from_wishlist,name="remove-from-wishlist")
]
