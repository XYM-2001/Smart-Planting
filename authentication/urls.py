from django.urls import path

from authentication.views import user
from authentication.views.user import update_profile, upgrade
from main.views.payment import checkout
from main.views.cart import add_to_cart

app_name = 'authentication'
urlpatterns = [
    path('update/<int:pk>', update_profile.as_view(), name='update'),
    path('login/', user.login, name='login'),
    path('logout/', user.logout, name='logout'),
    path('register/', user.register, name='register'),
    path('checkcart/', user.check_cart, name='check_cart'),
    path('expert/', user.expert, name='expert'),
    path('<str:username>/', user.userinfo, name='user'),
    path('upgrade/<int:pk>', upgrade.as_view(), name='upgrade'),
    path("checkout/", checkout, name="checkout"),
]
