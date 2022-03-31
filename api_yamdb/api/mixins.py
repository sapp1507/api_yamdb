from rest_framework import mixins, viewsets


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    """ViewSet для вывода списка, создания и удаления объекта модели"""

    pass
