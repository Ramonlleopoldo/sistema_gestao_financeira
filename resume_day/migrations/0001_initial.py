# Generated by Django 5.1.5 on 2025-02-09 15:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('training', '0002_alter_trainingclass_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingDismissal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('reason', models.TextField(blank=True, null=True)),
                ('training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.trainingclass')),
            ],
        ),
    ]
