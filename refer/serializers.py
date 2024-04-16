from django.contrib.auth.models import User
from rest_framework import serializers
from refer.models import Code, Profile



class CodeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Code
        fields = ['email','user']

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    refereal_code = serializers.CharField(allow_null=True,allow_blank=True)

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'],password=validated_data['password'],email=validated_data['email'],)
        user.save()
        profile = Profile.objects.create(user=user)

        c = Code.objects.get(refer_code=validated_data['refereal_code'])
        profile.refer_by = c.user
        profile.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user','refer_by']