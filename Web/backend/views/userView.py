from backend.__init__ import serviceInjector as si
from backend.services.userService import UserService

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from knox.auth import TokenAuthentication

from django.http import Http404, HttpResponseBadRequest
from ..serializers import UserInfoSerializer


class User(APIView):
    '''View for getting all users and posting a user to the DB. 
    Should only be accessable by admins'''

    authentication_classes = (TokenAuthentication,)
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

        json_body = request.data
        try:
            barcode_id = json_body['barcodeId']
            nfcId = json_body['nfcId']
            username = json_body['username']
            password = json_body['password']
            cost_centers = json_body['costCenters']
            group = json_body['role']
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        new_user = self.userService.create_user(
            username, password, barcode_id, nfcId, cost_centers, group)

        if new_user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer = UserInfoSerializer(new_user)
        if serializer.is_valid:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'serialization failed'}, status=status.HTTP_400_BAD_REQUEST)


class UserId(APIView):
    '''User'''

    authentication_classes = (TokenAuthentication,)
    @si.inject
    def __init__(self, _deps, *args):
        self.userService: UserService = _deps['UserService']()

    def get(self, request, user_id):
        '''Get.'''
        if request.method == 'GET':
            # A user can see a group if they have permission
            #            if not request.user.has_perm('backend.view_group'):
         #               raise PermissionDenied
            user = self.userService.get_user_info(user_id)
            if user is None:
                raise Http404("Could not find user")
            serializer = UserInfoSerializer(user)
            if serializer.is_valid:
                return Response(serializer.data, status=200)
        return Response({'serialization failed'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user_id):
        '''Edit user'''
        json_body = request.data
        try:
            barcode_id = json_body['barcodeId']
        except:
            barcode_id = None
        try:
            nfc_id = json_body['nfcId']
        except:
            nfc_id = None
        try:
            username = json_body['username']
        except:
            username = None
        try:
            password = json_body['password']
        except:
            password = None
        try:
            cost_center = json_body['costCenters']
        except:
            cost_center = None
        try:
            group = json_body['role']
            print(group)
        except:
            group = None

        updated_user = self.userService.update_user(user_id=user_id, barcode_id=barcode_id, nfc_id=nfc_id, username=username,
                                                    password=password, cost_center=cost_center, group=group)

        serialized_order = UserInfoSerializer(updated_user)
        if serialized_order.is_valid:
            return Response(serialized_order.data, status=200)
        return Response({'serialization failed'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        '''Delete order func'''
        deleted = self.userService.delete_user(user_id=user_id)
        if deleted is None:
            return Response({'User deletion failed'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
