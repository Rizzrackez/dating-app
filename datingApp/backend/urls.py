from django.urls import path
from backend.views import MemberCreateView, RatingAnotherMember

urlpatterns = [
    path('clients/create', MemberCreateView.as_view()),
    path('clients/<int:pk>/match', RatingAnotherMember.as_view()),
]
