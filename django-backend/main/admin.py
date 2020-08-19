from django.contrib import admin
from .models import Tag,Post,Comment,User,Token,Subscription


admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Token)
admin.site.register(Tag)
admin.site.register(Subscription)
