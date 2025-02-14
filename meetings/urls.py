from django.urls import path
from .views import process_meeting, add_meeting, get_meeting_details, list_meetings

urlpatterns = [
    path("process_meeting/", process_meeting, name="process_meeting"),
    path("add_meeting/", add_meeting, name="add_meeting"),
    path("get_meeting_details/<int:meeting_id>/", get_meeting_details, name="get_meeting_details"),
    path("list_meetings/", list_meetings, name="list_meetings"),
]
