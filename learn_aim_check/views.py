from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from custom_exceptions.learn_check_exceptions import LearnAimNotInEducationOrdinance, \
    LearnCheckAlreadyApproved, LearnCheckNotYourOwn
from learn_aim_check.models import ActionCompetence, CheckLearnAim
from learn_aim_check.serializers import ActionCompetenceSerializer, CheckLearnAimSerializer
from services.learn_check_validator import learn_check_validator
from users.permissions import IsStudent


class LearnCheckView(APIView):
    """
    View for the learn check.
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request, *args, **kwargs) -> Response:
        """
        Get all action competences.
        - only if the user is a student
        - only to the education ordinance of the user
        return: Response with all action competences and learn aims
        """
        action_competence = ActionCompetence.objects.filter(education_ordinance=self.request.user.education_ordinance)
        serializer = ActionCompetenceSerializer(action_competence, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs) -> Response:
        """
        Create a new learning check.
        - only if the learn aim is part of the user's education ordinance
        - only if the learn aim is not already checked
        - only if the semester is not lower than the previous semester
        return: Response with the new learn check
        """
        serializer = CheckLearnAimSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        learn_aim = serializer.validated_data['closed_learn_check']
        if request.user.education_ordinance not in learn_aim.action_competence.education_ordinance.all():
            raise LearnAimNotInEducationOrdinance

        learn_check_validator(request.user, serializer)

        serializer.save(assigned_trainee=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, pk) -> Response:
        """
        Update a learning check.
        - only the assigned trainee can update the learn check
        - only if the learn check is not approved
        return: Response with the updated learn check
        """
        learn_aim_check = get_object_or_404(CheckLearnAim, pk=pk)

        if learn_aim_check.is_approved:
            raise LearnCheckAlreadyApproved
        if learn_aim_check.assigned_trainee != request.user:
            raise LearnCheckNotYourOwn

        serializer = CheckLearnAimSerializer(learn_aim_check, data=request.data)
        if serializer.is_valid():
            learn_check_validator(request.user, serializer, is_create=False)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
