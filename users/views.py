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


class AllTraineesView(ModelViewSet):
    """
    ModelViewSet to provide all User Data needed for trainees.

    :returns: Queryset of users in the student group
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        Get the queryset of users in the student group.

        :returns: Queryset of users in the student group
        """
        student_group_name = get_group_name_student()
        return User.objects.filter(groups__name=student_group_name)


class SingleTraineeView(RetrieveAPIView):
    """
    RetrieveAPIView to provide data for a single user who is a student.

    :returns: Serialized data for the specified user
    """
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        Get the queryset of users in the student group.

        :returns: Queryset of users in the student group
        """
        student_group_name = get_group_name_student()
        return User.objects.filter(groups__name=student_group_name)


class TraineeLearnDataView(APIView):
    """
    API-View to provide learn data for a specific trainee.

    :param trainee_id: int - ID of the trainee
    :returns: Response containing user data and checked learn aims
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, trainee_id, *args, **kwargs):
        """
        Handle GET request to fetch learn data for a specific trainee.

        :param request: The HTTP request object.
        :param trainee_id: The ID of the trainee whose learn data is being retrieved.
        :returns: Response containing serialized user data and checked learn aims.
        """
        user = get_object_or_404(User, pk=trainee_id)
        serializer = UserLearnDataSerializer(user, context={'request': request})

        checked_learn_aims = CheckLearnAim.objects.filter(assigned_trainee=user)
        checked_learn_aims_serializer = CheckLearnAimSerializer(checked_learn_aims, many=True,
                                                                context={'request': request})

        data = {
            'user_data': serializer.data,
            'checked_learn_aims': checked_learn_aims_serializer.data
        }
        return Response(data)
