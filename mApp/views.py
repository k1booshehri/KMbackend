from rest_framework.response import Response
from rest_framework import status, generics

from mApp.models import User
from mApp.serializers import UserSerializer, UpdateUserSerializer


class UserProfile(generics.GenericAPIView):
    def get(self, request, **kwargs):
        try:
            user = User.objects.get(id=kwargs.get('id'))

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        ser = UserSerializer(user)

        return Response(ser.data, status=status.HTTP_200_OK)

    def put(self, request, **kwargs):
        try:
            user = User.objects.get(id=kwargs.get('id'))
            request.data.update({'id': kwargs.get('id')})
            request.data.update({'username': user.username})
            ser = UpdateUserSerializer(user, data=request.data)
            if ser.is_valid():
                ser.update(instance=user, validated_data=request.data)
                return Response(ser.data, status=status.HTTP_200_OK)

            else:
                return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, **kwargs):
        try:
            User.objects.get(id=kwargs.get('id')).delete()
            return Response(status=status.HTTP_200_OK)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
