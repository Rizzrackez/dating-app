from django.urls import path
from backend.views import MemberCreateView

urlpatterns = [
    path('clients/create', MemberCreateView.as_view()),
]
