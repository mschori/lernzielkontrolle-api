from django.db.models import Max
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from custom_exceptions.learn_check_exceptions import LearnAimNotInEducationOrdinance, LearnCheckAlreadyApproved, \
    LearnCheckNotYourOwn
from learn_aim_check.models import ActionCompetence, CheckLearnAim, LearnAim
from learn_aim_check.serializers import ActionCompetenceSerializer, CheckLearnAimSerializer, DiagramSerializer, \
    LearnAimSerializer
from services.learn_check_validator import learn_check_validator
from users.permissions import IsStudent
from services.group_service import is_user_coach
from users.models import User


class LearnAimViewSet(viewsets.ModelViewSet):
    """
    View for the learn check.
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Get the serializer class for the view.
        :param self: View object
        :return: ActionCompetenceSerializer or CheckLearnAimSerializer
        """
        if self.request.method == 'GET':
            return ActionCompetenceSerializer
        return CheckLearnAimSerializer

    def get_serializer_context(self):
        """
        Get the context for the serializer.
        :param self: View object
        :return: Context for the serializer
        """
        context = super().get_serializer_context()
        context['student_id'] = self.request.query_params.get('student-id', None)
        return context

    def get_queryset(self) -> CheckLearnAim or ActionCompetence:
        """
        Get all learn aims.
        - only if the user is a student
        - only to the education ordinance of the user
        :param self: View object with the data for the learn aims
        :return: Response with all learn aims
        """
        return_value = None
        if self.request.method == 'GET':
            selected_student_id = self.request.query_params.get('student-id', None)
            print(selected_student_id)
            if is_user_coach(self.request.user) and selected_student_id.isnumeric():
                selected_student = User.objects.filter(id=selected_student_id).first()
                print(selected_student)
                if selected_student:
                    return_value = ActionCompetence.objects.filter(
                        education_ordinance=selected_student.education_ordinance).order_by('identification')
                    print(return_value)
            else:
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
    permission_classes = [IsAuthenticated]

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


class ToggleTodoAPIView(APIView):
    """
    API view to toggle the marked_as_todo field.
    """
    permission_classes = [IsAuthenticated, IsStudent]

    def patch(self, request, pk):
        """
        Toggle the marked_as_todo state of a learn aim.
        :param request: Request object
        :param pk: Primary key of the learn aim
        :return: Response with the updated learn aim
        """
        learn_aim = get_object_or_404(LearnAim, pk=pk)
        current_stage = CheckLearnAim.objects.filter(
            assigned_trainee=request.user,
            closed_learn_check=learn_aim,
            is_approved=True
        ).aggregate(Max('close_stage'))['close_stage__max'] or 0

        if current_stage >= 3:
            learn_aim.marked_as_todo.remove(request.user)
            return Response({"error": "This learn aim is fully completed and cannot be modified."},
                            status=status.HTTP_403_FORBIDDEN)

        if request.user in learn_aim.marked_as_todo.all():
            learn_aim.marked_as_todo.remove(request.user)
        else:
            learn_aim.marked_as_todo.add(request.user)
        return Response(LearnAimSerializer(learn_aim, context={'request': request}).data, status=status.HTTP_200_OK)
