from rest_framework import serializers
from customer.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create(**validated_data)
        if 'password' in validated_data and validated_data.get('password'):
            user.set_password(validated_data.get('password'))
        user.save()
        return user
