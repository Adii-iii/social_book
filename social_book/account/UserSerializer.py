from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

class UserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = get_user_model()
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name')