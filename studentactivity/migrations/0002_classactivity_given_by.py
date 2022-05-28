# Generated by Django 3.2.9 on 2021-12-14 03:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('studentactivity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='classactivity',
            name='given_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lecturer_name', to=settings.AUTH_USER_MODEL),
        ),
    ]
