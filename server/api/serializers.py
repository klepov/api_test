from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Employee, Departament, PositionDepartament
from common.common_exceptions import AlreadyExist


class DepartamentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Departament
        fields = '__all__'


class PositionDepartamentSerializers(serializers.ModelSerializer):
    class Meta:
        model = PositionDepartament
        fields = '__all__'

    departament = DepartamentSerializers()


class EmployeeCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = ('user',)

    password = serializers.CharField(required=True)
    username = serializers.CharField(required=True)

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')

        if username and password:
            if User.objects.filter(username=username).exists():
                raise AlreadyExist()

        user = User.objects.create_user(username=username, password=password)
        validated_data['user'] = user
        return Employee.objects.create(**validated_data)

    def to_representation(self, instance):
        return EmployeeReadSerializers(instance).data


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
