from rest_framework import permissions
from rest_framework.generics import UpdateAPIView, RetrieveAPIView, CreateAPIView, ListAPIView

from api.models import Employee, Departament
from api.serializers import EmployeeSerializers
from common.common_exceptions import OnlyHr

from api.serializers import EmployeeCreateSerializers


class IsOwnerOrHROnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.groups.filter(name='hr').exists() or obj.user == request.user:
            return True
        return False


class IsHROnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='hr').exists():
            return True
        return False


class EmployeeWorkflow(UpdateAPIView):
    serializer_class = EmployeeSerializers
    queryset = Employee.objects.all()

    permission_classes = (IsHROnly,)


class EmployeeCreateApi(CreateAPIView):
    serializer_class = EmployeeCreateSerializers
    queryset = Employee.objects.all()

    permission_classes = ()


class EmployeeApi(RetrieveAPIView, UpdateAPIView):

    def perform_update(self, serializer):
        if serializer.validated_data.get('workflow_type') or serializer.validated_data.get('position_departament'):
                if self.request.user.groups.filter(name='hr').exists() is False:
                    raise OnlyHr()
        super().perform_update(serializer)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    serializer_class = EmployeeSerializers
    queryset = Employee.objects.all()

    permission_classes = (IsOwnerOrHROnly,)


class EmployeeListApi(ListAPIView):
    serializer_class = EmployeeSerializers

    def get_queryset(self):

        queryset = Employee.objects.all()
        name = self.request.query_params.get('name', None)
        departament = self.request.query_params.get('departament', None)
        position = self.request.query_params.get('position', None)
        number = self.request.query_params.get('number', None)
        if name is not None:
            queryset = queryset.filter(name__contains=name)
        if departament is not None:
            queryset = queryset.filter(position_departament__departament__title=departament)
        if position is not None:
            queryset = queryset.filter(position_departament__title=position)
        if number is not None:
            queryset = queryset.filter(phone_number=number)

        return queryset
