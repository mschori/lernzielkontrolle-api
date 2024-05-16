from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from learn_aim_check.models import ActionCompetence
from learn_aim_check.serializers import ActionCompetenceSerializer
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
        return Response({'has_group': request.user.groups.filter(name=group_name.upper()).exists()}, status=status.HTTP_200_OK)


class TraineeListView(APIView):
    """
    API-View to list all users in the 'STUDENT' group.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        trainees = User.objects.filter(groups__name='STUDENT')
        serializer = UserSerializer(trainees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TraineeDetailView(APIView):
    """
    API-View to retrieve the details of a specific trainee and their action competences.
    Only accessible by coaches.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, trainee_id, *args, **kwargs):
        trainee = User.objects.filter(groups__name='STUDENT').filter(pk=trainee_id).first()
        if not trainee:
            return Response({'detail': 'Trainee not found or not a student.'}, status=status.HTTP_404_NOT_FOUND)

        # Assuming ActionCompetence is related to trainee through some field
        action_competences = ActionCompetence.objects.filter(education_ordinance=trainee.education_ordinance).distinct()

        trainee_serializer = UserSerializer(trainee)
        action_competences_serializer = ActionCompetenceSerializer(action_competences, many=True)

        return Response({
            'trainee': trainee_serializer.data,
            'action_competences': action_competences_serializer.data
        }, status=status.HTTP_200_OK)