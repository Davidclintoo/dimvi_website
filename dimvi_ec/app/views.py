from django.shortcuts import render, redirect
from django.db.models import Count
from urllib import request
from django.http import HttpResponse
from django.views import View
from .models import Product, Customer
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
    
    