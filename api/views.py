from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializer import UserSerializer, DriverStudentRequest, DriverStudentResponse, GeneralJsonRender, Result_Json


# Create your views here.


def serializer(args):
    pass


class DriverStudent(APIView):
    """
    List all snippets, or create a new snippet.
    """
    renderer_classes = (GeneralJsonRender,)

    def post(self, request, format=None):
        print("REQ: %s" % request)
        data = JSONParser().parse(request)
        temp = DriverStudentRequest(data=data)
        if temp.is_valid():
            users_list = []
            try:
                for item in User.objects.filter():
                    users_list.append(
                        {"username": item.username, "first_name": item.first_name, "last_name": item.last_name})
            except:
                result = Result_Json(return_status=status.HTTP_400_BAD_REQUEST, entries="درخواست ارسالی معتبر نمیباشد")
            else:
                result = Result_Json(return_status=status.HTTP_200_OK, entries=users_list)
            # ------------------------------------------------------------
        else:
            result = Result_Json(return_status=status.HTTP_406_NOT_ACCEPTABLE, entries={"errors": temp.errors})

            # ------------------------------------------------------------
        return Response(result)


class UserList(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        snippets = User.objects.filter()
        serializer = UserSerializer(snippets, many=True)
        return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = SnippetSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCreate(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        snippets = User.objects.create()
        serializer = UserSerializer(snippets, many=True)
        return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = SnippetSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
