# https://stackoverflow.com/questions/47008456/django-rest-framework-jwt-custom-payload-with-extend-user/47011439

from coresetup.serializers.serialiser import ContactSerializer

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token':token,
        'user':ContactSerializer(user, context={'request':request}).data
    }