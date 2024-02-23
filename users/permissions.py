from rest_framework import permissions

from services.group_service import is_user_student


class IsStudent(permissions.BasePermission):
    """
    Ensure user is in group 'apprentice'.
    """
    message = 'Only apprentices have the permission to do this action.'

    def has_permission(self, request, view):
        return is_user_student(request.user)
