import hmac
import hashlib
import base64
import json

from rest_framework import exceptions
# from rest_framework.authentication import BaseAuthentication
#
# from base.models import APISecret
#
# def get_authorization_header(request):
#     public_key = request.META.get('HTTP_X_APPLOYE_PUBLIC_KEY')
#     signature = request.META.get('HTTP_X_APPLOYE_SIGNATURE')
#     return public_key, signature
#
#
#
# class SharedSecretBackend(BaseAuthentication):
#     def authenticate(self, request, *args, **kwargs):
#         public_key, signature = get_authorization_header(request)
#
#         if public_key is None or type(public_key) != str or len(public_key) != 18 or not public_key.startswith('pk_'):
#             raise exceptions.AuthenticationFailed('invalid or no public key')
#
#         try:
#             api_secret=APISecret.objects.get(public_key=public_key)
#         except APISecret.DoesNotExist:
#             raise exceptions.AuthenticationFailed('invalid or no public key')
#
#         user = api_secret.user
#         secret_key = api_secret.secret_key
#
#         if request.method == 'GET' and request.data == {}:
#             data = None
#         else:
#             data = request.data
#
#         data = json.dumps(data, sort_keys=True)
#
#         digest = hmac.new(secret_key.encode('utf-8'), data.encode('utf-8'), hashlib.sha1).digest()
#         calculated_signature = base64.urlsafe_b64encode(digest).decode('utf-8')
#
#         if signature != calculated_signature:
#             raise exceptions.AuthenticationFailed("signature mismacth")
#
#         return user, api_secret