# Generated by Django 4.0.6 on 2022-07-21 07:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issueTracker', '0003_alter_users_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='author_user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project', to=settings.AUTH_USER_MODEL, verbose_name='author_user_id'),
        ),
        migrations.AlterField(
            model_name='users',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
