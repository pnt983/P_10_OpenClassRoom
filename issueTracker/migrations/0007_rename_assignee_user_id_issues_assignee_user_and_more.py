# Generated by Django 4.0.6 on 2022-07-27 11:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issueTracker', '0006_rename_author_user_id_projects_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issues',
            old_name='assignee_user_id',
            new_name='assignee_user',
        ),
        migrations.RenameField(
            model_name='issues',
            old_name='project_id',
            new_name='project',
        ),
        migrations.AlterField(
            model_name='projects',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
    ]
