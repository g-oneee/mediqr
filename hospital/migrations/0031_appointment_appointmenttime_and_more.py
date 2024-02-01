# Generated by Django 4.0.3 on 2024-01-28 08:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0030_patient_work_department_alter_doctor_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='appointmentTime',
            field=models.TimeField(default=datetime.time(8, 28, 15, 176504)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='appointmentDate',
            field=models.DateField(default=datetime.datetime.today),
        ),
    ]
