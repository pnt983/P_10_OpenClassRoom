from rest_framework.serializers import ModelSerializer

from .models import Users, Contributors, Projects, Issues, Comments


class UserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'first_name', 'last_name']


class ContributorsSerializer(ModelSerializer):
    class Meta:
        model = Contributors
        fields = ['id', 'user_id', 'project_id']


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'type', 'author_user_id']


class IssueSeriralizer(ModelSerializer):
    class Meta:
        model = Issues
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'
