from backend.__init__ import serviceInjector as si
from backend.services.userService import UserService
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, HttpResponseBadRequest
from ..serializers import UserInfoSerializer
from rest_framework.response import Response
from rest_framework import status


class User(APIView):
    '''View for getting all users and posting a user to the DB. 
    Should only be accessable by admins'''

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
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        '''posts a user to the database. Should Only accessable by Admins'''
        pass


class UserId(APIView):
    '''User'''
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
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        except:
            group = None

 #       user = self.userService.get_user_info(user_id)
  #      if user is None:
   #         raise Http404("Could not find user")
        updated_user = self.userService.update_user(user_id=user_id,barcode_id=barcode_id,nfc_id=nfc_id, username=username, 
        password=password, cost_center=cost_center, group=group  )
        print(updated_user)
        serialized_order = UserInfoSerializer(updated_user)
        if serialized_order.is_valid:
            return Response(serialized_order.data, status=200)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)





    def delete(self, request, user_id):
        '''Delete order func'''
        deleted = self.userService.delete_user(user_id=user_id)
        if deleted is None:
            return HttpResponseBadRequest
        return Response(status=status.HTTP_204_NO_CONTENT)
