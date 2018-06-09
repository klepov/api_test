from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from phonenumber_field.modelfields import PhoneNumberField


class Departament(models.Model):
    title = models.CharField(max_length=255, null=True, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'


class PositionDepartament(models.Model):
    title = models.CharField(max_length=255, null=True, db_index=True)
    departament = models.ForeignKey(Departament, on_delete=models.CASCADE)

    def __str__(self):
        return "депортамент %s позиция %s" % (self.departament, self.title)

    class Meta:
        verbose_name = 'Позиция в департаменте'
        verbose_name_plural = 'Позиции в департаменте'


'Работа с сотрудниками – приём на работу, увольнение, перевод в другой отдел, повышение в должности, etc.'


class Employee(models.Model):
    SEX = (
        (0, 'Не выбрано'),
        (1, 'Мужской'),
        (2, 'Женский'),
    )

    WORKFLOW = (
        (0, 'Не выбрано'),
        (1, 'Принят на работу'),
        (2, 'Увольнен'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, db_index=True)
    sex = models.IntegerField(choices=SEX, default=0, db_index=True)
    bdate = models.DateField(blank=True, null=True, db_index=True)
    phone_number = PhoneNumberField()
    position_departament = models.ForeignKey(PositionDepartament, null=True, on_delete=models.SET_NULL)
    workflow_type = models.IntegerField(choices=WORKFLOW, default=0, db_index=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return "%s, %s" % (self.name, self.position_departament)
