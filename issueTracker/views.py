from django.shortcuts import render
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status, generics

from .serializers import ProjectDetailSerializer, SignupUserSerializer, ProjectSerializer
from .models import Users, Contributors, Projects, Issues, Comments


class SignupUserView(ModelViewSet):
    serializer_class = SignupUserSerializer
    queryset = Users.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.create_user(first_name=request.data['first_name'],
                                   last_name=request.data['last_name'],
                                   email=request.data['email'],
                                   username=request.data['username'],
                                   password=request.data['password'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectListView(ModelViewSet):
    serializer_class = ProjectSerializer
    serializer_detail_class = ProjectDetailSerializer
    queryset = Projects.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = Users.objects.get(username=request.user)
        # user_data = SignupUserSerializer(user).data
        query = Projects.objects.filter(author_user_id=user)
        serializer = self.serializer_class(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_detail_class(data=request.data)
        user = Users.objects.get(username=request.user)
        user_data = SignupUserSerializer(user).data
        if serializer.is_valid():
            # user_id = self.serializer_detail_class.get_author_user_id(request.user)
            project = serializer.save(auth_user_id=user_data)
            contributor = Contributors.objects.create(user_id=user,
                                                      project_id=project,
                                                      role='AUTHOR')
            contributor.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

