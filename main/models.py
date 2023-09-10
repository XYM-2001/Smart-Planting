from cProfile import label
from collections import UserList
from datetime import datetime
from distutils.command.upload import upload
import uuid
from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from numpy import product
from authentication.models import User, Expert
from django.db.models.signals import pre_save
from django.db.models import Avg

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(max_length=556)
    image = models.ImageField()
    price = models.FloatField(default=0.0)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    isPromotion = models.BooleanField(default=False)
    isVR = models.BooleanField(default=False)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

    class Meta:
        ordering = ['isPromotion']

class QuantityVariant(models.Model):
    variant_name = models.CharField(max_length=100)

    def __str__(self):
        return self.variant_name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'cart')
    product_id = models.UUIDField()
    #product_num = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(999)])
    c_time = models.DateTimeField(auto_now_add=True)
    #checked_out = models.BooleanField(default=False, verbose_name=_('checked out'))
    ordered = models.BooleanField(default=False)
    total_price = models.FloatField(default=0)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name + '|' + str(self.total_price)

    class Meta:
        ordering = ['c_time']

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name = 'cart_items')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, null = True, blank = True)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.user.name) + '|' + str(self.product.description)

@receiver(pre_save, sender=CartItem)
def correct_price(sender, **kwargs):
    cart_items = kwargs['instance']
    price_of_product = Product.objects.get(id=cart_items.product.id)
    cart_items.price = cart_items.quantity * float(price_of_product.price)
    total_cart_items = CartItem.objects.filter(user = cart_items.user)
    cart_items.total_items = len(total_cart_items)
    cart = Cart.objects.get(id = cart_items.cart.id)
    cart.total_price = cart_items.price
    cart.save()

class Post(models.Model):
    title = models.CharField(max_length=49)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    content = models.TextField(max_length=999, default='Nothing Here')
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    post_views=models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='like_post')
    image = models.ImageField(upload_to='user_image/', null=True, blank=True)

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    def get_absolute_url(self):
        id = self.id
        post = get_object_or_404(Post, pk=id)
        return reverse('main:post_detail', args=[id])

    def num_likes(self):
        return self.likes.count()

    def num_comments(self):
        return len(Comment.objects.filter(post=self.id))

    def num_views(self):
        return self.post_views
    
    def average_rating(self) -> float:
        return Rating.objects.filter(post=self).aggregate(Avg("rating"))["rating__avg"]

class CustomerPost(Post):
    customer = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' | ' + str(self.author)
    
class ExpertPost(Post):
    expert = models.ForeignKey(Expert, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' | ' + str(self.author)

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.post.id}: {self.post.author}: {self.rating}"

class AddPost(models.Model):
    title = models.CharField(max_length=49)
    author = models.ForeignKey(User, null=True,on_delete=models.CASCADE,)
    content = models.TextField(max_length=999, default='Nothing Here')

    def get_absolute_url(self):
        id = self.id
        return reverse('main:post_detail', args=[id])

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=166, null=True)
    #name = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    content = models.TextField(max_length=999)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)

    def get_absolute_url(self):
        id = self.post.id
        return reverse('main:post_detail', args=[id])

    def get_user(self):
        return User.objects.get(name=self.name)

    #def sample_view(request):
        #current_user = request.user
        #return current_user

"""
class Profile(models.Model):
    user = models.OneToOneField(User, )
class Post():
    d = 1
class Comment(models.Model):
    post = models.ForeignKey(Cart, related_name="comments" on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
"""
class Plant(models.Model):
    name = models.CharField(max_length=128, null=True)
    category = models.CharField(max_length=50, null=True)
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE,)
    age = models.SmallIntegerField(default=0)
    image = models.ImageField(upload_to='plants/image', default='user_image/no_image.jpeg')
    HEALTH_CHOICES = (
        ('Good', 'Good'),
        ('Normal', 'Normal'),
        ('Bad',  'Bad'),
    )
    health = models.CharField(max_length=20, choices=HEALTH_CHOICES, default='Good')
    diagnose = models.BooleanField(default=False)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:my_plants')

    def get_user(self):
        return User.objects.get(name=self.owner.name)
