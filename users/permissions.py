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

    This permission class checks if the user is a coach by verifying if the user
    is in the 'trainer' group.

    :param request: The HTTP request object.
    :param view: The view for which the permission is being checked.
    :returns: Boolean indicating if the user has permission to perform the action.
    :raises: PermissionDenied if the user is not a trainer.
    """
    message = 'Only trainers have the permission to do this action.'

    def has_permission(self, request, view):
        """
        Check if the user is a coach.

        :param request: The HTTP request object.
        :param view: The view for which the permission is being checked.
        :returns: Boolean indicating if the user has permission to perform the action.
        """
        return is_user_coach(request.user)
