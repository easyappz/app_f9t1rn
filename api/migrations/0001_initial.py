# Generated migration

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'members',
            },
        ),
        migrations.CreateModel(
            name='MemberToken',
            fields=[
                ('key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('member', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='auth_token', to='api.member')),
            ],
            options={
                'db_table': 'member_tokens',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='api.member')),
            ],
            options={
                'db_table': 'messages',
                'ordering': ['created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='member',
            index=models.Index(fields=['username'], name='members_username_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['created_at'], name='messages_created_at_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['author'], name='messages_author_idx'),
        ),
        migrations.AddIndex(
            model_name='membertoken',
            index=models.Index(fields=['key'], name='member_tokens_key_idx'),
        ),
    ]
