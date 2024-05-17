from rest_framework import permissions

from services.group_service import is_user_student, is_user_coach


class IsStudent(permissions.BasePermission):
    """
    Ensure user is in group 'apprentice'.
    """
    message = 'Only apprentices have the permission to do this action.'

    def has_permission(self, request, view):
        return is_user_student(request.user)


class IsCoach(permissions.BasePermission):
    """
    Ensure user is in group 'trainer'.
    """
    message = 'Only trainers have the permission to do this action.'

    def has_permission(self, request, view):
        return is_user_coach(request.user)

    # class IsCoach(permissions.BasePermission):
    ##   def has_permission(self, request, view):
    #     # Implement your logic to determine if the user is a coach
    #    return request.user.is_authenticated and request.user.is_coach
