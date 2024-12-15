from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category
from .forms import *


def product_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'products.html', context)

def product_detail(request, id):
    product = Product.objects.get(id=id)
    context = {'product': product}
    return render(request, 'product_details.html', context)


def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ProductForm()
    return render(request, 'product_create.html', {'form':form})    

def product_update(request,id):
    product = get_object_or_404(Product,pk=id)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/', pk = product.pk)
        
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_update.html', {'form':form})    


def add_to_cart(request,id):
    product = get_object_or_404(Product, pk = id)
    session_key = request.session.session_key or request.session.create()

    cart , _ = Cart.objects.get_or_create(session_key=session_key, user = request.user)
    cart_item,created = CartItem.objects.get_or_create(cart=cart,product=product)


    if not created:
        cart_item.quantity +=1
        cart_item.save()
    return redirect('/')

def update_cart(request,id):
    cart_item = get_object_or_404(CartItem, pk =id,cart___session_key=request.session.session_key)
    new_quantity = int(request.POST.get('quantity', 1))

    if new_quantity > 0:
        cart_item.quantity = new_quantity
        cart_item.save()
    else: 
        cart_item.delete()   
    return redirect('/')    


def remove_cart_item(request,id):
    cart_item = get_object_or_404(CartItem, pk=id, cart___session_key=request.session.session_key)
    cart_item.delete()
    return redirect('/') 

