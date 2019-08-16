from rest_framework import authentication, exceptions, permissions
from .models import User

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and obj.user == request.user)

class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

class CodeAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        header = request.META.get('HTTP_AUTHORIZATION')
        code = None

        if header and len(header.split(" ")) == 2:
            code = header.split(" ")[1]

        if not code:
            return None

        try:
            user = User.objects.get(code=code)
        except User.DoesNotExist:
            return None

        return (user, None)