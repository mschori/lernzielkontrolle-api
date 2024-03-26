from custom_exceptions.learn_check_exceptions import LearnAimAlreadyChecked, \
    LearnAimStageCantStartHigherThenOne, \
    LearnCheckNotApproved, \
    SemesterCantBeLowerThenPrevious
from learn_aim_check.models import CheckLearnAim
from learn_aim_check.serializers import CheckLearnAimSerializer
from users.models import User


def learn_check_validator(user: User, serializer: CheckLearnAimSerializer, is_create=True) -> None:
    """
    Function to validate the learn check.
    :param user: User object
    :param serializer: CheckLearnAimSerializer Post or Patch data
    :param is_create: bool if the request is a create or update
    :return: None
    :raises LearnAimAlreadyChecked: if the learn aim is already checked
    :raises LearnAimStageCantStartHigherThenOne: if the learn aim stage is higher than 1
    :raises LearnCheckNotApproved: if the previous learn check is not approved
    :raises SemesterCantBeLowerThenPrevious: if the semester is lower than the current semester on Learn Check request
    :raises LearnAimAlreadyChecked: if the learn aim is already checked (only on create)
    """
    previous_checks = CheckLearnAim.objects.filter(
        assigned_trainee=user,
        closed_learn_check=serializer.validated_data['closed_learn_check']
    )

    if len(previous_checks) == 0 and serializer.validated_data['close_stage'] > 1:
        raise LearnAimStageCantStartHigherThenOne

    for check in previous_checks:
        if is_create:
            if (check.close_stage < serializer.validated_data['close_stage']
                    and not check.is_approved):
                raise LearnCheckNotApproved
            if check.close_stage == serializer.validated_data['close_stage']:
                raise LearnAimAlreadyChecked
            if serializer.validated_data['semester'] < check.semester:
                raise SemesterCantBeLowerThenPrevious
        elif not is_create and check.id != serializer.instance.id:
            if serializer.validated_data['semester'] < check.semester:
                raise SemesterCantBeLowerThenPrevious
