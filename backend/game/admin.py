from django.contrib import admin
from .models import User,Team, Member

class UserAdmin(admin.ModelAdmin):
    list_display = ['fullname','telegram_id','phone','created_at']
    list_filter = ['fullname']
    list_per_page = 10
    list_editable = ['phone']
admin.site.register(User,UserAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ['name','captain','matches_number','win_number','fail_number','draw_number']
    list_filter = ['name']
    list_per_page = 10
    list_editable = ['matches_number','win_number','fail_number','draw_number']
admin.site.register(Team,TeamAdmin)


class MemberAdmin(admin.ModelAdmin):
    list_display = ['name','phone_number','number','team']
    list_filter = ['name','team']
    list_per_page = 10
    list_editable = ['number']
admin.site.register(Member,MemberAdmin)