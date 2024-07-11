from django.urls import path
from .views import RegisterComplaintView,TakeLeaveView,ViewComplaints,CreateNoticeView,NoticeView

urlpatterns = [
    path('complaint',RegisterComplaintView.as_view(),name='complaint'),
    path('leave',TakeLeaveView.as_view(),name='leave'),
    path('all-complaint',ViewComplaints.as_view(),name='all-complaint'),
    path('all-notice',NoticeView.as_view(),name='all-notice'),
    path('notice',CreateNoticeView.as_view(),name='notice'),
]
