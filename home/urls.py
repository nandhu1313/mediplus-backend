from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('user/create', views.user_create),
    path('user/login', views.user_login),
    path('user/<int:id>', views.user),
    # path('user/otp/verify/<str:email>', views.user_verify_email),
    path('products', views.products),
    path('product/details/<int:id>', views.product),
    path('search/<str:query>', views.search),
    path('buy', views.buy),
]
