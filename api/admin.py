from django.contrib import admin

# Register your models here.
from api.models import Departament, PositionDepartament, Employee
admin.site.register(Departament)
admin.site.register(PositionDepartament)
admin.site.register(Employee)
