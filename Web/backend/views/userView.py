from backend.__init__ import serviceInjector as si
from backend.services.userService import UserService
from rest_framework.views import APIView
from django.http import Http404, JsonResponse, HttpResponseBadRequest
from ..serializers import UserInfoSerializer


class User(APIView):
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
                return JsonResponse(serializer.data, safe=False, status=200)
        return HttpResponseBadRequest
