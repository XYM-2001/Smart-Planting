from django.urls import path
# self edited --------------------------
from django.urls import re_path
from django.views.static import serve
from mysite.settings import MEDIA_ROOT
# self edited --------------------------
from main.views import ai_solutions
from main.views.consulting import HomeView
from main.views.consulting import PostDetail
from main.views.consulting import CreatePost
from main.views.consulting import AddComment,shopping_carts
from main.views.consulting import Experts
from main.views.consulting import LikeView
from main.views.consulting import PostRate
from main.views.consulting import ReverseView
from main.views.consulting import SortedView
from main.views.consulting import HotView
from main.views.consulting import MyShare
from main.views.plant import *
from main.views.plant import my_plants
from main.views.plant import add_plants, manage_plants
from main.views.plant import diagnoseView
from main.views.plant import delete_plants
from main.views.payment import checkout
from main.views.payment import create_alipay_payment_intent
from main.views.payment import create_wechat_pay_payment_intent
from main.views.payment import success
from main.views.payment import cancel
from main.views import payment
from main.views.cart import view_cart
from main.views.cart import add_to_cart

app_name = 'main'
urlpatterns = [
    path('', ai_solutions.index, name='index'),
    path('aisolutions/<int:page>/', ai_solutions.ai_solutions, name='ai_solutions'),
    path('aisolutions/smartcurtain/<int:page>/', ai_solutions.smart_curtain, name='smart_curtain'),
    path('aisolutions/ai_classification/', ai_solutions.ai_classification, name='ai_classification'),
    path('aisolutions/aidiseasediagnose/', ai_solutions.ai_disease_diagnose, name='aidiseasediagnose'),
    path('aisolutions/aidiseasediagnose/pichandle_classification/', ai_solutions.pic_handle_classification, name='pichandle_classification'),
    path('aisolutions/aidiseasediagnose/pichandle_yolov5/', ai_solutions.pic_handle_yolov5, name='pichandle_yolov5'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': 'main/static/'}),

    path('aisolutions/virtualrealityforesttherapy/<int:page>/', ai_solutions.virtual_reality_forest_therapy, name='virtual_reality_forest_therapy'),
    path('aisolutions/virtualrealityforesttherapy/digital_twin/', ai_solutions.digital_twin, name='digital_twin'),
    path('aisolutions/virtualrealityforesttherapy/vr_detail/', ai_solutions.vr_detail, name='vr_detail'),


    #path('', HomeView.as_view(), name='index'),
    path('consulting/', HomeView.as_view(), name='consulting'),
    path('consulting/my_share', MyShare.as_view(), name='my_share'),
    path('consulting/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('consulting/creatingPost/', CreatePost.as_view(), name='create_post'),
    path('consulting/<int:pk>/commentPost/', AddComment.as_view(), name='add_comment'),
    path('consulting/experts', Experts.as_view(), name='experts'),
    path('like/<int:pk>', LikeView, name='like_post'),
    path('consulting/', ReverseView.as_view(), name='reverse_post'),
    path('consulting/sorted/', SortedView.as_view(), name='sorted_post'),
    path('consulting/hot/', HotView.as_view(), name='hot_post'),
    path('my_plants/', my_plants.as_view(), name='my_plants'),
    path('manage_plants/<int:pk>/', manage_plants.as_view(), name='manage_plants'),
    path('add_plants/', add_plants.as_view(), name='add_plants'),
    path('plants_care/<int:pk>', plants_care.as_view(), name='plants_care'),
    path('diagnose/<int:pk>', diagnoseView, name='diagnose'),
    path('delete_plants/<int:pk>', delete_plants.as_view(), name='delete_plants'),
    path('shopping_carts/', shopping_carts.as_view(), name='shopping_carts'),


    path('consulting/<int:post_id>/<int:rating>/', PostRate, name='post_rate'),
    path("checkout/", checkout, name="checkout"),
    path("checkout/create_wechat_pay_payment_intent", payment.create_wechat_pay_payment_intent, name="create_wechat_pay_payment_intent"),
    path("checkout/create_alipay_payment_intent", payment.create_alipay_payment_intent, name="create_alipay_payment_intent"),
	  path('success/', success, name='success'),
    path('cancel/', cancel, name='cancel'),
    path('cart/', view_cart, name='veiw_cart'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
]
