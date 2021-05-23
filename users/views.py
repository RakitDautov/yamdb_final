from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, filters, serializers
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdminOrReadOnly
from .serializers import UserSerializer, UserRegistrationSerializer

User = get_user_model()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@api_view(["post"])
@permission_classes([AllowAny])
def registration_email(request):
    email = request.data.get("email")
    serializer = UserRegistrationSerializer(data=request.data, partial=True)
    confirmation_code = BaseUserManager.make_random_password(settings.CODE_LEN)
    serializer.is_valid(raise_exception=True)
    serializer.save(
        username=email, email=email, confirmation_code=confirmation_code
    )
    send_mail(
        "Api_yamdb регистрация",
        f"Используйте пароль для завершения регистрации {confirmation_code}",
        from_email=None,
        recipient_list=[email],
    )

    return Response(
        "Подтвердите свой адрес электронной почты для завершения регистрации",
        status=status.HTTP_200_OK,
    )


@api_view(["post"])
@permission_classes([AllowAny])
def token(request):
    email = request.data.get("email")
    confirmation_code = request.data.get("confirmation_code")
    user = get_object_or_404(User, email=email)
    if user.confirmation_code != confirmation_code:
        raise serializers.ValidationError("Bad confirmation_code")
    token = get_tokens_for_user(user)
    user.save()
    user_data = {
        "email": user.email,
        "confirmation_code": confirmation_code,
        "token": token,
    }
    return Response(user_data, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = [
        "username",
    ]
    search_fields = [
        "username",
    ]
    lookup_field = "username"
    queryset = User.objects.all()

    @action(
        methods=["get", "patch"],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        instance = get_object_or_404(User, username=self.request.user.username)

        serializer = self.get_serializer(instance)

        if request.method == "PATCH":
            serializer = self.get_serializer(
                instance, data=self.request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=instance.role, partial=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
