# Generated by Django 5.1.7 on 2025-03-08 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('urn', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(blank=True, max_length=100)),
                ('open_date', models.DateField(blank=True, null=True)),
                ('close_date', models.DateField(null=True)),
                ('city', models.CharField(max_length=100, null=True)),
                ('postcode', models.CharField(max_length=20, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('phone_number', models.CharField(max_length=30, null=True)),
            ],
        ),
    ]
