# Generated by Django 5.1.5 on 2025-02-17 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0009_student_billing_method_student_monthly_fee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='discount',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
