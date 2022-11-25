from backend.__init__ import serviceInjector as si
from backend.services.userService import UserService
from ..serializers import UserInfoSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from django.core.exceptions import PermissionDenied
from django.http import Http404


class User(APIView):
    '''View for getting all users and posting a user to the DB. 
    Should only be accessable by admins'''

    permission_classes = [IsAdminUser]

    @si.inject
    def __init__(self, _deps, *args):
        self.userService: UserService = _deps['UserService']()

    def get(self, request):
        '''Get all users from the database. Should Only accessable by admins'''

        users = self.userService.get_users()
        if users is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = UserInfoSerializer(users, many=True)
        if serializer.is_valid:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'serialization failed'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        '''posts a user to the database. Should Only accessable by Admins'''

        barcode_id = request.data.get('barcodeId', None)
        nfc_id = request.data.get('nfcId', None)
        username = request.data.get('username')
        password = request.data.get('password')
        cost_center = request.data.get('costCenters')
        group = request.data.get('role')

        new_user = self.userService.create_user(
            username, password, barcode_id, nfc_id, cost_center, group)

        if new_user is None:
            return Response('user could not be created', status=status.HTTP_400_BAD_REQUEST)

        serializer = UserInfoSerializer(new_user)
        if serializer.is_valid:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'serialization failed'}, status=status.HTTP_400_BAD_REQUEST)


class UserId(APIView):
    '''User view. Can only be accessed by admins'''

    permission_classes = [IsAdminUser]

    @si.inject
    def __init__(self, _deps, *args):
        self.userService: UserService = _deps['UserService']()

    def get(self, request, user_id):
        '''Get.'''
        if request.method == 'GET':
            if not request.user.has_perm('backend.view_group'):
                raise PermissionDenied

            user = self.userService.get_user_info(user_id)
            if user is None:
                raise Http404("Could not find user")
            serializer = UserInfoSerializer(user)
            if serializer.is_valid:
                return Response(serializer.data, status=200)
        return Response({'serialization failed'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user_id):
        '''Edit user'''
        user = self.userService.get_user_info(user_id)
        if user is None:
            return Response({'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        barcode_id = request.data.get('barcodeId', user.barcode_id)
        nfc_id = request.data.get('nfcId', user.nfc_id)
        username = request.data.get('username', user.user.username)
        password = request.data.get('password', user.user.password)
        cost_center = request.data.get('costCenters', user.cost_center)
        cost_center = request.data.get('costCenters', user.cost_center)
        group = request.data.get('role', user.group)

        updated_user = self.userService.update_user(user_id=user_id, barcode_id=barcode_id, nfc_id=nfc_id, username=username,
                                                    password=password, cost_center=cost_center, group=group)

        if updated_user is None:
            return Response({'user could not be updated'}, status=status.HTTP_400_BAD_REQUEST)

        serialized_order = UserInfoSerializer(updated_user)
        if serialized_order.is_valid:
            return Response(serialized_order.data, status=200)
        return Response({'serialization failed'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        '''Delete order func'''
        user = self.userService.get_user_info(user_id)
        if user is None:
            return Response({'Deletion failed. User does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        deleted = self.userService.delete_user(user_id=user_id)
        if deleted is None:
            return Response({'User deletion failed'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
