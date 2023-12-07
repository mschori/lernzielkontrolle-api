from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


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
