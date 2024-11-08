from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('register',views.Register,name='register'),
    path('log_in',views.LogIn,name='log_in'),
    path('log_out',views.LogOut,name='log_out'),
    path('addtocart',views.add_to_cart,name='addtocart'),
    path('addtofavourite',views.add_to_fav,name='addtofavourite'),
    path('Collections',views.Collections,name='collections'),
    path('Collection/<str:cslug>',views.ViewProducts,name='Products'),
    path('Product_Details/<str:cslug>/<str:pslug>',views.ProductDetails,name='product_details'),
    path('cart',views.viewCart,name='cart'),
    path('favourite',views.viewFavourite,name='favourite'),
    path('deleteCartItem/<int:cid>',views.Delete_Cart_Item,name='deleteCartItem'),
    path('deleteFavItem/<int:fid>',views.Delete_Favourite_Item,name='deleteFavItem'),
]