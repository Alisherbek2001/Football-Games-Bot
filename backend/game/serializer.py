from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import User,Team, Member

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class TeamSerializer(ModelSerializer):
    captain = UserSerializer(read_only=True)
    class Meta:
        model = Team
        fields = '__all__'
        

class MemberSerializer(ModelSerializer):
    team = TeamSerializer(read_only=True)
    class Meta:
        model = Member
        fields = '__all__'