from django.urls import path
from .views import (
    Home,
    RegisterHostelView,
    HostelEmailTokenObtainPairView,
    HostelLoginView,
    HostelLogoutView,
    RegisterStudentWithHostelView,
    StudentLoginView,
    ViewLeaves,
    StudentEmailTokenObtainPairView
)
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    # path('', Home.as_view()),
    path('',RegisterHostelView.as_view(),name='hostel-registration'),
    path('api/token/hostel', HostelEmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/student', StudentEmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('check',Home.as_view(),name='check'),
    path('login',HostelLoginView.as_view(),name='login'),
    path('logout',HostelLogoutView.as_view(),name='logout'),
    path('register-student', RegisterStudentWithHostelView.as_view(), name='register_student'),
    path('student-login',StudentLoginView.as_view(),name='student-login'),   
    path('leaves',ViewLeaves.as_view(),name='view leaves'),
]