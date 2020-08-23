from django.urls import path, include
from rest_framework_nested import routers
from .views import (
    register,
    login,
    test,
    user,
    TagViewSet,
    PostViewSet, 
    CommentViewSet, 
    SubscriptionView, 
    cache_post,
    ProductViewSet
)

router=routers.SimpleRouter()

router.register('tags', TagViewSet)
router.register('posts', PostViewSet)
router.register('products',ProductViewSet)

posts_router=routers.NestedSimpleRouter(router, 'posts', lookup='post')

posts_router.register('comments', CommentViewSet, basename='post-comments')

app_name='main'

urlpatterns=[
    path('cache-post/<int:pk>', cache_post),
    path('', include(router.urls)),
    path('', include(posts_router.urls)),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('user/', user),
    path('subscription/', SubscriptionView.as_view(), name='subscription'),
    path('test/', test)
]
