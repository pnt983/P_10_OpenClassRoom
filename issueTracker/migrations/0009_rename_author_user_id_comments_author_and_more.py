# Generated by Django 4.0.6 on 2022-07-27 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issueTracker', '0008_rename_project_id_contributors_project_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comments',
            old_name='author_user_id',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='comments',
            old_name='issue_id',
            new_name='issue',
        ),
    ]
