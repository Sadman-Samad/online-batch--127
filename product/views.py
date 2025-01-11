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
    return redirect('cart_views')    


def remove_cart_item(request,id):
    cart_item = get_object_or_404(CartItem, pk=id)
    cart_item.delete()
    return redirect('cart_views') 

def cart_views(request):
    cart = CartItem.objects.filter(cart__user = request.user)
    # print('cart=======', cart)
    return render(request, 'cart.html', {'cart':cart})


def add_coupon(request):
    code = request.POST.get('code')
    print('code===', code)
    cart = CartItem.objects.get(cart__user=request.user)
    print('cart===', cart)

    if not code:
        return redirect('/')
    try:
        coupon = Coupon.objects.get(code=code,is_active=True)
        print('coupon===', coupon)
        
        if coupon.used_count>= coupon.limit:
            print('coupon======')
            return redirect('/')
        total_price = cart.get_total()
        
        print('total_price===', total_price)
        discount_amount = (coupon.discount/100)* total_price
        print('discount_amount===', discount_amount)
        final_price = total_price - discount_amount
        print('final_price===', final_price)

        coupon.used_count +=1
        coupon.save()

        return redirect('/')
    
    except Coupon.DoesNotExist:
        return redirect('/')



def add_to_wishlist(request,id):
    print('id---------', id)
    product = get_object_or_404(Product, pk=id)
    print('product====', product)
    wishlist = Wishlist.objects.get_or_create(user=request.user, product = product)
    print('wishlist=============', wishlist)

    return redirect('/')



def create_order(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    print('cart_items======', cart_items)
    # if not cart_items.exists():
    #     return render(request, 'order.html', {'error': 'Your cart is empty!'})

    total_due = sum(item.get_total() for item in cart_items)
    print('total_due----------', total_due)

    if request.method == "POST":
        form = OrderForm(request.POST)
        print('form=====', form)
        if form.is_valid():
            print('form=====', form)
            order = form.save(commit=False)
            order.user = request.user
            order.total_due = total_due
            order.total_paid = 0.00
            order.save()

            order.cart.set(cart_items)
            
            # Clear the cart
            cart_items.delete()


    else:
        form = OrderForm()

    return render(request, 'order.html', {
        'cart_items': cart_items,
        'total_due': total_due,
        'form': form,
    })
