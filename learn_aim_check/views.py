from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from custom_exceptions.learn_check_exceptions import LearnAimAlreadyChecked, LearnAimNotInEducationOrdinance, \
    LearnAimStageCantStartHigherThenOne, LearnCheckNotApproved, \
    SemesterCantBeLowerOnNewRequest
from learn_aim_check.models import ActionCompetence, CheckLearnAim
from learn_aim_check.serializers import ActionCompetenceSerializer, CheckLearnAimSerializer


class LearnCheckView(APIView):
    """
    View for the learn check.
    """

    def get(self, request, *args, **kwargs):
        """
        Get all action competences.
        """
        action_competence = ActionCompetence.objects.filter(education_ordinance=self.request.user.education_ordinance)
        serializer = ActionCompetenceSerializer(action_competence, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create a new learning check.
        """
        serializer = CheckLearnAimSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        learn_aim = serializer.validated_data['closed_learn_check']
        if request.user.education_ordinance not in learn_aim.action_competence.education_ordinance.all():
            raise LearnAimNotInEducationOrdinance

        previous_checks = CheckLearnAim.objects.filter(
            assigned_trainee=request.user, closed_learn_check=learn_aim)
        if len(previous_checks) == 0 and serializer.validated_data['close_stage'] > 1:
            raise LearnAimStageCantStartHigherThenOne

        for check in previous_checks:
            if check.close_stage < serializer.validated_data['close_stage'] and not check.is_approved:
                raise LearnCheckNotApproved
            if serializer.validated_data['semester'] < check.semester:
                raise SemesterCantBeLowerOnNewRequest
            if check.close_stage == serializer.validated_data['close_stage']:
                raise LearnAimAlreadyChecked

        serializer.save(assigned_trainee=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
