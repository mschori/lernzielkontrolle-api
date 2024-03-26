from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from custom_exceptions.learn_check_exceptions import LearnAimNotInEducationOrdinance, LearnCheckAlreadyApproved, \
    LearnCheckNotYourOwn
from learn_aim_check.models import ActionCompetence, CheckLearnAim
from learn_aim_check.serializers import ActionCompetenceSerializer, CheckLearnAimSerializer, DiagramSerializer
from services.learn_check_validator import learn_check_validator
from users.permissions import IsStudent


class LearnAimViewSet(viewsets.ModelViewSet):
    """
    View for the learn check.
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def get_serializer_class(self):
        """
        Get the serializer class for the view.
        :param self: View object
        :return: ActionCompetenceSerializer or CheckLearnAimSerializer
        """
        if self.request.method == 'GET':
            return ActionCompetenceSerializer
        return CheckLearnAimSerializer

    def get_queryset(self) -> CheckLearnAim or ActionCompetence:
        """
        Get all learn aims.
        - only if the user is a student
        - only to the education ordinance of the user
        :param self: View object with the data for the learn aims
        :return: Response with all learn aims
        """
        if self.request.method == 'GET':
            return_value = ActionCompetence.objects.filter(
                education_ordinance=self.request.user.education_ordinance).order_by('identification')
        else:
            return_value = CheckLearnAim.objects.filter(assigned_trainee=self.request.user)
        return return_value

    def create(self, request, *args, **kwargs) -> Response:
        """
        Create a new learning check.
        - only if the learn aim is part of the user's education ordinance
        - only if the learn aim is not already checked
        - only if the semester is not lower than the previous semester
        :param self: View object with the data for the new learn check
        :param request: Request with the data for the new learn check
        :raises LearnAimNotInEducationOrdinance: if the learn aim is not part of the user's education ordinance
        :return: Response with the new learn check
        """
        serializer = CheckLearnAimSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        learn_aim = serializer.validated_data['closed_learn_check']
        if request.user.education_ordinance not in learn_aim.action_competence.education_ordinance.all():
            raise LearnAimNotInEducationOrdinance

        learn_check_validator(request.user, serializer)

        serializer.save(assigned_trainee=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs) -> Response:
        """
        Update a learning check.
        - only the assigned trainee can update the learn check
        - only if the learn check is not approved
        :param self: View object with the data for the updated learn check
        :param request: Request with the data for the updated learn check
        :raises LearnCheckAlreadyApproved: if the learn check is already approved
        :raises LearnCheckNotYourOwn: if the learn check is not your own
        :return: Response with the updated learn check
        """
        learn_aim_check = get_object_or_404(CheckLearnAim, pk=kwargs['pk'])

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

    def destroy(self, request, *args, **kwargs) -> Response:
        """
        Delete a learning check.
        - only the assigned trainee can delete the learn check
        - only if the learn check is not approved
        :param self: View object with the data for the destroyed learn check
        :param request: Request with the data for the updated learn check
        :raises LearnCheckAlreadyApproved: if the learn check is already approved
        :raises LearnCheckNotYourOwn: if the learn check is not your own
        :return: Response with the success message
        """
        learn_aim_check = get_object_or_404(CheckLearnAim, pk=kwargs['pk'])

        if learn_aim_check.is_approved:
            raise LearnCheckAlreadyApproved
        if learn_aim_check.assigned_trainee != request.user:
            raise LearnCheckNotYourOwn
        learn_aim_check.delete()
        return Response({"Success": "Learn check successfully deleted"}, status=status.HTTP_204_NO_CONTENT)


class LearnCheckChartAPIView(APIView):
    """
    View for the diagram of the learn check.
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request, pk) -> Response:
        """
        Get the diagram for the learn check.
        - only if the learn aim is part of the user's education ordinance
        :param self: View object with the data for the diagram
        :param request: Request with the data for the diagram (User)
        :param pk: Primary key of the learn aim
        :raises LearnAimNotInEducationOrdinance: if the learn aim is not part of the user's education ordinance
        :return: Response for the chart
        """
        action_competence = get_object_or_404(ActionCompetence, id=pk)
        if request.user.education_ordinance not in action_competence.education_ordinance.all():
            raise LearnAimNotInEducationOrdinance

        serializer = DiagramSerializer(action_competence, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
