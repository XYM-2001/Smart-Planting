import collections
import openai
import logging

from unicodedata import name
from attr import fields
from django import forms
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView,DeleteView,CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from authentication.utils.check_login_state import check_login
from main.serializer import CartItemSerializer
from main.utils.ai_solutions_utils import *
from main.models import Cart, CartItem, Post, Rating, CustomerPost, ExpertPost
from main.models import Comment
from authentication.models import User, Expert
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpRequest, HttpResponse
from datetime import datetime

#from authentication.form import CommentForm

logger = logging.getLogger(__name__)
def index(request):
    return render(request, 'main/consulting.html', {})

sort=0 
"""
0: regular 
1: reverse
2: hot
"""


class HomeView(ListView):
    model = Post
    template_name = 'main/consulting.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['object_list'] = context['object_list'][::-1]
        for object in context['object_list']:
            object_author = object.author
            if Expert.objects.filter(user__name=object_author).exists():
                print('true\n')
                object.status = True
            else:
                print('false\n')
                object.status = False   
        return context
        
def get_ai_answer(question):
    openai.api_key = "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"
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=question,
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    response = (response["choices"][0]["text"]).strip()
    return response
    
#@method_decorator(check_login, name='dispatch')
class PostDetail(DeleteView):
    model = Post
    template_name = 'main/post_detail.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.user = get_object_or_404(User, pk=request.session['user_id'])
        except: 
            self.user = user = User.objects.get(name='Guest')
        
        self.p = get_object_or_404(Post, id=self.kwargs['pk'])
        if not self.p.author:
            self.p.author = self.user
            # send post to our email
            send_mail(
                "Post update",
                f"Hello, \n\nThe user: {self.p.author.name}({self.p.author.email}) has shared a post.\nPost title: {self.p.title}\nPost content: {self.p.content}\nPlease check the detail at Smartplanting.net as admin.\n\nThank you!",
                "visionxsmartplanting@gmail.com",
                ["rundi.liu26@visionx.org"]
            )
        self.p.save()

        Comment.objects.filter(name=None).update(name=self.user.name)
        self.p.post_views = self.p.post_views + 1
        self.p.save()

        if not Comment.objects.filter(post=self.p,name='SmartPlanting'):
            question = self.p.content
            ai_comment = get_ai_answer(question)
            record = Comment(
                post=self.p,
                name='SmartPlanting',
                content=ai_comment,
                date_added = datetime.now()
            )
            record.save()

        return super(PostDetail, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        # context['customer_posts'] = CustomerPost.objects.all()
        # context['expert_posts'] = ExpertPost.objects.all()
        ob = get_object_or_404(Post, id=self.kwargs['pk'])
        context["num_likes"] = ob.num_likes
        rating = Rating.objects.filter(post=self.p, user=self.user).first()
        context['post'].user_rating = rating.rating if rating else 0
        return context
    

#@method_decorator(check_login, name='dispatch')
class CreatePost(CreateView):
    def dispatch(self, request, *args, **kwargs):
        try:
            self.user = get_object_or_404(User, pk=request.session['user_id'])
        except: 
            self.user = user = User.objects.get(name='Guest')

        if Expert.objects.filter(user__name=self.user.name).exists():
            self.model = ExpertPost
            print(self.user.name)
        else:
            self.model = CustomerPost
            print("no expert")

        self.template_name: str = 'main/create_post.html' # same w render(request, teplate_name)
        self.fields = ['title', 'image', 'content']

        return super(CreatePost, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

#@method_decorator(check_login, name='dispatch')
class AddComment(CreateView):
    model = Comment
    #form_class = CommentForm
    template_name = 'main/add_comment.html'
    fields = ['post', 'content']

    def get_context_data(self, **kwargs):
        context = super(AddComment, self).get_context_data(**kwargs)
        ob = get_object_or_404(Post, id=self.kwargs['pk'])
        context["form"].fields["post"].queryset = Post.objects.filter(title=ob.title, author=ob.author)
        return context
    
class Experts(ListView):
    model = Post
    template_name = 'main/experts.html'
    fields = '__all__'

class MyShare(ListView):
    model = Post
    template_name = 'main/my_share.html'

@check_login
def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id')) # grab in detail html
    try:
        user = get_object_or_404(User, pk=request.session['user_id'])
    except:
        user = User.objects.get(name='Guest')
    if user not in post.likes.all():
        post.likes.add(user)
    else:
        post.likes.remove(user)
    return HttpResponseRedirect(reverse('main:post_detail', args=[str(pk)]))

def PostRate(request, post_id, rating):
    post = get_object_or_404(Post, id=post_id)
    try:
        user = get_object_or_404(User, pk=request.session['user_id'])
    except:
        user = User.objects.get(name='Guest')
    Rating.objects.filter(post=post, user=user).delete()
    post.rating_set.create(user=user, rating=rating)
    return HttpResponseRedirect(reverse('main:post_detail', args=[str(post_id)]))

class SortedView(ListView):
    model = Post
    template_name = 'main/consulting.html'

    def get_context_data(self, **kwargs):
        context = super(SortedView, self).get_context_data(**kwargs)
        return context

class ReverseView(ListView):
    model = Post
    template_name = 'main/consulting.html'

    def get_context_data(self, **kwargs):
        context = super(ReverseView, self).get_context_data(**kwargs)
        new_context = context
        new_context['object_list'] = new_context['object_list'].order_by('-date_added')
        return new_context

class HotView(ListView):
    model = Post
    template_name = 'main/consulting.html'

    def get_context_data(self, **kwargs):
        context = super(HotView, self).get_context_data(**kwargs)
        hot_context = context
        hot_context['object_list'] = hot_context['object_list'].order_by('-post_views')
        return hot_context

class CartView(APIView):
     
    def get(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user,ordered=False).first()
        queryset = CartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user, ordered=False)
        product = Product.objects.get(id=data.get('product'))
        price = product.price
        quantity = data.get('quantity')
        cart_items = CartItem(cart=cart, user=user, product=product, price=price, quantity=quantity)
        cart_items.save()

        cart_items = CartItem.objects.filter(user=user, cart=cart.id)
        cart.total_price = sum([i for i in cart_items])
        cart.save()

        return Response({'success': 'Items Added'})

    def put(self, request):
        data = request.data
        cart_item = CartItem.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Items Updated'})

    def delete(self, request):
        user = request.user
        data = request.data
        cart_item = CartItem.objects.get(id=data.get('id'))
        cart_item.delete()
        cart = Cart.objects.filter(user=user, ordered=False).first()
        queryset = CartItem.objects.filter(cart=cart)
        serialier = CartItemSerializer(queryset, many=True)
        return Response(serialier.data)

@method_decorator(check_login, name='dispatch')
class shopping_carts(ListView):
    model = CartItem
    template_name = 'main/shopping_carts.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            self.user = get_object_or_404(User, pk=request.session['user_id'])
        except:
            self.user = user = User.objects.get(name='Guest')
        return super(shopping_carts, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['object_list'] = CartItem.objects.order_by('id')
        return super(shopping_carts, self).get_context_data(**kwargs)


