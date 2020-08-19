from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view,permission_classes 
from rest_framework import status,viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import ReadOnlyOrIsCreator
from .filters import PostFilter
from .serializers import UserSerializer,TagSerializer,PostSerializer,CommentSerializer,SubscriptionSerializer
from .models import Tag,Post,Comment,Token,Subscription,User



@api_view(['POST','DELETE'])
@permission_classes([IsAuthenticated])
def subscription(request):
  target = request.data.get('target-username',None)
  if target == None or ( not target.strip() ) :
    return Response({'errors':'target-username is required'},status=status.HTTP_400_BAD_REQUEST)
  user_source = request.user
  try:
    user_target = User.objects.get(username=target)
  except:
    return Response({'errors':"target username don't exist"})
  if request.method == 'POST' :
    try:
      sub = Subscription.objects.get(source=user_source,target=user_target)
      return Response({'errors':'subscription already exists'},status=status.HTTP_400_BAD_REQUEST)
    except :
      sub = Subscription.objects.create(source=user_source,target=user_target)
      sub_ser = SubscriptionSerializer(sub)
      return Response(sub_ser.data)
  elif request.method == 'DELETE':
    try:
      #cannot possible delete other user sub because user_source depends on the req token
      sub = Subscription.objects.get(source=user_source,target=user_target)
      sub.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
    except :
      return Response({'errors':"subscription don't exist"},status.HTTP_400_BAD_REQUEST)





class CommentViewSet(viewsets.ModelViewSet):
  serializer_class = CommentSerializer
  permission_classes = [ReadOnlyOrIsCreator]
  def get_queryset(self):
      return Comment.objects.filter(post=self.kwargs['post_pk'])
  def perform_create(self,serializer):
    post_id = self.kwargs['post_pk']
    post = Post.objects.get(id=post_id)
    serializer.save(post=post,author = self.request.user)

class PostViewSet(viewsets.ModelViewSet):
  filter_class = PostFilter
  queryset = Post.objects.all()
  permission_classes = [ReadOnlyOrIsCreator]
  serializer_class = PostSerializer

  def perform_create(self,serializer):
    serializer.save(author = self.request.user)

class TagViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Tag.objects.all()
  serializer_class = TagSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user(request):
  user_ser = UserSerializer(request.user)
  return Response(user_ser.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test(request):
  user_ser = UserSerializer(request.user)
  return Response({'token':user_ser.data })


@api_view(['POST'])
def register(request):
  user_ser = UserSerializer(data=request.data)
  if user_ser.is_valid():
    user = user_ser.save()
    token = Token.create(user)
  else:
    return Response(user_ser.errors,status=status.HTTP_400_BAD_REQUEST)
  json_res = {
    'user': user_ser.data,
    'token' : token.value
  }
  return Response(json_res,status=status.HTTP_201_CREATED)

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
    token = Token.objects.get(user = user)
    return Response({'token':token.value},status=status.HTTP_200_OK)
  else :
    if not errors:
      errors['global'] = 'could not find user with these credentials'
    return Response(errors,status=status.HTTP_401_UNAUTHORIZED)
