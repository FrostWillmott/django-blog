from dj_rest_auth import views as auth_views
from django.contrib.auth import logout as django_logout, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from . import serializers
from .services import AuthAppService, full_logout
from main.models import User
from main.tasks import send_information_email


class SignUpView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserSignUpSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = AuthAppService()
        user = service.create_user(serializer.validated_data)
        send_information_email.delay(
            subject="Successful registration!",
            template_name="emails/confirmation_email.html",
            context={'user': user.full_name, 'activate_url': service.get_activate_url(user)},
            to_email=user.email,
        )
        return Response(
            {'detail': _('Confirmation email has been sent')},
            status=status.HTTP_201_CREATED,
        )



class LoginView(auth_views.LoginView):
    serializer_class = serializers.LoginSerializer


class LogoutView(auth_views.LogoutView):
    allowed_methods = ('POST', 'OPTIONS')

    def session_logout(self):
        django_logout(self.request)

    def logout(self, request):
        response = full_logout(request)
        return response


class PasswordResetView(GenericAPIView):
    serializer_class = serializers.PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {'detail': _('Password reset e-mail has been sent.')},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = serializers.PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {'detail': _('Password has been reset with the new password.')},
            status=status.HTTP_200_OK,
        )


class VerifyEmailView(GenericAPIView):
    serializer_class = serializers.VerifyEmailSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if user and not user.is_active and user.confirmation_key == serializer.validated_data['key']:
            user.is_active = True
            user.confirmation_key = None
            user.save()
            return Response(
                {'detail': _('Email verified')},
                status=status.HTTP_200_OK,
            )
        return Response(
            {'detail': _('Invalid or expired confirmation link.')},
            status=status.HTTP_400_BAD_REQUEST,
        )
