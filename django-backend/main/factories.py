import factory
from . import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.User
    
    username = 'jhonnyx6'
    email = 'jhon@email.com'
    password = '123456*ABC' 
    first_name = 'Jhon'
    age = 25
    description = 'i am a test uset , and i am gonna die :('


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Post
    title = 'post title'
    content  = 'this is the content of the post'

