from django.urls import path
from .views import RegisterComplaintView,TakeLeaveView,ViewComplaints

urlpatterns = [
    path('complaint',RegisterComplaintView.as_view(),name='complaint'),
    path('leave',TakeLeaveView.as_view(),name='leave'),
    path('all-complaint',ViewComplaints.as_view(),name='all-complaint'),
]
