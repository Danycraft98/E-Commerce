import stripe
from django.contrib.auth.decorators import login_required
from django.http import Http404, QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings

from products.models import Product, Group, Tag, ProductsToBuyers


def index(request):
    products1 = Product.objects.all()
    tags = Tag.objects.all()
    pages = len(products1) // 3
    groups = Group.objects.all()
    return render(request, 'main/index.html', {'products': products1, 'tags': tags, 'pages': range(pages), 'groups': groups})


def search(request):
    groups = Group.objects.all()
    item = request.POST.get('search', '')
    try:
        products1 = Product.objects.filter(name__contains=item)
    except Group.DoesNotExist:
        return redirect(reverse('products', kwargs={'item': item}))
    return render(request, 'main/products.html', {'products': products1, 'item': item, 'groups': groups})


def products(request, item):
    groups = Group.objects.all()
    try:
        item = Group.objects.get(name=item)
        products1 = Product.objects.filter(group__id=item.id)
    except Group.DoesNotExist or Product.DoesNotExist:
        try:
            item = Tag.objects.get(content=item)
            products1 = Product.objects.filter(tag__id=item.id)
        except Tag.DoesNotExist or Product.DoesNotExist:
            raise Http404('Group or Tag or Products does not exist')
    return render(request, 'main/products.html', {'products': products1, 'item': item, 'groups': groups})


def product(request, name):
    groups = Group.objects.all()
    try:
        product1 = Product.objects.get(name=name)
    except Product.DoesNotExist:
        raise Http404('Product does not exist')
    return render(request, 'main/product.html', {'product': product1, 'groups': groups})


def add(request):
    product1 = Product.objects.get(pk=request.POST.get('prod_id', None))
    quantity = int(request.POST.get('quantity', 0))
    try:
        prodToBuyers = ProductsToBuyers.objects.get(products=product1, buyers=request.user)
        prodToBuyers.quantity += quantity
        prodToBuyers.save()
    except BaseException:
        prodToBuyers = ProductsToBuyers.objects.create(products=product1, buyers=request.user, quantity=quantity)
    return render(request, 'main/add.html', {'prodToBuyers': prodToBuyers})


def cart(request):
    if request.method == 'POST':
        quantity = request.POST.getlist('quantity', '')
        if len(quantity) == 1:
            print(quantity)
            prodToBuyer = ProductsToBuyers.objects.get(pk=int(request.POST.get('prod_id', None)))
            prodToBuyer.quantity = int(quantity[0])
            prodToBuyer.save()

        else:
            pass

    list_of_prod = ProductsToBuyers.objects.filter(buyers=request.user).all()
    total_quantity, total_cost = 0, 0
    for prod in list_of_prod:
        total_quantity += prod.quantity
        total_cost += prod.products.price * prod.quantity
    return render(request, 'main/cart.html', {'products': list_of_prod, 'total_info': (total_quantity, total_cost)})


def pay(request):
    list_of_prod = ProductsToBuyers.objects.filter(buyers=request.user).all()
    total_cost = 0
    for prod in list_of_prod:
        total_cost += prod.products.price * prod.quantity

    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1I2xTCEUKaBiWzyCm3SKMXDZ',
            'quantity': 1
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('cart'))+ '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('cart'))
    )

    context = {
        'session_id': session.id,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'main/pay.html', {'total_cost': total_cost})


def delete(request, prod_id):
    prodToBuyer = ProductsToBuyers.objects.get(pk=prod_id)
    prodToBuyer.delete()
    return redirect(reverse('cart'))
