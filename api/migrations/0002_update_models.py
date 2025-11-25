# Generated migration

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='member',
            options={'ordering': ['-created_at']},
        ),
        migrations.RenameField(
            model_name='message',
            old_name='author',
            new_name='member',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='created_at',
            new_name='timestamp',
        ),
        migrations.AlterField(
            model_name='member',
            name='password',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='member',
            name='username',
            field=models.CharField(db_index=True, max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['timestamp']},
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['timestamp'], name='messages_timesta_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['member', 'timestamp'], name='messages_member_timesta_idx'),
        ),
    ]
