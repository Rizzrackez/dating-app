from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail

from backend.models import Member
from backend.serializers import MemberCreateSerializer
from backend.backend_service import calculating_distance_between_points



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


class ListMembers(ListAPIView):
    serializer_class = MemberCreateSerializer
    # queryset = Member.objects.all()
    # filterset_fields = ['gender', 'name', 'surname']

    def get_queryset(self):
        if self.request.method == 'GET':
            queryset = Member.objects.all()
            if self.request.GET.get('gender', None) is not None:
                gender = self.request.GET.get('gender', None)
                queryset = queryset.filter(gender=gender)
            if self.request.GET.get('name', None) is not None:
                name = self.request.GET.get('name', None)
                queryset = queryset.filter(name=name)
            if self.request.GET.get('surname', None) is not None:
                surname = self.request.GET.get('surname', None)
                queryset = queryset.filter(surname=surname)

            if self.request.GET.get('length', None) is not None:
                length = self.request.GET.get('length', None)
                if self.request.GET.get('width', None) is not None:
                    width = self.request.GET.get('width', None)
                    if self.request.GET.get('distance', None) is not None:
                        distance = self.request.GET.get('distance', None)
                        member_in_distance_list = []
                        try:
                            for member in queryset:
                                distance_between_points = calculating_distance_between_points(int(length), int(member.length), int(width), int(member.width))
                                if distance_between_points < float(distance):
                                    member_in_distance_list.append(member)
                            queryset = member_in_distance_list
                        except ValueError:
                            print("В url передана строка вместо чисел")
            return queryset
