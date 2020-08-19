from rest_framework import serializers
from .models import User,Tag,Post,Comment,Subscription
from rest_flex_fields import FlexFieldsModelSerializer

from django.contrib.auth.password_validation import validate_password


class SubscriptionSerializer(serializers.ModelSerializer):
  target = serializers.ReadOnlyField(source='target.username')
  source = serializers.ReadOnlyField(source='source.username') 
  class Meta:
    model = Subscription
    fields = ['id','source','target']



class TagSerializer(FlexFieldsModelSerializer):
  class Meta:
    model = Tag
    fields = ['name','id']


class CommentSerializer(serializers.ModelSerializer):
  author = serializers.ReadOnlyField(source='author.username')

  class Meta: 
    model = Comment
    fields = ['author','id','content','published_date']

class PostSerializer(FlexFieldsModelSerializer):
  author = serializers.ReadOnlyField(source='author.username')
  class Meta:
    model = Post
    fields = [
      'id',
      'author',
      'title',
      'content',
      'published_date',
      'tags'
    ]
    expandable_fields = {
      'tags': (TagSerializer, {'many': True})
    }

'''
  Explicacion : esto es un poco hacky pero es la unica manera que consegui 2 cosas
  1) que cuando pido las subcripciones de un usuario me devuelva solo los nombres 
  2) que cuando creo un usuario no requiera subscripciones

  no comprendo muy bien por que nececito esto pero termine probando muchas cosas
  y encontre "serializers.RealatedField" en la documentacion de django_rest_framework ,
  con django-flex-fields no pude hacerlo
'''

class UserOfSubscription(serializers.RelatedField):
  def to_representation(self, value):
      return value.username

class UserSerializer(FlexFieldsModelSerializer):
  first_name = serializers.CharField(max_length=128,required=True)
  password1 = serializers.CharField(write_only=True,max_length=64)
  password2 = serializers.CharField(write_only=True,max_length=64)
  subscription_users = UserOfSubscription(many=True,read_only=True)
  class Meta:
    model = User
    fields = [
      'id',
      'username',
      'password1',
      'password2',
      'age',
      'first_name',
      'description',
      'subscription_users'
    ]

  def validate_password1(self,value):
    validate_password(value)
    return value
  
  def validate(self,data): 
    data = super().validate(data)
    password1 = data.get('password1')
    password2 = data.get('password2')
    if password1 != password2:
      raise serializers.ValidationError("the passwords didn't match")
    return data
  
  def create(self, validated_data):
    password = validated_data.pop('password1')
    validated_data.pop('password2')
    validated_data['password'] = password
    user = User.objects.create_user(**validated_data)
    return user
