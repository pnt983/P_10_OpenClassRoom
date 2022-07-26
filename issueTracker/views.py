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
        user = Users.objects.get(username=request.user.username)
        query = Projects.objects.filter(author=user)
        serializer = self.serializer_class(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        # project = Projects.objects.create(title=request.data['title'],
        #                                   description=request.data['description'],
        #                                   type=request.data['type'],
        #                                   author=request.user)

        data = {
            'title': request.data['title'],
            'description': request.data['description'],
            'type': request.data['type'],
            'author': request.user
        }
        serializer = self.serializer_detail_class(data=data)
        if serializer.is_valid():
            project = serializer.save()
            contributor = Contributors.objects.create(user_id=request.user,
                                                      project_id=project,
                                                      role='AUTHOR')
            contributor.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(ModelViewSet):
    serializer_class = ProjectDetailSerializer
    queryset = Projects.objects.all()
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        print('type : ', type(request.user.id), request.user.id)
        project = Projects.objects.get(id=kwargs['pk'])
        print('mon print', project)
        if project:
            test = self.serializer_class(project)
            return Response(test.data, status=status.HTTP_200_OK)

