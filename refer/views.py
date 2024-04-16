import uuid

from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from .permissions import IsOwnerOrReadOnly
from .tasks import delete_code
from refer.models import Code, Profile
from refer.serializers import CodeSerializer, RegisterSerializer, ProfileSerializer


def random_code():
    return uuid.uuid4()


class CreateCode(APIView,CreateModelMixin):
    serializer_class = CodeSerializer
    queryset = Code.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        lst = Code.objects.filter(user_id=self.request.user.id).values()
        return Response({'codes':list(lst)})

    def post(self, request, *args, **kwargs):
        new = Code(refer_code=random_code(),user_id=self.request.user.id)
        new.save()
        delete_code.delay(new.id)
        lst = Code.objects.filter(user_id=self.request.user.id).values()
        return Response({'codes':list(lst)})
class ReferalsApiView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        lst = Profile.objects.filter(refer_by_id=self.request.user.id)
        a = {'referals':[{
            'username':i.user.username,
            'email':i.user.email,
            'date_joined': i.user.date_joined,
            'first_name': i.user.first_name,
            'last_name': i.user.last_name,
            'last_login': i.user.last_login,
        } for i in lst ]}
        return Response(a)


class CodeDelete(generics.DestroyAPIView):
    serializer_class = CodeSerializer
    queryset = Code.objects.all()
    permission_classes = [IsOwnerOrReadOnly,]

class RegisterApiView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny,]
