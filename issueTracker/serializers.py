from rest_framework.serializers import ModelSerializer, ValidationError

from .models import Users, Contributors, Projects, Issues, Comments


class SignupUserSerializer(ModelSerializer):

    class Meta:
        model = Users
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}}

    def create_user(self, first_name, last_name, email, username, password):
        user = Users.objects.create()
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        user.set_password(password)
        user.save()
        return user




class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Projects
        fields = ['title', 'description', 'type']


class ProjectDetailSerializer(ModelSerializer):

    class Meta:
        model = Projects
        fields = ['title', 'description', 'type', 'author_user_id']
        extra_kwargs = [{'author_user_id': {'read_only': True}}]
