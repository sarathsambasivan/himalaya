from django.urls import path
from . import views
from .views import signup_view
from .views import product_details_view
from .views import edit_product_view

urlpatterns = [
    path('', views.home, name='index'),
    path("about",views.about, name="about"),
    path("benefits",views.benefits, name="benefits"),
    path("contactus", views.contactus, name="contactus"),
    path("products", views.products, name="products"),
    path("admin_home", views.admin_home, name="admin_home"),
    path("customer_home", views.customer_home, name="customer_home"),

    # -----Login and signup-------#
    path("signup", views.signup_view, name="signup"),
    path("login_view", views.login_view, name="login_view"),


    #-----customer-------#
    path("customer_detail", views.customer_detail_view, name="customer_detail"),
    path('customer/<int:customer_id>/edit/', views.customer_edit_profile_view, name='customer_edit_profile'),
    path('customer/<int:customer_id>/delete/', views.customer_delete_view, name='customer_delete'),

    #----products------#
    path("add_product", views.add_product_view, name="add_product"),
    path("product_details", views.product_details_view, name="product_details"),
    path('products/<int:product_id>/edit/', views.edit_product_view, name='edit_product'),
    path('products/<int:product_id>/delete/', views.delete_product_view, name='delete_product'),
    path("product_booking/<int:id>/", views.product_booking, name="product_booking"),

    path("confirm_booking", views.confirm_booking, name="confirm_booking"),
    path("payment", views.payment, name="payment"),

    path("razorpay_success", views.razorpay_success, name="razorpay_success"),
    path("payment_success", views.payment_success, name="payment_success"),
    path("my_orders", views.my_orders, name="my_orders"),


path('orderlist', views.orderlist_view, name='orderlist'),




]

