from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from learn_aim_check.models import ActionCompetence
from learn_aim_check.serializers import ActionCompetenceSerializer


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
