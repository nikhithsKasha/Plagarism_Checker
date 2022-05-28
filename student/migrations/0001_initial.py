# Generated by Django 3.2.9 on 2021-12-08 06:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import student.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('studentactivity', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to=student.models.user_directory_path)),
                ('description', models.TextField(blank=True, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('activity', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='studentactivity.classactivity')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]