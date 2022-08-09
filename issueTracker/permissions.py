from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Projects, Contributors


class ContributorPermission(BasePermission):

    def has_permission(self, request, view):
        project = Projects.objects.get(id=view.kwargs['project_pk'])
        if project in Projects.objects.filter(author=request.user):
            if request.method in SAFE_METHODS:
                return True
            return request.user == project.author
        return False


class ProjectPermission(BasePermission):

    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        elif view.action == 'list':
            if Contributors.objects.filter(user=request.user).exists():
                return True
        else:
            if Contributors.objects.filter(user=request.user).filter(project=view.kwargs['pk']).exists():
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'destroy']:
            return obj.author == request.user
        return False


class IssuePermission(BasePermission):

    def has_permission(self, request, view):
        if Contributors.objects.filter(user=request.user).filter(project=view.kwargs['project_pk']).exists():
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'destroy']:
            return obj.assignee_user == request.user
        return False


class CommentPermission(BasePermission):

    def has_permission(self, request, view):
        if Contributors.objects.filter(user=request.user).filter(project=view.kwargs['project_pk']).exists():
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'destroy']:
            return obj.author == request.user
        return False


