from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.decorators import APIView, permission_classes
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .serializers import RefreshTokenSerializer
from .serializers import LoginSerializer
from .serializers import UserSerializer
from .serializers import ChangePasswordSerializer
from .serializers import OauthTokenSerializer


User = get_user_model()


class user_registration(GenericAPIView):
    """
    create a new user.
    """
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response({"logout":"validated"})


class UpdatePassword(APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"password":"your password has been changed"},status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self,request,format = None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response (serializer.validated_data['data'],status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthLogin(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self,request,format = None):
        serializer = OauthTokenSerializer(data=request.data)
        if serializer.is_valid():
            return Response (serializer.validated_data['data'],status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)