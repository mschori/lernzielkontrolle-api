from rest_framework import status
from rest_framework.exceptions import APIException


class LearnCheckNotApproved(APIException):
    """
    Exception if the previous learn check is not approved and the user tries to create a new learn check.
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "The previous learn check is not approved. Please wait for the approval."
    default_code = "learn_check_not_approved"


class SemesterCantBeLowerThenPrevious(APIException):
    """
    Exception if the semester is lower than the current semester on Learn Check request.
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Semester can't be lower than the previous checked learn aim. Please check the semester."
    default_code = "semester_cant_be_lower"


class LearnAimAlreadyChecked(APIException):
    """
    Exception if the learn aim is already checked.
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "The learn aim is already checked."
    default_code = "learn_aim_already_checked"


class LearnAimNotInEducationOrdinance(APIException):
    """
    Exception if the learn aim is not part of the user's education ordinance.
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "The learn aim is not part of your education ordinance."
    default_code = "learn_aim_not_in_education_ordinance"


class LearnAimStageCantStartHigherThenOne(APIException):
    """
    Exception if the learn aim stage is higher than 1.
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "The learn aim stage can't start higher than 1."
    default_code = "learn_aim_stage_cant_start_higher_than_one"


class LearnCheckNotYourOwn(APIException):
    """
    Exception if the learn check is not the user's own.
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "The learn check is not your own."
    default_code = "learn_check_not_your_own"


class LearnCheckAlreadyApproved(APIException):
    """
    Exception if the learn check is already approved.
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "The learn check is already approved. You can not change it."
    default_code = "learn_check_already_approved"


class CloseStageUpdateNotAllowed(APIException):
    """
    Exception: The close stage can not be updated
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "The close stage can not be updated."
    default_code = "close_stage_update_not_allowed"
