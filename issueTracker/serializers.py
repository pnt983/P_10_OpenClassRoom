from rest_framework.serializers import ModelSerializer

from .models import Users, Contributors, Projects, Issues, Comments


class SignupUserSerializer(ModelSerializer):

    class Meta:
        model = Users
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}}

    def create_user(self, first_name, last_name, email, username, password):
        return Users.objects.create_user(first_name=first_name, last_name=last_name, email=email,
                                         username=username, password=password)


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Projects
        fields = ['title', 'description', 'type', 'author']


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributors
        fields = ['user', 'project', 'role']


class IssueSerializer(ModelSerializer):

    class Meta:
        model = Issues
        fields = ['title', 'description', 'tag', 'priority', 'status', 'created_time',
                  'project', 'assignee_user']


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comments
        fields = ['description', 'created_time', 'author', 'issue']
