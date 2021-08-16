from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import CustomUser
from account.serializers import RegisterSerializer, CreateNewPasswordSerializer
from .utils import send_activation_code


class RegisterView(APIView):

    def post(self, request):
        data = request.data
        print(request.data)
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Successfuly registered!', 201)


class ActivationView(APIView):

    def get(self, request, email, activation_code):
        user = CustomUser.objects.filter(email=email, activation_code=activation_code).first()

        if not user:
            return Response('This user does not exist', 400)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response('MOLODEC!!!!!', 200)


# password reset
class PasswordResetView(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        # query_params = возвращает словарь, и тут все что после вопросительного знака в url
        user = get_object_or_404(CustomUser, email=email)
        user.is_active = False
        user.create_activation_code()
        user.save()
        send_activation_code(email=user.email, activation_code=user.activation_code,
                             status='reset_password')

        return Response('Check your email for resetting your password.', status=200)


# password reset
class CompleteResetPasswordView(APIView):
    def post(self, request):
        serializer = CreateNewPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('вы успешно восстановили пароль!', status=200)
































