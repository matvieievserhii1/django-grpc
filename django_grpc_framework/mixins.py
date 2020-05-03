from google.protobuf import empty_pb2

from django_grpc_framework.protobuf.json_format import (
    message_to_dict, parse_dict
)


class CreateModelMixin:
    """
    Create a model instance.
    """
    def Create(self, request, context):
        data = message_to_dict(request)
        serializer = self.get_serializer(request, context, data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        protobuf_class = self.get_protobuf_class(request, context)
        return parse_dict(serializer.data, protobuf_class())

    def perform_create(self, serializer):
        serializer.save()


class ListModelMixin:
    """
    List a queryset.
    """
    def List(self, request, context):
        queryset = self.filter_queryset(
            request, context, self.get_queryset(request, context)
        )
        serializer = self.get_serializer(request, context, queryset, many=True)
        protobuf_class = self.get_protobuf_class(request, context)
        for data in serializer.data:
            yield parse_dict(data, protobuf_class())


class RetrieveModelMixin:
    """
    Retrieve a model instance.
    """
    def Retrieve(self, request, context):
        instance = self.get_object(request, context)
        serializer = self.get_serializer(request, context, instance)
        protobuf_class = self.get_protobuf_class(request, context)
        return parse_dict(serializer.data, protobuf_class())


class UpdateModelMixin:
    """
    Update a model instance.
    """
    def Update(self, request, context):
        instance = self.get_object(request, context)
        data = message_to_dict(request)
        serializer = self.get_serializer(request, context, instance, data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        protobuf_class = self.get_protobuf_class(request, context)
        return parse_dict(serializer.data, protobuf_class())

    def perform_update(self, serializer):
        serializer.save()


class DestroyModelMixin:
    """
    Destroy a model instance.
    """
    def Destroy(self, request, context):
        instance = self.get_object(request, context)
        self.perform_destroy(instance)
        return empty_pb2.Empty()

    def perform_destroy(self, instance):
        instance.delete()
