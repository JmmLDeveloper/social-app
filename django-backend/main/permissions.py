from rest_framework import permissions

'''
  allows to read a list or a individual item
  but only allows you to create an item if you are authenticated
  and only allows you to write (edit,delete,ath) an item 
  if you are the owner of that item

  because Comment and Post both have an author field it works with 
  both models 
'''

class ReadOnlyOrIsCreator(permissions.BasePermission):

  def has_permission(self, request, view):
    if request.method in permissions.SAFE_METHODS:
      return True
    if request.user :
      return True
    else :
      return False 


  def has_object_permission(self, request, view, obj):
    if request.method in permissions.SAFE_METHODS:
        return True
    return obj.author == request.user