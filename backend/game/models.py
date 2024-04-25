from django.db import models


class User(models.Model):
    fullname = models.CharField(max_length=255,null=True,blank=True)
    telegram_id = models.CharField(max_length=30,unique=True)
    phone = models.CharField(max_length=30,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname
    

class Team(models.Model):
    name = models.CharField(max_length=255,unique=True)
    captain = models.OneToOneField(User,on_delete=models.CASCADE)
    matches_number = models.CharField(max_length=10,null=True,blank=True)
    win_number = models.CharField(max_length=25,null=True,blank=True)
    fail_number = models.CharField(max_length=25,null=True,blank=True)
    draw_number = models.CharField(max_length=25,null=True,blank=True)
    
    def __str__(self) -> str:
        return self.name
    

    
class Member(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255,null=True,blank=True)
    number = models.CharField(max_length=20,null=True,blank=True)
    team  = models.ForeignKey(Team,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
     