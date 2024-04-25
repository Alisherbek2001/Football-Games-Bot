from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *
router = DefaultRouter()
router.register('user',UserViewSet)
router.register('team',TeamViewSet)
router.register('member',MemberViewSet)
router.register('memberid',MemberViewbyId)
urlpatterns = [
    path('',include(router.urls)),
    path('team/id/<str:telegram_id>/',TeamList.as_view()),
    # path('member/id/<str:telegram_id/',MemberList.as_view())
]