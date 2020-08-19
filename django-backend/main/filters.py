import rest_framework_filters as filters
from django.db.models import Q
from .models import Post

class PostFilter(filters.FilterSet):
  subs_only = filters.BooleanFilter(method='subs_only_filter')
  class Meta:
    model = Post
    fields = ['tags']
  
  def subs_only_filter(self,queryset,name,value):
    if not self.request.user:
      return queryset
    subscription_users = self.request.user.subscription_users.all()
    query = None
    for user in subscription_users:
      if query == None :
        query = Q(author=user)
      else:
        query = Q(author=user) | query 
    return queryset.filter(query)
