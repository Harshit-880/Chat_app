from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Contact, OnlineStatus

class UserSerializer(serializers.ModelSerializer):
    is_online = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'is_online')

    def get_is_online(self, obj):
        return obj.onlinestatus.is_online

    def create(self, validated_data):
        # Create the user and set the password
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
    
class ContactSerializer(serializers.ModelSerializer):
    other_party = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ('id', 'other_party', 'accepted')

    def get_other_party(self, obj):
        request_user = self.context['request'].user
        other_party = obj.get_other_party(request_user)
        return UserSerializer(other_party).data