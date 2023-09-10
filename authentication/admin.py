from django.contrib import admin

from main.models import Post
from main.models import Comment
from .models import User, Expert

admin.site.register(User)
admin.site.register(Expert)
admin.site.register(Post)
admin.site.register(Comment)
