from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    
class TeamList(APIView):
    def get(self, request, telegram_id, format=None):
        try:
            captain = User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        teams = Team.objects.filter(captain=captain)
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)
    
       
class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    def create(self, request, *args, **kwargs):
        data = request.data
        captain = User.objects.get(telegram_id=data['captain'])
        team = Team.objects.create(name=data['name'],captain=captain)
        serializer = TeamSerializer(team)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def update(self, request, *args, **kwargs):
        team_object = self.get_object()
        data = request.data
        try:
            team_object.name = data.get('name',team_object.name)
            team_object.matches_number = data.get('matches_number',team_object.matches_number)
            team_object.win_number = data.get('win_number',team_object.win_number)
            team_object.fail_number = data.get('fail_number',team_object.fail_number)
            team_object.draw_number = data.get('draw_number',team_object.draw_number)
            team_object.save()
            serializers = TeamSerializer(team_object)
            return Response(serializers.data,status=status.HTTP_206_PARTIAL_CONTENT)
        except Exception as a:
            return Response({'error':str(a)},status=status.HTTP_400_BAD_REQUEST)
    def partial_update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
        
        
        
class MemberViewSet(ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer 
    # def get(self,request,*args,**kwargs):
    #     data = request.data
    #     print(data)
    #     captain = User.objects.get(telegram_id=data['captain'])
    #     member = Member.objects.filter(team=captain.team)
    #     serializer = TeamSerializer(member)
    #     return Response(serializer.data,status=status.HTTP_302_FOUND)
    def retrieve(self, request, *args, **kwargs):
        params = kwargs
        captain = User.objects.get(telegram_id=params['pk'])
        team = captain.team
        member = Member.objects.filter(
           team = team.id
        )
        serializer = MemberSerializer(member,many=True)
        return Response(serializer.data,status=status.HTTP_302_FOUND)
    def create(self, request, *args, **kwargs):
        data = request.data
        captain = User.objects.get(telegram_id=data['captain'])
        member = Member.objects.create(name=data['name'],phone_number=data['phone_number'],number=data['number'],team=captain.team)
        serializer = TeamSerializer(member)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    
class MemberViewbyId(ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer 
    def update(self, request, *args, **kwargs):
        member_object = self.get_object()
        data = request.data
        try:
            member_object.name = data.get('name',member_object.name)
            member_object.phone_number = data.get('phone_number',member_object.phone_number)
            member_object.number = data.get('number',member_object.number)
            member_object.save()
            serializers = MemberSerializer(member_object)
            return Response(serializers.data,status=status.HTTP_206_PARTIAL_CONTENT)
        except Exception as a:
            return Response({'error':str(a)},status=status.HTTP_400_BAD_REQUEST)
        
    def partial_update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
        
    



