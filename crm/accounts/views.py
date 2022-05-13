from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from . forms import OrderForm
from .filters import OrderFilter
from django.contrib.auth.models import User, auth
from django.contrib import messages

#-------------------(DETAIL/LIST VIEWS) -------------------

def dashBoard(request):
	orders = Order.objects.all().order_by('-status')[0:5]
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = Order.objects.all().count()
	delivered = Order.objects.filter(status='Delivered').count()
	pending = Order.objects.filter(status='Pending').count()



	context = {'customers':customers, 'orders':orders,
	'total_customers':total_customers,'total_orders':total_orders, 
	'delivered':delivered, 'pending':pending}
	return render(request, 'accounts/dashBoard.html', context)

def products(request):
	products = Product.objects.all()
	context = {'products':products}
	return render(request, 'accounts/products.html', context)

def customer(request, pk):
	customer = Customer.objects.get(id=pk)
	orders = customer.order_set.all()
	total_orders = orders.count()



	orderFilter = OrderFilter(request.GET, queryset=orders) 
	orders = orderFilter.qs

	context = {'customer':customer, 'orders':orders, 'total_orders':total_orders,
	'filter':orderFilter}
	return render(request, 'accounts/customer.html', context)


#-------------------(CREATE VIEWS) -------------------

def createOrder(request):
	action = 'create'
	form = OrderForm()
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')

	context =  {'action':action, 'form':form}
	return render(request, 'accounts/order_form.html', context)

#-------------------(UPDATE VIEWS) -------------------

def updateOrder(request, pk):
	action = 'update'
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/customer/' + str(order.customer.id))

	context =  {'action':action, 'form':form}
	return render(request, 'accounts/order_form.html', context)

#-------------------(DELETE VIEWS) -------------------

def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == 'POST':
		customer_id = order.customer.id
		customer_url = '/customer/' + str(customer_id)
		order.delete()
		return redirect(customer_url)
		
	return render(request, 'accounts/delete_item.html', {'item':order})



def register(request):   
    if request.method == "POST" :
        firstname = request.POST['f_name']
        lastname = request.POST['l_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password : 
            if User.objects.filter(username = username).exists():
                messages.info(request, "Username already taken")
                return redirect("register")
            elif User.objects.filter(email = email).exists():
                messages.info(request, "Email already in use")
                return redirect("register")
            else :
                user = User.objects.create_user(username, email, password)
                user.first_name, user.last_name = firstname, lastname
                user.save()
                auth.login(request, user)
                return redirect("dashboard")

        else :
            messages.info(request, 'Password not matched!')
            return redirect("register")
    return render(request, "accounts/register.html")



def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect("dashboard")
        else:           
            return render(request, "accounts/login.html")
    return render(request, "accounts/login.html")



def logout(request):
    auth.logout(request)
    return redirect("dashboard")


