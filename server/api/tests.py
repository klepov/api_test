from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

# Create your tests here.
from django.utils.crypto import get_random_string
from rest_framework import status
from rest_framework.test import APIClient

from api.models import Employee, PositionDepartament, Departament


class TestEmployeeModel(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_employee(self):
        response = self.client.post('/employee/create/',
                                    data={
                                        "name": "ivan",
                                        "sex": 1,
                                        "phone_number": "+79030008888",
                                        "bdate": "1990-01-01",
                                        "username": 'ivan',
                                        "password": 'test'
                                    },
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = response.json()
        response.pop('id')
        self.assertEqual(response,
                         {'bdate': '1990-01-01',
                          'phone_number': '+79030008888',
                          'name': 'ivan',
                          'position_departament': None,
                          'sex': 1,
                          'workflow_type': 0
                          }
                         )

    def test_create_employee_double_fail(self):
        self.test_create_employee()
        response = self.client.post('/employee/create/',
                                    data={
                                        "name": "ivan",
                                        "sex": 1,
                                        "phone_number": "+79030008888",
                                        "bdate": "1990-01-01",
                                        "username": 'ivan',
                                        "password": 'test'
                                    },
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_change_employee(self):
        self._create_emp()
        emp = Employee.objects.first()
        self.client.force_authenticate(emp.user)
        response = self.client.patch('/employee/%s/' % emp.id,
                                     data={
                                         "name": "petr",
                                         "sex": 2,
                                     },
                                     format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('name'), Employee.objects.first().name)
        self.assertEqual(response.json().get('sex'), Employee.objects.first().sex)

    def test_hr_change_employee(self):
        hr = self._custom_perm()
        self._create_emp()

        self.client.force_authenticate(hr.user)

        response = self.client.patch('/employee/%s/' % Employee.objects.get(name='ivan').id,
                                     data={
                                         "name": "petr",
                                         "sex": 2,
                                     },
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('name'), Employee.objects.exclude(name='hr').first().name)
        self.assertEqual(response.json().get('sex'), Employee.objects.exclude(name='hr').first().sex)

    def test_other_change_employee(self):
        first = self._create_emp()

        self.client.force_authenticate(first.user)

        response = self.client.patch('/employee/%s/' % self._create_emp().id,
                                     data={
                                         "name": "petr",
                                         "sex": 2,
                                     },
                                     format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_workflow_self(self):
        emp = self._create_emp()
        self.client.force_authenticate(emp.user)
        response = self.client.patch('/employee/%s/' % emp.id,
                                     data={
                                         "workflow_type": "1",
                                     },
                                     format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_workflow_HR(self):
        emp = self._create_emp()
        hr = self._custom_perm()
        self.client.force_authenticate(hr.user)
        response = self.client.patch('/employee/%s/' % emp.id,
                                     data={
                                         "workflow_type": "1",
                                     },
                                     format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('workflow_type'), 1)

    def test_migrate_hr(self):
        emp = self._create_emp()
        pos = PositionDepartament.objects.create(title="стажер",
                                                 departament=Departament.objects.create(
                                                     title="разработка"))

        emp.position_departament = pos
        emp.save()

        hr = self._custom_perm()
        self.client.force_authenticate(hr.user)

        response = self.client.patch('/employee/%s/' % emp.id,
                                     data={
                                         "position_departament":
                                             PositionDepartament.objects.create(title="синьор",
                                                                                departament=Departament.objects.create(
                                                                                    title="помидор")).id,
                                     },
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('position_departament').get('title'), 'синьор')
        self.assertEqual(response.json().get('position_departament').get('departament').get('title'), 'помидор')

    def test_migrate_self(self):
        emp = self._create_emp()
        pos = PositionDepartament.objects.create(title="стажер",
                                                 departament=Departament.objects.create(
                                                     title="разработка"))

        emp.position_departament = pos
        emp.save()

        self.client.force_authenticate(emp.user)

        response = self.client.patch('/employee/%s/' % emp.id,
                                     data={
                                         "position_departament":
                                             PositionDepartament.objects.create(title="синьор",
                                                                                departament=Departament.objects.create(
                                                                                    title="помидор")).id,
                                     },
                                     format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_employee(self):
        emp = self._create_emp()
        response = self.client.get('/employee/%s/' % emp.id)
        self.assertEqual(response.status_code, 200)
        response = response.json()
        response.pop('id')
        self.assertEqual(response, {
            'sex': 1,
            'bdate': '1990-01-01',
            'name': 'ivan',
            'phone_number': '+79030008888',
            'workflow_type': 0,
            'position_departament': None}
                         )

    def test_get_list(self):
        for _ in range(100):
            self._create_emp(name=get_random_string())
        response = self.client.get('/employee/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 100)

    def test_search_employee(self):
        self.test_get_list()
        emp = self._create_emp('вася')

        emp.position_departament = PositionDepartament.objects.create(title="стажер",
                                                                      departament=Departament.objects.create(
                                                                          title="разработка"))
        emp.save()
        response = self.client.get('/employee/?name=вася&departament=разработка&position=стажер')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0].get('name'), 'вася')

    @staticmethod
    def _create_emp(name='ivan'):
        return Employee.objects.create(user=User.objects.create(username=get_random_string(),
                                                                password=get_random_string()),
                                       name=name,
                                       sex=1,
                                       phone_number="+79030008888",
                                       bdate="1990-01-01")

    @staticmethod
    def _custom_perm():
        content_type = ContentType.objects.get(app_label='api', model='employee')
        group = Group.objects.create(name='hr')
        permission = Permission.objects.create(codename='can_edit',
                                               name='Can edit employee',
                                               content_type=content_type)
        user = User.objects.create(username='HR', password="test")

        group.permissions.add(permission)
        user.groups.add(group)
        emp = Employee.objects.create(user=user, name='hr', sex=1, phone_number="+79030008888", bdate="1990-01-01")

        return emp
