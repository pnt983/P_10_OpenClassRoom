from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .serializers import UserSerializer, ContributorsSerializer, \
                         ProjectSerializer, IssueSeriralizer, CommentSerializer
from .models import Users, Contributors, Projects, Issues, Comments


# class UserAPIView(APIView):
#
#     def get(self, *args, **kwargs):
#         users = Users.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)


class UserViewset(ModelViewSet):

    serializer_class = UserSerializer

    def get_queryset(self):
        return Users.objects.all()


class ContributorViewset(ModelViewSet):

    serializer_class = ContributorsSerializer

    def get_queryset(self):
        return Contributors.objects.all()


class ProjectViewset(ModelViewSet):

    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Projects.objects.all()


class IssueViewset(ModelViewSet):

    serializer_class = IssueSeriralizer

    def get_queryset(self):
        return Issues.objects.all()


class CommentViewset(ModelViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comments.objects.all()

