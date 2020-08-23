from django.db import models
import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Product(models.Model):
    code = models.CharField("identificador del producto", max_length=64, error_messages={
        'required': 'green i not a primary color'
    })
    stock_number = models.IntegerField(verbose_name="Cantidad En Alamacene",
                                       error_messages={
                                           'required': 'Ya existe un color con ese nombre'
                                       }
                                       )


class User(AbstractUser):
    age = models.IntegerField()
    description = models.CharField(max_length=128)
    # list of users , this user has subscribe to
    REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS + ['age', 'description']
    subscription_users = models.ManyToManyField(
        'self',
        through='Subscription',
        symmetrical=False,
        through_fields=('source', 'target'),
        blank=True
    )

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Token.create(self)
# this model could store info about a subscription
# for now it just store the date of the subscription but it could be user for more


class Subscription(models.Model):
    # the user that subscribe
    source = models.ForeignKey(
        User, related_name='source', on_delete=models.CASCADE)
    # the user being that is being subscribed to
    target = models.ForeignKey(
        User, related_name='target', on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('source', 'target')

    def __str__(self):
        return f'{self.source.username} => {self.target.username} at {self.issued_at}'


class Tag(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(
        User, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    # black to allow users to create posts without tags
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class Token(models.Model):
    value = models.CharField(max_length=512)
    # need this field because it will be annoying to have to:
    # get all tokens -> decode them -> get the one with the right sub
    # instead with this i can get the right token directly
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.value

    @staticmethod
    def create(user):
        if type(user) != User:
            raise Exception('create method expect a "User" class')
        id = user.id
        token = jwt.encode({'sub': id}, settings.SECRET_KEY).decode('utf-8')
        return Token.objects.create(value=token, user=user)
