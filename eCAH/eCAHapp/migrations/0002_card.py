# Generated by Django 3.1.4 on 2021-01-18 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eCAHapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('is_black', models.BooleanField()),
            ],
        ),
    ]
