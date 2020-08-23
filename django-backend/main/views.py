from django.shortcuts import render
from django.contrib.auth import authenticate
from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import JSONParser

from .permissions import ReadOnlyOrIsCreator
from .filters import PostFilter
from .serializers import UserSerializer, TagSerializer, PostSerializer, CommentSerializer, SubscriptionSerializer, ProductSerializer
from .models import Tag, Post, Comment, Token, Subscription, User, Product

from .forms import ProductForm

import redis
import io

import json


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


@api_view(["GET"])
def cache_post(request, pk):

    redis_con = redis.Redis(host='localhost', port=6379, db=0)

    bstring_post = redis_con.get(f'post-{pk}')
    if bstring_post:
        print('FROM CACHE')
        post_data = JSONParser().parse(io.BytesIO(bstring_post))
        post_ser = PostSerializer(data=post_data)
        if post_ser.is_valid():
            return Response(data=post_ser.data)
    print('FROM DATABASE')
    post = Post.objects.get(id=pk)
    post_ser = PostSerializer(post)
    redis_con.setex(f'post-{pk}', 3600, json.dumps(post_ser.data))
    return Response(post_ser.data)


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def valid_target(self):
        target = self.request.data.get('target-username', None)
        if target == None or (not target.strip()):
            self.errorRes = Response(
                {'errors': 'target-username is required'}, status=status.HTTP_400_BAD_REQUEST)
            return False
        try:
            self.target = User.objects.get(username=target)
            return True
        except:
            self.errorRes = Response(
                {'errors': "target username don't exist"}, status=status.HTTP_400_BAD_REQUEST)
            return False

    # create subscription if it dosent exists
    def post(self, request, format=None):
        if not self.valid_target():
            return self.errorRes
        try:
            sub = Subscription.objects.get(
                source=self.request.user, target=self.target)
            return Response({'errors': 'subscription already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            sub = Subscription.objects.create(
                source=self.request.user, target=self.target)
            sub_ser = SubscriptionSerializer(sub)
            return Response(sub_ser.data)

    # delete the user subscription if it exists
    def delete(self, request, format=None):
        if not self.valid_target():
            return self.errorRes
        try:
            sub = Subscription.objects.get(
                source=self.request.user, target=self.target)
            sub.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'errors': "subscription don't exist"}, status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [ReadOnlyOrIsCreator]

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['post_pk'])

    def perform_create(self, serializer):
        post_id = self.kwargs['post_pk']
        post = Post.objects.get(id=post_id)
        serializer.save(post=post, author=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    filter_class = PostFilter
    queryset = Post.objects.all()
    permission_classes = [ReadOnlyOrIsCreator]
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user(request):
    user_ser = UserSerializer(request.user)
    return Response(user_ser.data)


def test(request):
    context = {
        'form': ProductForm()
    }
    if request.method == 'POST':
        context = {
            'form': ProductForm(request.POST)
        }
    return render(request, 'index.html', context)


@api_view(['POST'])
def register(request):
    user_ser = UserSerializer(data=request.data)
    if user_ser.is_valid():
        user_ser.save()
        return Response(user_ser.data, status=status.HTTP_201_CREATED)
    else:
        return Response(user_ser.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    errors = {}
    if not username:
        errors['username'] = 'username field cant be empty'
    if not password:
        errors['password'] = 'password field cant be empty'

    user = authenticate(username=username, password=password)
    if user != None:
        token = Token.objects.get(user=user)
        return Response({'token': token.value}, status=status.HTTP_200_OK)
    else:
        if not errors:
            errors['global'] = 'could not find user with these credentials'
        return Response(errors, status=status.HTTP_401_UNAUTHORIZED)
