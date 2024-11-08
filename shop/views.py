from django.shortcuts import render, redirect, get_object_or_404
from . models import *
from django.contrib import messages
from .forms import CustumUserForm
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import json

def home(request):
    offered_products = Products.objects.filter(trending=True,status=0)
    return render(request,"shop/index.html",{'Offered_Products':offered_products})

def Register(request):
    form = CustumUserForm()
    if request.method=='POST':
        form=CustumUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registration Success you can login now...!')
            return redirect('log_in')
    return render(request,"shop/register.html",{'form':form})

def LogIn(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method=='POST':
            name=request.POST.get('username')
            pwd=request.POST.get('password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,'Logged in Successfully')
            else:
                messages.error(request,'Invalid Username or Password')
                return redirect('log_in')
            return redirect('/')
        return render(request,"shop/login.html")

def LogOut(request):
    if request.user.is_authenticated:
        logout(request)
        messages.warning(request,'You are Logged Out ...!')
    return redirect('/')
 
def add_to_cart(request):
    if request.headers.get("X-Request-With")=="XMLHttpRequest":
        if request.user.is_authenticated:
            data = json.load(request)
            product_id = (data['pid'])
            product_qty = (data['qty'])
            user_id = (request.user.id)
            product_status = Products.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user_id=user_id,product_id=product_id):
                    return JsonResponse({'status':'Product Alrady in cart'}, status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user_id=user_id,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status':'Product added to cart Successfully'}, status=200)
                    else:
                        return JsonResponse({'status':'Product Quantity not available'}, status=200)
            else:
                return JsonResponse({'status':'Product is not available'}, status=200)
        else:
            return JsonResponse({'status':'Lodin to add to cart'}, status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)

def add_to_fav(request):
    if request.headers.get("X-Request-With")=="XMLHttpRequest":
        if request.user.is_authenticated:
            data = json.load(request)
            product_id = (data['pid'])
            user_id = (request.user.id)
            product_status = Products.objects.get(id=product_id)
            if product_status:
                if Favourite.objects.filter(user_id=user_id,product_id=product_id):
                    return JsonResponse({'status':'Product Alrady in Favourite'}, status=200)
                else:
                    Favourite.objects.create(user_id=user_id,product_id=product_id)
                    return JsonResponse({'status':'Product added to Favourite Successfully'}, status=200)
            else:
                return JsonResponse({'status':'Product is not available'}, status=200)
        else:
            return JsonResponse({'status':'Lodin to add to Favourite'}, status=200)
    else:
        return JsonResponse({'status':'Invalid Access'}, status=200)

def Collections(request): 
    category = Category.objects.filter(status=0)
    supcategory = SuperCategory.objects.filter(status=0)
    return render(request,"shop/collections.html",{'Category':category,'SupCategory':supcategory})

def ViewProducts(request,cslug):
    if (Category.objects.filter(slug=cslug,status=0)):
        category_obj = Category.objects.get(slug=cslug)
        products = Products.objects.filter(category_id=category_obj.id,status=0)
        return render(request,"shop/Products/products.html",{'Products':products, 'CategoryName':category_obj.name})
    else:
        messages.warning(request,"No such Category Found")
        return redirect("collections")

def ProductDetails(request, cslug, pslug):
    try:
        category = Category.objects.get(slug=cslug, status=0)
    except Category.DoesNotExist:
        messages.warning(request, "No such Category Found")
        return redirect("collections")

    try:
        product = Products.objects.get(slug=pslug, status=0)
    except Products.DoesNotExist:
        messages.warning(request, "No such Product Found")
        return redirect("collections")
    
    return render(request, "shop/Products/prod_detail.html", {'Product': product})

#def ProductDetails(request,cslug,pslug):
#    if (Category.objects.get(slug=cslug,status=0)):
#        if (Products.objects.get(slug=pslug, status=0)):
#            product_obj = Products.objects.get(slug=pslug, status=0)
#            product = Products.objects.get(id=product_obj.id, status=0)
#            return render(request,"shop/Products/prod_detail.html",{'Product':product})
#        else:
#            messages.warning(request,"No such Product Found")
#            return redirect("collections")   
#    else:
#        messages.warning(request,"No such Category Found")
#        return redirect("collections")

def viewCart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user_id=request.user.id)  
        return render(request,"shop/cart.html",{'cart':cart})
    else:
        messages.warning(request,"Login to Access Cart")
        return redirect("log_in") 

def viewFavourite(request):
    if request.user.is_authenticated:
        fav = Favourite.objects.filter(user_id=request.user.id)  
        return render(request,"shop/favourite.html",{'fav':fav})
    else:
        messages.warning(request,"Login to Access Favourite")
        return redirect("log_in") 

def Delete_Cart_Item(request,cid):
    cartItem = Cart.objects.get(id=cid)
    cartItem.delete()
    return redirect("cart")

def Delete_Favourite_Item(request,fid):
    favItem = Favourite.objects.get(id=fid)
    favItem.delete()
    return redirect("favourite")


