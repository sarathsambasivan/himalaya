from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from myadmin.models import Customer, Product, Booking

from django.shortcuts import render, get_object_or_404, redirect

import razorpay
from django.conf import settings

from django.core.mail import send_mail
from django.shortcuts import render


from django.core.mail import EmailMessage

import os
from .utils import generate_invoice_pdf

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache

from django.db.models import Q




# Create your views here.

def home(request):
    return render(request, "index.html")
def about(request):
    return render(request, "about.html")
def benefits(request):
    return render(request, "benefits.html")
def contactus(request):
    return render(request, "contactus.html")
def signup(request):
    return render(request, "signup.html")

def products(request):
    return render(request, "products.html")

# def admin_home(request):
#     return render(request, "admin_home.html")

def add_product(request):
    return render(request, "add_product.html")

def admin_home(request):
    return render(request, "admin_home.html")

def customer_home(request):
    product = Product.objects.first()  # You can change to .last() or filter
    return render(request, 'customer_home.html', {"product": product})



def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            customer = Customer.objects.create(user=user,mobile_number=phone, age=age, gender=gender)
            user.save()
            customer.save()
            messages.success(request, "You have successfully registered")
            return redirect('login_view')
        else:
            messages.error(request, "Passwords don't match.")
            return redirect('signup')

    return render(request, 'signup.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:  # Admin Login
                return redirect('admin_home')
            else:  # Normal user login
                return redirect('customer_home')

        else:
            messages.error(request, "Username or password is incorrect.")
            return redirect('login_view')

    return render(request, 'login.html')



#-----------product-----------#
def add_product_view(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        available = request.POST.get('available')
        image = request.FILES.get('image')

        product = Product.objects.create(product_name=product_name, description=description, price=price, stock=stock,available=available, image=image)
        product.save()
        messages.success(request, "You have successfully product added")
        return redirect('product_details')

    return render(request, "add_product.html")



def product_details_view(request):
    product = Product.objects.all()
    return render(request, 'product_details.html', {'products': product})

def edit_product_view(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.method == 'POST':
        product.product_name = request.POST.get('product_name')
        product.description = request.POST.get('description')
        product.price = float(request.POST.get('price'))
        product.stock = int(request.POST.get('stock'))
        product.available = request.POST.get('available') == 'on'

        product.save()
        messages.success(request, "Product updated successfully.")
        return redirect('product_details')

    return render(request, 'edit_product.html', {'product': product})


def delete_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('product_details')  # Update this to your actual view name

    return redirect('edit_product_view', product_id=product_id)

#-----------customer-----------#
def customer_edit_profile_view(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    if request.method == "POST":
        customer.user.first_name = request.POST.get('first_name')
        customer.user.last_name = request.POST.get('last_name')
        customer.user.email = request.POST.get('email')

        customer.mobile_number = request.POST.get('phone')
        customer.age = request.POST.get('age')
        customer.user.save()
        customer.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('customer_detail')

    return render(request, 'customer_edit_profile.html', {'customer': customer})


def customer_detail_view(request):
    customers = Customer.objects.select_related('user').all()
    return render(request, 'customer_details.html', {'customer': customers})


def customer_delete_view(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    if request.method == "POST" or request.method == "GET":
        customer.user.delete()  # delete the associated user too
        customer.delete()
        messages.success(request, "Customer deleted successfully.")
        return render(request, 'customer_details.html')

#----------------booking product---------------#
def customer_dashboard(request):
    product = Product.objects.first()  # You can change to .last() or filter
    return render(request, 'cust_home.html', {"product": product})

def book_product(request, product_id):
    if request.method == "POST":
        request.session['booking_data'] = {
            'product_id': product_id,
            'product_name': request.POST.get('product_name'),
            'quantity': request.POST.get('quantity'),
            'customer_name': request.POST.get('customer_name'),
            'phone': request.POST.get('phone'),
            'address': request.POST.get('address')
        }
        return redirect('confirm_booking')

    # load session data if exists (for back button)
    booking_data = request.session.get('booking_data', {})
    return render(request, "book_product.html", {'booking_data': booking_data})

def product_booking(request, id):
    product = Product.objects.get(id=id)
    user = User.objects.get(id=request.user.id)
    customer = Customer.objects.get(user_id=request.user.id)

    if request.method == "POST":
        alt_mobile = request.POST.get("alt_mobile")
        qty = int(request.POST.get("quantity"))
        total = qty * product.price

        request.session['booking'] = {
            "product_id": product.id,
            "qty": qty,
            "total": total,
            "product_name": product.product_name,
            "base_price": product.price,

            # Save user+customer details in session also
            "customer_name": user.first_name,
            "customer_email": user.email,
            "customer_phone": customer.mobile_number,
            "alt_mobile": alt_mobile
        }

        return redirect('confirm_booking')
    try:
        booking = request.session.get('booking')
        context = {
            'booking': booking,
            'product': product,
            'user': user,
            'customer': customer
        }
        return render(request, 'product_booking.html', context)
    except Exception as e:

        return redirect('customer_dashboard')






    # return render(request, 'product_booking.html', {
    #     "product": product,
    #     "customer": customer,
    #     "user": user,
    #
    # })



def confirm_booking(request):
    booking = request.session.get("booking")

    if not booking:
        return redirect('payment')

    product = Product.objects.get(id=booking["product_id"])
    customer = Customer.objects.get(user_id=request.user.id)

    if request.method == "POST":
        # Here later we save into DB
        # del request.session['booking']
        messages.success(request, "Booking Confirmed!")
        return redirect('payment')

    return render(request, "confirm_booking.html", {
        "booking": booking,
        "product": product,
        "customer": customer
    })


# confirm booking

def payment(request):
    return render(request, "payment.html")

def razorpay_success(request):
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    order = client.order.create(dict(amount=1000, currency="INR", payment_capture=1))

    booking = request.session.get('booking')


    return render(request, "razorpay.html", {
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'order_id': order['id'],
         'amount': booking['total'],
        'payment_method':"card",
        'booking_data': booking,
    })


@never_cache
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def payment_success(request):
    if 'booking' not in request.session:
        return redirect('customer_home')



    booking_save = request.session.get('booking')
    customer = Customer.objects.get(user_id=request.user.id)
    product = Product.objects.get(id=booking_save["product_id"])

    email = booking_save['customer_email']

    booking = Booking.objects.create(
        customer=customer,
        product=product,
        email=booking_save["customer_email"],
        alt_mobile=booking_save["alt_mobile"],
        total_amount=booking_save["total"],
        total_quantity=booking_save["qty"],
        payment_status="paid",
        order_status="confirmed",
        price=booking_save["base_price"],
    )

    # booking.save()

    # Generate PDF invoice path
    invoice_path = f"media/invoices/invoice_{booking.id}.pdf"
    # invoice_path = f"media/invoices/test_invoice.pdf"
    # Create folder if not exists
    os.makedirs(os.path.dirname(invoice_path), exist_ok=True)

    # Generate PDF
    generate_invoice_pdf(booking, invoice_path)




    # Fetch all customer purchases (newest first)
    all_orders = Booking.objects.filter(customer=customer).order_by('-id')

    if email:

        message = EmailMessage(
            subject="Payment Successful - Your Invoice",
            body="Thank you! Please find your invoice attached.",
            from_email=settings.EMAIL_HOST_USER,
            to=[email],
        )

        message.attach_file(invoice_path)
        message.send()

        # context = {
        #      "booking": booking_save,
        #      "session_id": request.session.session_key,
        #     "latest_booking": booking,  # current order
        #     "all_orders": all_orders,  # all customer purchase history
        # }



        # request.session.flush()


    # return render(request, "payment_success.html", context)

    return redirect("my_orders")


def my_orders(request):
    customer = Customer.objects.get(user_id=request.user.id)
    all_orders = Booking.objects.filter(customer=customer).order_by('-id')
    latest_order = Booking.objects.filter(customer=customer).order_by('-id').first()
    context = {
        'all_orders': all_orders,
        'customer': customer,
        'latest_order': latest_order,
    }

    return render(request, "payment_success.html", context)


def orderlist_view(request):
    search = request.GET.get('search', '')
    orders = Booking.objects.all().order_by('-id')  # newest first

    if search:
        orders = orders.filter(
            Q(customer__user__username__icontains=search) |
            Q(product__product_name__icontains=search)
        )

    return render(request, "orderlist.html", {"orders": orders, "search": search})
