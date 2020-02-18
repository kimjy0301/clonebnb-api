from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import RelatedUserSerializer, UserSerializer
from .models import User
from rooms.serializers import RoomSerializer
from rooms.models import Room
from .permissions import IsSelf


import jwt
from django.conf import settings


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [permissions.IsAdminUser]
        elif (
            self.action == "create"
            or self.action == "retrieve"
            or self.action == "favs"
        ):
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsSelf]

        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["POST"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            encoded_jwt = jwt.encode(
                {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
            )
            return Response(
                data={"token": encoded_jwt, "id": user.pk,}, status=status.HTTP_200_OK
            )
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True)
    def favs(self, request, pk):
        user = self.get_object()
        serializer = RoomSerializer(user.favs.all(), many=True)
        return Response(serializer.data)

    @favs.mapping.put
    def toggle_favs(self, request, pk):
        pk = request.data.get("pk", None)
        user = self.get_object()
        if pk is not None:
            try:
                room = Room.objects.get(pk=pk)
                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                serializer = RoomSerializer(user.favs.all(), many=True)
                return Response(serializer.data)
            except Room.DoesNotExist:
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST)


# class UsersView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(request.data)
#         if serializer.is_valid():
#             new_user = serializer.save()
#             return Response(
#                 data=UserSerializer(instance=new_user).data, status=status.HTTP_200_OK
#             )
#         else:
#             return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class MeView(APIView):

#     permission_class = [IsAuthenticated]

#     def get(self, request):
#         return Response(UserSerializer(request.user).data)

#     def put(self, request):
#         serializer = UserSerializer(
#             instance=request.user, data=request.data, partial=True
#         )
#         if serializer.is_valid():
#             user = serializer.save()
#             return Response(
#                 data=UserSerializer(instance=user).data, status=status.HTTP_200_OK
#             )
#         else:
#             return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class FavsView(APIView):

#     permission_class = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         serializer = RoomSerializer(user.favs.all(), many=True)
#         return Response(serializer.data)

#     def put(self, request):
#         pk = request.data.get("pk", None)
#         user = request.user
#         if pk is not None:
#             try:
#                 room = Room.objects.get(pk=pk)
#                 if room in user.favs.all():
#                     user.favs.remove(room)
#                 else:
#                     user.favs.add(room)
#                 serializer = RoomSerializer(user.favs.all(), many=True)
#                 return Response(serializer.data)
#             except Room.DoesNotExist:
#                 pass
#         return Response(status=status.HTTP_400_BAD_REQUEST)


# @api_view(["GET"])
# def user_detail(request, pk):
#     try:
#         user = User.objects.get(pk=pk)
#         return Response(UserSerializer(instance=user).data)
#     except User.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)


# @api_view(["POST"])
# def login(request):
#     username = request.data.get("username")
#     password = request.data.get("password")
#     if not username or not password:
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         encoded_jwt = jwt.encode(
#             {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
#         )
#         return Response(data={"token": encoded_jwt}, status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_401_UNAUTHORIZED)

