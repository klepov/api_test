from rest_framework import serializers

from api.models import Employee, Departament, PositionDepartament


class DepartamentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Departament
        fields = '__all__'


class PositionDepartamentSerializers(serializers.ModelSerializer):
    class Meta:
        model = PositionDepartament
        fields = '__all__'

    departament = DepartamentSerializers()


class EmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

    def to_representation(self, instance):
        return EmployeeReadSerializers(instance).data


class EmployeeReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ('user',)

    position_departament = PositionDepartamentSerializers(required=False)
