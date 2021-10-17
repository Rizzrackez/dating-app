from django.urls import path
from backend.views import MemberCreateView, RatingAnotherMember, ListMembers

urlpatterns = [
    path('clients/create', MemberCreateView.as_view()),
    path('clients/<int:pk>/match', RatingAnotherMember.as_view()),
    path('list/', ListMembers.as_view())
]
