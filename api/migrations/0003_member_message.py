# Generated migration

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_update_models'),
    ]

    operations = [
        # This migration is intentionally empty as Member, Message and MemberToken
        # models are already created in 0001_initial.py and modified in 0002_update_models.py
        # This file exists to maintain migration history consistency
    ]
