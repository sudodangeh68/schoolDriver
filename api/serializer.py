from django.contrib.auth.models import User
from Base.models import *
from django.http import JsonResponse
from rest_framework import serializers, renderers

from Base.models import UserProfile

RETURN_HTTP_CODE = {
    406: "Not Acceptable",
    401: "Unauthorized",
    404: "Not Found",
    400: "Bad request",
    200: "success",
    201: "created",
    304: "NOT MODIFIED"

}


def Result_Json(return_status, entries, return_message=None, total_page=None):
    if return_message is None:
        return_message = RETURN_HTTP_CODE[return_status]
    if total_page:
        return {"returns": {'code': return_status, 'total_page': total_page, "message": return_message},
                "entriess": entries}
    else:
        return {"returns": {'code': return_status, "message": return_message},
                "entriess": entries}


class GeneralJsonRender(renderers.BaseRenderer):
    media_type = 'application/json'
    format = 'json'
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        return JsonResponse(data, safe=False)


class DriverStudentRequest(serializers.Serializer):
    driver_id = serializers.CharField(max_length=500)


class DriverStudentResponse(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=100)


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    position = PositionSerializer()
    location = DestinationSerializer()

    # TODO: add userprofile ot mode

    """
    askjdaksdaksjdkjasd
    """

    class Meta:
        model = Student
        fields = ['name', 'className', 'position', 'location']

# class UserSerializer1(serializers.Serializer):
#     email = serializers.CharField()
