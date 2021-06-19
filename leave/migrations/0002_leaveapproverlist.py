# Generated by Django 2.1.7 on 2021-04-05 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0006_auto_20210405_1010'),
        ('leave', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeaveApproverList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approver_position', models.IntegerField()),
                ('approver_status', models.CharField(blank=True, choices=[('Approved', 'Approved'), ('Pending', 'Pending'), ('Rejected', 'Rejected')], max_length=12, null=True)),
                ('approver_remark', models.TextField(blank=True, null=True)),
                ('approver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Employee.Employee')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leave.LeaveRequest')),
            ],
        ),
    ]