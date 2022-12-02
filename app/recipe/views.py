from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from core import models
from recipe import serializers


class TagViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        '''return tag objects for current authuser'''
        return self.queryset\
            .filter(user_id=self.request.user.id)\
            .order_by('-name')

    def perform_create(self, serializer):
        '''modify data object before create'''
        serializer.save(user=self.request.user)
