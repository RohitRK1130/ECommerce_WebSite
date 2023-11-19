from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name="index"),
	path('cart/', views.cart, name="cart"),
    path('about/', views.about, name="about"),
    path('testimonial/', views.testimonial, name="testimonial"),
    path('product/', views.product, name="product"),
    path('blog/', views.blog, name="blog"),
    path('contact/', views.contact, name="contact"),
    path('checkout/', views.checkout, name="checkout"),

    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('razorpay-success/', views.razorpaySuccess, name="razorpaySuccess"),

    # login 
    path(r'login/$', views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
]