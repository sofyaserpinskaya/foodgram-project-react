from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from djoser import views, utils
from djoser.conf import settings

from .serializers import (
    UserSerializer, UserDetailSerializer,
    SetPasswordSerializer, SubscriptionSerializer
)
from .models import User, Subscription
from api.pagination import PageLimitPagination


SUBSCRIPTION_ERROR = 'Вы уже подписаны на этого пользователя.'
UNSUBSCRIPTION_ERROR = 'Вы не были подписаны на этого пользователя.'
SELF_SUBSCRIPTION_ERROR = 'Нельзя подписаться на самого себя.'


class TokenCreateView(views.TokenCreateView):
    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        return Response(
            data=token_serializer_class(token).data,
            status=status.HTTP_201_CREATED
        )


class UserViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = User.objects.all()
    pagination_class = PageLimitPagination
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['POST'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def set_password(self, request):
        serializer = SetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.check_password(request.data.get('current_password')):
            request.user.set_password(request.data.get('new_password'))
            request.user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        queryset = Subscription.objects.filter(
            user=request.user
        ).select_related('author')
        serializer = SubscriptionSerializer(
            self.paginate_queryset(queryset),
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, pk):
        author = get_object_or_404(User, id=pk)
        if request.method == 'POST':
            if request.user == author:
                return Response(
                    {'errors': SELF_SUBSCRIPTION_ERROR},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                subscription = Subscription.objects.create(
                    user=request.user, author=author
                )
                serializer = SubscriptionSerializer(subscription)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            except IntegrityError:
                return Response(
                    {'errors': SUBSCRIPTION_ERROR},
                    status=status.HTTP_400_BAD_REQUEST
                )
        subscription = Subscription.objects.filter(
                user=request.user, author=author
            )
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': UNSUBSCRIPTION_ERROR},
            status=status.HTTP_400_BAD_REQUEST
        )
