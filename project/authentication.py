from rest_framework import authentication
from rest_framework import exceptions

from base.models import UserAuthInfo

class AccessTokenAuthentication(authentication.BaseAuthentication):


    def authenticate(self, request):
        access_token = request.META.get('HTTP_AUTHORIZATION') # get the username request header
        if not access_token: #no access token in the request.header's
            return None #authentication did not succeed

        try:
            user = UserAuthInfo.objects.get(access_token = access_token)
        except UserAuthInfo.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user.user,access_token)