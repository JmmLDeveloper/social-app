from django.urls import path,include
from rest_framework_nested import routers
from .views import register,login,test,user,TagViewSet,PostViewSet,CommentViewSet,subscription

router = routers.SimpleRouter()

router.register('tags', TagViewSet)
router.register('posts', PostViewSet)

posts_router = routers.NestedSimpleRouter(router, 'posts', lookup='post')

posts_router.register('comments', CommentViewSet,basename='post-comments') 

app_name = 'main'

urlpatterns = [
    path('',include(router.urls)),
    path('',include(posts_router.urls)),
    path('register/',register,name= 'register') ,
    path('login/',login,name= 'login'),
    path('user/',user),
    path('subscription/',subscription)
]
