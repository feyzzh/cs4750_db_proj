# Generated by Django 5.2 on 2025-04-06 01:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('food_id', models.AutoField(primary_key=True, serialize=False)),
                ('food_item', models.TextField()),
                ('food_category', models.TextField()),
                ('per_100_units', models.TextField()),
                ('calories_per_100', models.IntegerField()),
                ('kj_per_100', models.IntegerField()),
            ],
            options={
                'db_table': 'foods',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='NutritionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_of_consumption', models.DateTimeField()),
                ('num_grams_consumed', models.PositiveIntegerField()),
                ('source', models.TextField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('food', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hooswellapp.food')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hooswellapp.user')),
            ],
        ),
    ]
