from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView

from backend.models import Member
from backend.serializers import MemberCreateSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail


class MemberCreateView(CreateAPIView):
    model = Member
    serializer_class = MemberCreateSerializer


class RatingAnotherMember(APIView):
    serializer_class = MemberCreateSerializer

    def get(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated:
            user = Member.objects.get(email=request.user)
            liked_user = get_object_or_404(Member, pk=pk)
            if user.id != liked_user.id:
                user.liked_members.add(liked_user)
                user.save()

                # логика отправки сообщения, в случае симпатии с обеих сторон
                liked_members_id = [member.id for member in liked_user.liked_members.all()]
                if user.id in liked_members_id:
                    #  если прописать данные в settings к SMTP, то можно убрать исключение
                    try:
                        send_mail(
                            'Вы кому-то понравились',
                            f'Вы понравились {user.name}! Почта участника: {user.email}',
                            'maksim6info@gmail.com',
                            [liked_user.email],
                            fail_silently=False,
                        )
                        send_mail(
                            'Вы кому-то понравились',
                            f'Вы понравились {liked_user.name}! Почта участника: {liked_user.email}',
                            'maksim6info@gmail.com',
                            [user.email],
                            fail_silently=False,
                        )
                    except Exception as e:
                        pass
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
