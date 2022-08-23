from rest_framework.permissions import BasePermission
from .models import Projects, Contributors


def get_contributor(user, project):
    return Contributors.objects.filter(user=user).filter(project=project).exists()


class ContributorPermission(BasePermission):

    def has_permission(self, request, view):
        project = Projects.objects.get(id=view.kwargs['project_pk'])
        if request.user == project.author:
            return True

        if view.action in ['list']:
            return get_contributor(request.user, project)

        return False


class ProjectPermission(BasePermission):

    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        elif view.action == 'list':
            if Contributors.objects.filter(user=request.user).exists():
                return True
        else:
            if get_contributor(request.user, project=view.kwargs['pk']):
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'destroy']:
            return obj.author == request.user
        return False


class IssuePermission(BasePermission):

    def has_permission(self, request, view):
        if get_contributor(request.user, project=view.kwargs['project_pk']):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'destroy']:
            return obj.assignee_user == request.user
        return False


class CommentPermission(BasePermission):

    def has_permission(self, request, view):
        if get_contributor(request.user, project=view.kwargs['project_pk']):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'destroy']:
            return obj.author == request.user
        return False


