# Generated by Django 5.1.5 on 2025-02-03 15:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0002_alter_expense_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='installment_count',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.CreateModel(
            name='Installment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installment_number', models.PositiveIntegerField()),
                ('installment_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('due_date', models.DateField()),
                ('expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prestações', to='expense.expense')),
            ],
        ),
    ]
