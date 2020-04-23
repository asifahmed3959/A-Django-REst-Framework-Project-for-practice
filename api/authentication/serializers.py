from rest_framework import serializers

from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.settings import api_settings

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.text import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from rest_framework import exceptions

from nanoid import generate

from base.models import UserAuthInfo

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class LoginSerializer(serializers.Serializer):
    """
    takes in username and password and login the user
    """
    username_or_email = serializers.CharField(max_length=256, required=True)
    password = serializers.CharField(max_length=256, required=True)

    default_error_messages = {
        "email_not_verified": _("not a valid email id or username"),
        "wrong_password": _("provided password does not match")
    }

    def validate(self, attrs):
        username_or_email = attrs['username_or_email']
        password = attrs['password']

        user_username = User.objects.filter(username__iexact=username_or_email).first()
        user_email = User.objects.filter(email__iexact=username_or_email).first()

        if user_email and user_username is None:
            msg = self.default_error_messages['email_not_verified']
            raise exceptions.AuthenticationFailed(msg)

        if user_username:

            if not user_username.check_password(password):
                msg = self.default_error_messages['wrong_password']
                raise exceptions.AuthenticationFailed(msg)
            refresh = RefreshToken.for_user(user_username)
            data = {
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token)

            }
        else:

            if not user_email.check_password(password):
                msg = self.default_error_messages['wrong_password']
                raise exceptions.AuthenticationFailed(msg)

            refresh = RefreshToken.for_user(user_email)
            data = {
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token)

            }

        attrs['data'] = data
        return attrs


class OauthTokenSerializer(LoginSerializer):

    def validate(self, attrs):
        username_or_email = attrs['username_or_email']
        password = attrs['password']

        user_username = User.objects.filter(username__iexact=username_or_email).first()
        user_email = User.objects.filter(email__iexact=username_or_email).first()

        if user_email and user_username is None:
            msg = self.default_error_messages['email or username not verified']
            raise exceptions.AuthenticationFailed(msg)

        if user_username:

            if not user_username.check_password(password):
                msg = self.default_error_messages['wrong_password']
                raise exceptions.AuthenticationFailed(msg)
            access_token = generate(size=48)
            person, created = UserAuthInfo.objects.update_or_create(
                user=user_username, defaults={"access_token": access_token}
            )
            data = {
                'access_token': str(access_token)
            }
        else:

            if not user_email.check_password(password):
                msg = self.default_error_messages['wrong_password']
                raise exceptions.AuthenticationFailed(msg)

            access_token = generate(size=48)
            person, created = UserAuthInfo.objects.update_or_create(
                user=user_email, defaults={"access_token": access_token}
            )
            data = {
                'access_token': str(access_token)
            }

        attrs['data'] = data
        return attrs
