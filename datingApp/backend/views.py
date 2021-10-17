from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from backend.models import Member
from backend.serializers import MemberCreateSerializer


class MemberCreateView(CreateAPIView):
    model = Member
    serializer_class = MemberCreateSerializer
