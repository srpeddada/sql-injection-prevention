# Generated by Django 4.1.1 on 2022-11-23 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_empsin_eid'),
    ]

    operations = [
        migrations.CreateModel(
            name='adminlogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=500)),
                ('password', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=500)),
                ('password', models.CharField(max_length=500)),
            ],
        ),
    ]
