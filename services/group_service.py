from django.contrib.auth.models import Group

from users.models import User

# Group names
GROUP_NAMES = {
    'COACH': 'COACH',
    'STUDENT': 'STUDENT',
}


def is_user_group_member(user: User, group: Group) -> bool:
    """
    Check if user is a member of the given group.
    :param user: user to check
    :param group: group to check
    :return: True if user is a member of the given group.
    """
    return user.groups.filter(name=group.name).exists()


def is_user_coach(user: User) -> bool:
    """
    Check if user is a coach.
    :param user: user to check
    :return: True if user is a coach.
    """
    return is_user_group_member(user, Group.objects.get(name=GROUP_NAMES['COACH']))


def is_user_student(user: User) -> bool:
    """
    Check if user is student.
    :param user: user to check
    :return: True if user is student.
    """
    return is_user_group_member(user, Group.objects.get(name=GROUP_NAMES['STUDENT']))


def get_group_name_coach():
    """
    Get group name for coach.
    :return: group name for coach.
    """
    return GROUP_NAMES['COACH']


def get_group_name_student():
    """
    Get group name for student.
    :return: group name for student.
    """
    return GROUP_NAMES['STUDENT']
