from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.products_page, name='products_page'),
    path('order-history/', views.order_history, name='order_history'),  # Order history page
    path('liked-products/', views.liked_products, name='liked_products'),  # Liked products page
    path('cart/', views.cart_page, name='cart_page'),  # Cart page

]
