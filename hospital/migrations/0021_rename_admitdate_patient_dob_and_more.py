# Generated by Django 4.0.3 on 2023-12-29 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0020_rename_department_doctor_blood_group_choices'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patient',
            old_name='admitDate',
            new_name='dob',
        ),
        migrations.RenameField(
            model_name='patient',
            old_name='symptoms',
            new_name='history',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='blood_group_choices',
        ),
        migrations.AddField(
            model_name='doctor',
            name='department',
            field=models.CharField(choices=[('Cardiologist', 'Cardiologist'), ('Dermatologists', 'Dermatologists'), ('Emergency Medicine Specialists', 'Emergency Medicine Specialists'), ('Allergists/Immunologists', 'Allergists/Immunologists'), ('Anesthesiologists', 'Anesthesiologists'), ('Colon and Rectal Surgeons', 'Colon and Rectal Surgeons')], default='Cardiologist', max_length=50),
        ),
        migrations.AddField(
            model_name='patient',
            name='Blood_group_choices',
            field=models.CharField(choices=[('O+', 'O positive'), ('O-', 'O negative'), ('A+', 'A positive'), ('A-', 'A negative'), ('B+', 'B positive'), ('B-', 'B negative'), ('AB+', 'AB positive'), ('AB-', 'AB negative')], default='O+', max_length=50),
        ),
        migrations.AddField(
            model_name='patient',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=50),
        ),
        migrations.AddField(
            model_name='patient',
            name='height',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='mobile2',
            field=models.CharField(default=99999999, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='patient_id',
            field=models.CharField(default=11, max_length=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='weight',
            field=models.CharField(max_length=3, null=True),
        ),
    ]
