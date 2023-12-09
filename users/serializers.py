from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')

    def create(self, validated_data):
        # Hash password for security concerns (it is a bad practice to store passwords in plain text).
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)