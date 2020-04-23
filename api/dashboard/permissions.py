from rest_framework.permissions import BasePermission



class HasThisViewScope(BasePermission):
    message = "intended action is not permitted for this api key"

    def has_permission(self, request, view):
        cls = view.__class__
        try:
            pass
        except AttributeError:
            print('no such attribute exist')
        return True