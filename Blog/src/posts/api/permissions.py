from email import message
from rest_framework.permissions import BasePermission

#--- Custom Permission to Define user is the Owner of Object
class IsOwnerorReadOnly(BasePermission):
    message = "You must be owner of this object"
    my_safe_method = ['GET','PUT']
    def has_permission(self, request, view):
        if request.method in self.my_safe_method:
            return True
        return False

    def has_object_permission(self, request, view, obj):

        if request.method in self.my_safe_method:
            return True
        return obj.user == request.user