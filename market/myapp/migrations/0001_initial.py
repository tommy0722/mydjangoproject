# Generated by Django 3.2.4 on 2023-02-01 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(max_length=30)),
                ('pprice', models.IntegerField()),
                ('pimage', models.CharField(max_length=40)),
                ('pdescription', models.TextField()),
            ],
        ),
    ]
