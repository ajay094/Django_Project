from django.shortcuts import render,redirect
from django.http import HttpResponse
from foodzone.forms import Userregister
from fooddelivery import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from foodzone.models import Product
from foodzone import forms,models

# Create your views here.

def home(request):
    context = {'products':Product.objects.all()}
    return render(request,'html/home.html',context)

@login_required
def myorder(request):
	return render(request,'html/myorders.html')

def about(request):
	return render(request,'html/about.html')

def contact(request):
	sub = forms.ContactusForm()
	if request.method == 'POST':
		sub = forms.ContactusForm(request.POST)
		if sub.is_valid():
			email = sub.cleaned_data['Email']
			name=sub.cleaned_data['Name']
			message = sub.cleaned_data['Message']
			send_mail(str(name)+' || '+str(email),message, settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
			return render(request, 'ecom/contactussuccess.html')
	return render(request,'html/contact.html')

@login_required
def userdashboard(request):	
	return render(request,'html/admindashboard.html')

def register(request):
	if request.method == "POST":
		a = Userregister(request.POST)
		if a.is_valid():
			p = a.save(commit=False)
			rc = p.email
			sb = "Welcome to fooddelivery"
			msg = "Dear {},You have successfully created your Onlinegrocery account.Congratulations and welcome to a whole new world of grocery shopping.Your details: password:{}".format(p.username,p.password)
			sd = settings.EMAIL_HOST_USER
			snt = send_mail(sb,msg,sd,[rc])
			if snt == 1:
				p.save()
				messages.success(request,"Please check your {} for login creadentials".format(rc))
				return redirect("/lg")
	a = Userregister()
	return render(request,'html/register.html',{'b':a})

def addtocart(request,pk):
	products = models.Product.objects.all()

@login_required
def admindashboard(request):
	productcount=models.Product.objects.all().count()
	ordercount=models.Orders.objects.all().count()
	orders = models.Orders.objects.all()
	ordered_products = []
	ordered_buys = []
	for order in orders:
		ordered_product = models.Product.objects.all().filter(id = order.product.id)
		ordered_buys = models.Customer.objects.all().filter(id = order.customer.id)
		ordered_products.append(ordered_product)
		ordered_buys.append(ordered_buys)

	mydict = {
	'productcount':productcount,
	'ordercount':ordercount,
	'data':zip(ordered_products,ordered_buys,orders)
	}
	return render(request,'html/admindashboard.html',context=mydict)

@login_required
def products(request):
    productss = models.Product.objects.all()
    return render(request, 'html/productscatalogue.html', {'pro':productss})

@login_required
def addproducts(request):
	a = forms.ProductForm()
	if request.method == "POST":
		a = forms.ProductForm(request.POST,request.FILES)
		if a.is_valid():
			a.save()
			messages.success(request,"{} you have successfully added a new product details in productscatalogue".format(request.user.username))
			return redirect('/prod')
	return render(request,'html/addproducts.html',{'k':a})

@login_required
def updateproducts(request,pk):
	product = models.Product.objects.get(id=pk)
	productForm = forms.ProductForm(instance = product)
	if request.method == "POST":
		productForm = forms.ProductForm(request.POST,request.FILES,instance=product)
		if productForm.is_valid():
			productForm.save()
			messages.warning(request,"{} you have successfully updated the product details in productscatalogue".format(request.user.username))
		return redirect('/prod')	
	return render(request,'html/updateproduct.html',{'productForm':productForm})

@login_required
def deleteproducts(request,pk):
	product = models.Product.objects.filter(id=pk)
	if request.method == "POST":
		product.delete()
		messages.warning(request,"{} you have successfully deleted the product from productscatalogue".format(request.user.username))
		return redirect('/prod')
	return render(request,'html/deleteproduct.html')
