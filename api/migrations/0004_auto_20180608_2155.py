# Generated by Django 2.0 on 2018-06-08 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20180608_2044'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='workflow_type',
            field=models.IntegerField(choices=[(0, 'Не выбрано'), (1, 'Принят на работу'), (2, 'Увольнен')], db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='employee',
            name='sex',
            field=models.IntegerField(choices=[(0, 'Не выбрано'), (1, 'Мужской'), (2, 'Женский')], db_index=True, default=0),
        ),
    ]
