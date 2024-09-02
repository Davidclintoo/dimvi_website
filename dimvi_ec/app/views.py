from django.shortcuts import render, redirect
from django.db.models import Count
from django.db.models import Q
from urllib import request
from django.http import HttpResponse
from django.http import  JsonResponse
from django.views import View
from .models import Product, Customer, Cart
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, "app/home.html")

def about(request):
    return render(request, "app/about.html")

class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category = val)
        title = Product.objects.filter(category = val).values('title')
        return render(request, "app/category.html", locals())
    
class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title = val)
        title = Product.objects.filter(category = product[0].category).values('title')
        return render(request, "app/category.html", locals())
    
class Productdetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, "app/productdetails.html", locals())
    
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', locals())
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulation! You have succeefully registered')
        else:
            messages.warning(request, "invalid input data")
        return render(request, 'app/customerregistration.html', locals())

class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', locals())
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            town = form.cleaned_data['town']
            mobile = form.cleaned_data['mobile']
            county = form.cleaned_data['county']
            zipcode = form.cleaned_data['zipcode']
            
            reg = Customer(user=user, name=name, town=town, mobile=mobile, county=county, zipcode=zipcode)
            reg.save()
            messages.success(request, "congratulation! Profile save successfully")
        else:
            messages.warning(request, "invalid input Data")
        return render(request, 'app/profile.html', locals())
         
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', locals())
 
class UpdateAdress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAdress.html', locals())
    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.town = form.cleaned_data['town'] 
            add.mobile = form.cleaned_data['mobile'] 
            add.county = form.cleaned_data['county'] 
            add.zipcode = form.cleaned_data['zipcode']
            add.save()  
            messages.success(request, "Congratulations! Profile Update Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect( 'address')

def add_to_cart(request):
    user=request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id= product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity*p.product.discounted_price
        amount = value + amount
    total_amount = amount + 20.00
    
    return render(request, 'app/addtocart.html', locals())


def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.quantity+=1
        print(c)
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        total_amount = amount + 20.00
        
        data ={
            'quantity':c.quantity,
            'amount': amount,
            'total_amount' : total_amount
        }
        print(data)
        
        # return JsonResponse(data)


def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        total_amount = amount + 20.00
        data ={
            'quantity':c.quantity,
            'amount': amount,
            'total_amount' : total_amount
        }
        return JsonResponse(data)
    
    