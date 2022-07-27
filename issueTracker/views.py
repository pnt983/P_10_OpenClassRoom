from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status, generics

from .serializers import ProjectDetailSerializer, SignupUserSerializer, ProjectSerializer, IssueSerializer, \
    CommentSerializer
from .models import Users, Contributors, Projects, Issues, Comments


class SignupUserView(ModelViewSet):
    serializer_class = SignupUserSerializer
    queryset = Users.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # serializer.create_user(first_name=request.data['first_name'],
            #                        last_name=request.data['last_name'],
            #                        email=request.data['email'],
            #                        username=request.data['username'],
            #                        password=request.data['password'])
            serializer.save()
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
            contributor = Contributors.objects.create(user=request.user,
                                                      project=project,
                                                      role='AUTHOR')
            contributor.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        project = get_object_or_404(Projects, pk=kwargs['project'])
        if project:
            serializer = self.serializer_class(project)
            return Response(serializer.data, status=status.HTTP_200_OK)

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


class IssueView(ModelViewSet):
    queryset = Issues.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'issue'

    def list(self, request, *args, **kwargs):
        project = get_object_or_404(Projects, id=kwargs['project_project'])
        # project = Projects.objects.get(id=kwargs['project_project'])
        issues_list = []
        for issue in Issues.objects.all():
            if issue.project == project:
                issues_list.append(issue)
        serializer = self.serializer_class(issues_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        project = get_object_or_404(Projects, id=kwargs['project_project'])
        # project = Projects.objects.get(id=kwargs['project_project'])
        data = {
            'title': request.data['title'],
            'description': request.data['description'],
            'tag': request.data['tag'],
            'priority': request.data['priority'],
            'project': project.id,
            'status': request.data['status'],
            'assignee_user': request.user.id
        }
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

    def update(self, request, *args, **kwargs):
        # kwargs ---> {'project_project': '24', 'issue': '2'}
        issue = get_object_or_404(Issues, id=kwargs['issue'])
        self.check_object_permissions(self.request, issue)
        serializer = self.serializer_class(issue, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        issue = get_object_or_404(Issues, id=kwargs['issue'])
        self.check_object_permissions(self.request, issue)
        self.perform_destroy(issue)
        message = f'Le projet " {issue} " a été correctement supprimé.'
        return Response(message, status=status.HTTP_200_OK)


class CommentView(ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'Comment'

    def list(self, request, *args, **kwargs):
        # kwargs ---> {'project_project': '24', 'issue_issue': '1'}
        issue = get_object_or_404(Issues, id=kwargs['issue_issue'])
        # project = Projects.objects.get(id=kwargs['project_project'])
        comments_list = []
        for comment in Comments.objects.all():
            if comment.project == issue:
                comments_list.append(comment)
        serializer = self.serializer_class(comments_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        issue = get_object_or_404(Issues, id=kwargs['issue_issue'])
        data = {
            'description': request.data['description'],
            'author': request.user.id,
            'issue': issue.id,
        }
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

    def update(self, request, *args, **kwargs):
        # kwargs ---> {'project_project': '24', 'issue_issue': '1', 'Comment': '1'}
        comment = get_object_or_404(Comments, id=kwargs['Comment'])
        self.check_object_permissions(self.request, comment)
        serializer = self.serializer_class(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        comment = get_object_or_404(Comments, id=kwargs['Comment'])
        self.check_object_permissions(self.request, comment)
        self.perform_destroy(comment)
        message = f'Le projet " {comment} " a été correctement supprimé.'
        return Response(message, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        comment = get_object_or_404(Comments, pk=kwargs['Comment'])
        if comment:
            serializer = self.serializer_class(comment)
            return Response(serializer.data, status=status.HTTP_200_OK)


