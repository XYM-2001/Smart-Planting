from atexit import register
from django.contrib import admin
from .models import Product, Cart, Post, Plant, CartItem, Rating, CustomerPost, ExpertPost


admin.site.register(Product)
admin.site.register(Cart)
#admin.site.register(Post)
admin.site.register(CartItem)
admin.site.register(Plant)
admin.site.register(Rating)
admin.site.register(CustomerPost)
admin.site.register(ExpertPost)



class PostAdmin(admin.ModelAdmin):
    list_display = ('title','content')
    actions = None

    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        obj.save()
