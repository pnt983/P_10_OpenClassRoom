from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
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
    queryset = Projects.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "project"

    def list(self, request, *args, **kwargs):
        queryset = Projects.objects.filter(author=request.user.id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = {
            'title': request.data['title'],
            'description': request.data['description'],
            'type': request.data['type'],
            'author': request.user.id
        }
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            project = serializer.save()
            contributor = Contributors.objects.create(user_id=request.user,
                                                      project_id=project,
                                                      role='AUTHOR')
            contributor.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        try:
            project = Projects.objects.get(pk=kwargs['project'])
            if project:
                serializer = self.serializer_class(project)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        obj = get_object_or_404(Projects, id=kwargs['project'])
        self.check_object_permissions(self.request, obj)
        project = Projects.objects.get(id=kwargs['project'])
        serializer = self.serializer_class(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        project = get_object_or_404(Projects, id=kwargs['project'])
        self.check_object_permissions(self.request, project)
        self.perform_destroy(project)
        message = f'Le projet " {project} " a été correctement supprimé.'
        return Response(message, status=status.HTTP_200_OK)






# class ProjectDetailView(ModelViewSet):
#     serializer_class = ProjectDetailSerializer
#     queryset = Projects.objects.all()
#     permission_classes = [IsAuthenticated]
#     lookup_field = "project"
#
#     def retrieve(self, request, *args, **kwargs):
#         print('type : ', type(request.user.id), request.user.id)
#         project = Projects.objects.get(id=kwargs['pk'])
#         print('mon print', project)
#         if project:
#             test = self.serializer_class(project)
#             return Response(test.data, status=status.HTTP_200_OK)

