from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from custom_exceptions.firebase_exceptions import FirebaseUserNotFoundException, FirebaseTokenNotFoundException
from custom_exceptions.user_exceptions import EmailAlreadyExistsException
from services import firebase_service, user_service, token_service
from .serializers import UserLoginSerializer


class LoginView(APIView):
    """
    API-View to log user in.
    """

    serializer_class = UserLoginSerializer

    def post(self, request):
        try:
            token = request.data.get('firebaseIdToken', None)
            user_record = firebase_service.get_user_infos_with_id_token(token)
            user = user_service.get_or_create_user(user_record)
            tokens = token_service.get_tokens_for_user(user)
            data = {
                'id': user.id,
                'email': user.email,
                'firstname': user.firstname,
                'lastname': user.lastname,
                'groups': user.get_groups().values(),
                'tokens': tokens
            }
            return Response(self.serializer_class(data).data, status=status.HTTP_200_OK)
        except FirebaseTokenNotFoundException:
            return Response({'error': 'Please supply a valid firebase id-token.'}, status=status.HTTP_400_BAD_REQUEST)
        except FirebaseUserNotFoundException:
            return Response({'error': 'Firebase-User not found.'}, status=status.HTTP_400_BAD_REQUEST)
        except EmailAlreadyExistsException:
            return Response({'error': 'Email already exists. UID does not match.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)


class LogoutView(APIView):
    """
    API-View to log user out.
    """

    permission_classes = [IsAuthenticated]
    success_message = 'Successfully logged out!'

    def delete(self, request):
        firebase_service.revoke_refresh_token(request.user)
        return Response({self.success_message}, status=status.HTTP_200_OK)
