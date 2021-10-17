from rest_framework import serializers
from backend.models import Member


class MemberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ( "id", "avatar", "gender", "name", "surname", "email", "password")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Member(**validated_data)
        user.set_password(password)
        user.save()
        return user


