# Generated by Django 3.1.2 on 2020-11-06 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PeopleFetch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=255, unique=True)),
                ('fetching_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
