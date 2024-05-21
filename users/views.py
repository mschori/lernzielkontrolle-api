from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from learn_aim_check.models import CheckLearnAim
from learn_aim_check.serializers import UserLearnDataSerializer, CheckLearnAimSerializer
from services.group_service import get_group_name_student
from users.models import User
from users.serializers import UserSerializer


class UserView(viewsets.ModelViewSet):
    """
    ModelViewSet to provide all User Data needed.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class CheckUserGroupView(APIView):
    """
    API-View to check if user has a specific group.
    GET-PARAMS:
        group_name: str --> name of the group to check for
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        group_name = self.request.query_params.get('groupName', None)
        if group_name is None:
            return Response({'groupName': 'Please supply a groupName in params.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'has_group': request.user.groups.filter(name=group_name.upper()).exists()},
                        status=status.HTTP_200_OK)


# class TraineeListView(APIView):
#     """
#     API-View to list all users in the 'STUDENT' group.
#     """
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, *args, **kwargs):
#         trainees = User.objects.filter(groups__name='STUDENT')
#         serializer = UserSerializer(trainees, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


class AllTraineesView(ModelViewSet):
    """
    ModelViewSet to provide all User Data needed
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        student_group_name = get_group_name_student()
        return User.objects.filter(groups__name=student_group_name)


class SingleTraineeView(RetrieveAPIView):
    """
    RetrieveAPIView to provide data for a single user who is a student
    """
    serializer_class = UserSerializer

    def get_queryset(self):
        student_group_name = get_group_name_student()
        return User.objects.filter(groups__name=student_group_name)


class TraineeLearnDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, trainee_id, *args, **kwargs):
        # Fetches data for the user specified by trainee_id; removed fallback to request.user
        user = get_object_or_404(User, pk=trainee_id)
        serializer = UserLearnDataSerializer(user, context={'request': request})

        # Fetch checked learn aims
        checked_learn_aims = CheckLearnAim.objects.filter(assigned_trainee=user)
        checked_learn_aims_serializer = CheckLearnAimSerializer(checked_learn_aims, many=True, context={'request': request})

        data = {
            'user_data': serializer.data,
            'checked_learn_aims': checked_learn_aims_serializer.data
        }
        return Response(data)

# class TraineeDetailView(APIView):
#     """
#     API-View to retrieve the details of a specific trainee and their action competences.
#     Only accessible by coaches.
#     """
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request, trainee_id, *args, **kwargs):
#         trainee = User.objects.filter(groups__name='STUDENT').filter(pk=trainee_id).first()
#         if not trainee:
#             return Response({'detail': 'Trainee not found or not a student.'}, status=status.HTTP_404_NOT_FOUND)
#
#         # Assuming ActionCompetence is related to trainee through some field
#         action_competences = ActionCompetence.objects.filter(education_ordinance=trainee.education_ordinance).distinct()
#
#         trainee_serializer = UserSerializer(trainee)
#         action_competences_serializer = ActionCompetenceSerializer(action_competences, many=True)
#
#         return Response({
#             'trainee': trainee_serializer.data,
#             'action_competences': action_competences_serializer.data
#         }, status=status.HTTP_200_OK)
