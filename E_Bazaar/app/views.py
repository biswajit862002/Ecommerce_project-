from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced, Payment
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings

# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):
 def get(self, request): 
  total_item = 0
  topwears = Product.objects.filter(category = 'TW')
  bottomwears = Product.objects.filter(category = 'BW')
  mobiles = Product.objects.filter(category = 'M')
  laptops = Product.objects.filter(category = 'L')

  if request.user.is_authenticated:
    total_item = len(Cart.objects.filter(user=request.user))

  context = {'topwears':topwears, 'bottomwears':bottomwears, 'mobiles':mobiles, 'laptops':laptops, 'totalitem':total_item}

  return render(request, 'app/home.html', context)

# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
 def get(self, request, pk):
  total_item = 0
  product = Product.objects.get(pk=pk)
  all_product = Product.objects.filter(category=product.category)
  # print("all Product: ",all_product)
  # print("category: ",product.category)
  item_already_in_cart = False
  if request.user.is_authenticated:
    total_item = len(Cart.objects.filter(user=request.user))
    item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
  context = {'product':product, 'item_already_in_cart':item_already_in_cart, 'totalitem':total_item, 'category':product.category, 'allproduct':all_product}
  return render(request, 'app/productdetail.html', context)


@login_required
def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
#  print("product : ",product_id)
 product = Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()
 return redirect('/cart')


@login_required
def show_cart(request):
 total_item = 0
 if request.user.is_authenticated:
  total_item = len(Cart.objects.filter(user=request.user))
  user = request.user
  cart = Cart.objects.filter(user=user)
  # print(cart)

  amount = 0.0
  shipping_amount = 40.0
  total_amount = 0.0
  card_product = [p for p in Cart.objects.all() if p.user == user]
  # print(card_product)

  if card_product:
   for p in card_product:
    temp_amount = (p.quantity * p.product.discounted_price)
    amount = amount + temp_amount
    total_amount = amount + shipping_amount
   return render(request, 'app/addtocart.html', {'carts':cart, 'amount':amount, 'totalamount':total_amount, 'totalitem':total_item})
  else:
   return render(request, 'app/emptycart.html', {'totalitem':total_item})
  
def plus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity+=1
  c.save()
  amount = 0.0
  shipping_amount = 40.0
  card_product = [p for p in Cart.objects.all() if p.user == request.user]

  for p in card_product:
    temp_amount = (p.quantity * p.product.discounted_price)
    amount = amount + temp_amount

  data = {
    'quantity': c.quantity,
    'amount': amount,
    'totalamount': amount + shipping_amount
    }
  return JsonResponse(data)
 
def minus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity-=1
  c.save()
  amount = 0.0
  shipping_amount = 40.0
  card_product = [p for p in Cart.objects.all() if p.user == request.user]

  for p in card_product:
    temp_amount = (p.quantity * p.product.discounted_price)
    amount = amount + temp_amount

  data = {
    'quantity': c.quantity,
    'amount': amount,
    'totalamount': amount + shipping_amount
    }
  return JsonResponse(data)
 

def remove_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.delete()
  amount = 0.0
  shipping_amount = 40.0
  card_product = [p for p in Cart.objects.all() if p.user == request.user]

  for p in card_product:
    temp_amount = (p.quantity * p.product.discounted_price)
    amount = amount + temp_amount

  data = {
    'amount': amount,
    'totalamount': amount + shipping_amount,
    }
  return JsonResponse(data)

@login_required
def buy_now(request):
  total_item = 0
  if request.user.is_authenticated:
    total_item = len(Cart.objects.filter(user=request.user))
  user = request.user
  product_id = request.GET.get('item_id')
  print("product : ",product_id)
  product = Product.objects.get(id=product_id)
  Cart(user=user, product=product).save()
  
  add = Customer.objects.filter(user=user)
  cart_items = Cart.objects.filter(user=user)
  amount = 0.0
  shipping_amount = 40.0
  totalamount = 0.0
  card_product = [p for p in Cart.objects.all() if p.user == request.user]
  if card_product:
    for p in card_product:
      temp_amount = (p.quantity * p.product.discounted_price)
      amount = amount + temp_amount
    if amount < 500:
      totalamount = amount + shipping_amount
    else:
      totalamount = amount
  return render(request, 'app/buynow.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items, 'totalitem':total_item})


@login_required
def address(request):
 total_item = 0
 address = Customer.objects.filter(user=request.user)
 if request.user.is_authenticated:
    total_item = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/address.html', {'address':address, 'active':'btn-primary', 'totalitem':total_item})


class updateAddress(View):
  def get(self, request, pk):
    add = Customer.objects.get(pk=pk)
    form = CustomerProfileForm(instance=add)
    return render(request, 'app/updateaddress.html', {'form':form})
  def post(self, request, pk):
    form = CustomerProfileForm(request.POST)
    if form.is_valid():
      add = Customer.objects.get(pk=pk) 
      add.name = form.cleaned_data['name']
      add.locality = form.cleaned_data['locality']
      add.city = form.cleaned_data['city']
      add.mobile = form.cleaned_data['mobile']
      add.zipcode = form.cleaned_data['zipcode']
      add.state = form.cleaned_data['state']

      add.save()
      messages.success(request,"Congratulations! Profile Updated Successfully")
    else:
      messages.warning(request,"Invalid Input Data")

    return redirect('address')


@login_required
def orders(request):
 total_item = 0
 op = OrderPlaced.objects.filter(user=request.user)
 if request.user.is_authenticated:
    total_item = len(Cart.objects.filter(user=request.user))
 return render(request, 'app/orders.html', {'order_placed':op, 'totalitem':total_item})


# @csrf_exempt
# def cancel_order(request):
#     if request.method == 'POST':
#         order_id = request.POST.get('order_id')
#         print("order_id: ",order_id)
#         try:
#             order = OrderPlaced.objects.get(id=order_id)
#             order.status = 'Cancel'
#             order.save()
#             return JsonResponse({'message': 'Order cancelled successfully!'})
#         except OrderPlaced.DoesNotExist:
#             return JsonResponse({'error': 'Order not found!'}, status=404)
#     return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def cancel_order(request):
    if request.method == 'POST':
        # print("--------POST Data: ", request.POST)  # Debugging
        order_id = request.POST.get('order_id')  # Get the product ID
        user_id = request.user.id  # Get the logged-in user's ID
        # print("1-----------order_id: ",order_id)
        # print("1-----------user_id: ",user_id)
        if not order_id:
            return JsonResponse({'error': 'Order ID is missing'}, status=400)
        
        try:
            # order = OrderPlaced.objects.get(product=order_id, user_id=user_id)

            # Fetch the specific order using the unique order ID
            order = OrderPlaced.objects.get(id=order_id)

            # print("-----------order: ",order)
            # print(f"id: {order.id}")  # See the current value
            # print(f"user: {order.user}")  # See the current value
            # print(f"product: {order.product}")  # See the current value
            # print(f"Before status: {order.status}")  # See the current value
            order.status = 'Cancel'
            # print(f"After status: {order.status}")  # Confirm the new value
            order.save()
            return JsonResponse({'message': 'Order cancelled successfully!'})
        except OrderPlaced.DoesNotExist:
            return JsonResponse({'error': 'Order not found!'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)



def mobile(request, data=None):
 total_item = 0
 if request.user.is_authenticated:
    total_item = len(Cart.objects.filter(user=request.user))
 if data == None:
  mobiles = Product.objects.filter(category='M')
 elif data == 'Redmi' or data == 'Samsung' or data == 'Oppo' or data == 'Vivo' or data == 'Apple':
  mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data == 'below10k':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
 elif data == 'below20k':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=20000)
 elif data == 'above20k':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=20000)

 context = {'mobiles':mobiles, 'totalitem':total_item}
 return render(request, 'app/mobile.html', context)


def laptop(request, data=None):
 total_item = 0
 if request.user.is_authenticated:
    total_item = len(Cart.objects.filter(user=request.user))
 if data == None:
  laptops = Product.objects.filter(category='L')
 elif data == 'Hp' or data == 'Dell' or data == 'Lenovo' or data == 'Msi' or data == 'Samsung':
  laptops = Product.objects.filter(category='L').filter(brand=data)
 elif data == 'below40k':
  laptops = Product.objects.filter(category='L').filter(discounted_price__lt=40000)
 elif data == 'below50k':
  laptops = Product.objects.filter(category='L').filter(discounted_price__lt=50000)
 elif data == 'above50k':
  laptops = Product.objects.filter(category='L').filter(discounted_price__gt=50000)
 elif data == 'above100k':
  laptops = Product.objects.filter(category='L').filter(discounted_price__gt=100000)

 context = {'laptops':laptops, 'totalitem':total_item}
 return render(request, 'app/laptop.html', context)



def topwear(request, data=None):
 total_item = 0
 if request.user.is_authenticated:
    total_item = len(Cart.objects.filter(user=request.user))
 if data == None:
  topwears = Product.objects.filter(category='TW')
 elif data == 'Park' or data == 'Polo':
  topwears = Product.objects.filter(category='TW').filter(brand=data)
 elif data == 'below500':
  topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=500)
 elif data == 'above500':
  topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=500)

 context = {'topwears':topwears, 'totalitem':total_item}
 return render(request, 'app/topwear.html', context)


def bottomwear(request, data=None):
 total_item = 0
 if request.user.is_authenticated:
    total_item = len(Cart.objects.filter(user=request.user))
 if data == None:
  bottomwears = Product.objects.filter(category='BW')
 elif data == 'Lee' or data == 'Spykar':
  bottomwears = Product.objects.filter(category='BW').filter(brand=data)
 elif data == 'below500':
  bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lt=500)
 elif data == 'below1000':
  bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lt=1000)
 elif data == 'above1000':
  bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gt=1000)

 context = {'bottomwears':bottomwears, 'totalitem':total_item}
 return render(request, 'app/bottomwear.html', context)




def login(request):
 return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
 def get(self, request):
  form = CustomerRegistrationForm()
  context = {'form':form}
  return render(request, 'app/customerregistration.html', context)
 
 def post(self, request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations!! Registered Successfully')
   form.save() 
  
  return render(request, 'app/customerregistration.html', {'form':form})


@login_required
def checkout(request):
 total_item = 0
 if request.user.is_authenticated:
  total_item = len(Cart.objects.filter(user=request.user))
 user = request.user
 add = Customer.objects.filter(user=user)
#  print("-----address : ",add)
 cart_items = Cart.objects.filter(user=user)
 amount = 0.0
 shipping_amount = 40.0
 totalamount = 0.0
 card_product = [p for p in Cart.objects.all() if p.user == request.user]
 if card_product:
  for p in card_product:
    temp_amount = (p.quantity * p.product.discounted_price)
    amount = amount + temp_amount
  if amount < 500:
   totalamount = amount + shipping_amount
   razoramount = int(totalamount * 100)
  else:
   totalamount = amount
   razoramount = int(totalamount * 100)
  
  client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
  data = {'amount': razoramount, 'currency':'INR', 'receipt': 'order_rcptid_12'}
  payment_response = client.order.create(data=data)
  print(payment_response)

  order_id = payment_response['id']
  order_status = payment_response['status']
  if order_status == 'created':
    payment = Payment(
      user = user,
      amount = totalamount,
      razorpay_order_id = order_id,
      razorpay_payment_status = order_status
    )
    payment.save()

 return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items, 'totalitem':total_item, 'razoramount':razoramount, 'order_id':order_id})

@login_required
def payment_done(request):
  order_id = request.GET.get('order_id')
  payment_id = request.GET.get('payment_id')
  cust_id = request.GET.get('cust_id')

  print("-----------------")
  print("order id :", order_id)
  print("payment id :", payment_id)
  print("cust id :", cust_id)
  print("-----------------")

  user = request.user
  customer = Customer.objects.get(id=cust_id)
  print("customer :", customer)

  # to update payment status and payment id
  payment = Payment.objects.get(razorpay_order_id=order_id)
  print("payment :", payment)

  payment.paid = True
  payment.razorpay_payment_id = payment_id
  payment.save()
  # to save other details
  cart = Cart.objects.filter(user=user)
  print("-------cart: ", cart)
  for c in cart:
    OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, payment=payment).save()
    c.delete()
  return redirect('orders')


# @login_required
# def paymentdone(request):
#  user = request.user
#  custid = request.GET.get('custid')
# #  print("cust_id: ",custid)
#  customer = Customer.objects.get(id=custid)
#  cart = Cart.objects.filter(user=user)
#  for item in cart:
#   OrderPlaced(user=user, customer=customer, product=item.product, quantity=item.quantity).save()
#   item.delete()
#  return redirect('orders')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
 def get(self, request):
  total_item = 0
  if request.user.is_authenticated:
    total_item = len(Cart.objects.filter(user=request.user))
  form = CustomerProfileForm()
  return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'totalitem':total_item})
 
 def post(self, request):
  total_item = 0
  if request.user.is_authenticated:
    total_item = len(Cart.objects.filter(user=request.user))
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   user = request.user
   name = form.cleaned_data['name']
   locality = form.cleaned_data['locality']
   city = form.cleaned_data['city']
   mobile = form.cleaned_data['mobile']
   state = form.cleaned_data['state']
   zipcode = form.cleaned_data['zipcode']

   profile = Customer(user=user, name=name, locality=locality, city=city, mobile=mobile, state=state, zipcode=zipcode)
   profile.save()

   messages.success(request, 'Congratulations!! Profile Updated Successfully')
  return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'totalitem':total_item})

