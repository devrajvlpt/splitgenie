from social_auth.backends.google import GOOGLEAPIS_PROFILE, googleapis_profile
from rest_framework import status, mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from social_auth.backends import get_backend
from .serializers import UserRegisterSerializer
class SocialSignUp(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    “””
    Social Authentication API.
    “””
    permission_classes = (AllowAny,)
    throttle_classes = (AnonRateThrottle, )
    def create(self, request, *args, **kwargs):
        “””
        Create user using information from social channels like, facebook and google.
        — 
        parameters:
        – name: provider
        description: provider can be facebook or google-oauth2
        required: true
        type: string
        paramType: form
        – name: access_token
        description: Access Token which we will use to fetch the user’s detail.
        required: true
        type: string
        paramType: form
        parameters_strategy: replace
        “””
        redirect = request.path
        try:
            provider = request.DATA[‘provider’]
            access_token = request.DATA[‘access_token’]
        except KeyError:
            return Response({‘success’: False, 
            ‘detail’: “‘provider’ and ‘access_token’ are required parameters”},
            status=status.HTTP_400_BAD_REQUEST)
        backend = get_backend(provider, request, redirect)
        request.social_auth_backend = backend
        if access_token:
        try:
            if provider == “google-oauth2”:
                test_response = googleapis_profile(GOOGLEAPIS_PROFILE, access_token)
            if test_response is None:
                return Response({‘success’: False, ‘detail’: “bad access_token”}, status=status.HTTP_400_BAD_REQUEST)
            user = backend.do_auth(access_token, expires=None, *args, **kwargs)
            my_user = User.objects.get(user=user)
            user_serializer = UserRegisterSerializer(my_user)
            return Response({‘success’: True, ‘detail’: user_serializer.data})
            except Exception as e:
            return Response({‘success’: False, ‘detail’: e},
        status=status.HTTP_400_BAD_REQUEST)