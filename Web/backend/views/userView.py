from backend.__init__ import serviceInjector as si
from backend.services.userService import UserService
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404, HttpResponseBadRequest
from ..serializers import UserInfoSerializer


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
            print(user)
            if user is None:
                raise Http404("Could not find user")
            serializer = UserInfoSerializer(user)
            if serializer.is_valid:
                return Response(serializer.data, safe=False, status=200)
        return HttpResponseBadRequest
