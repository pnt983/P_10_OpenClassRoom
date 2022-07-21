# Generated by Django 4.0.6 on 2022-07-20 12:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issueTracker', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issues',
            old_name='desc',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='comment_id',
        ),
        migrations.RemoveField(
            model_name='issues',
            name='author_user_id',
        ),
        migrations.RemoveField(
            model_name='projects',
            name='project_id',
        ),
        migrations.RemoveField(
            model_name='users',
            name='user_id',
        ),
        migrations.AlterField(
            model_name='comments',
            name='author_user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='contributors',
            name='project_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contributor_project', to='issueTracker.projects'),
        ),
        migrations.AlterField(
            model_name='contributors',
            name='role',
            field=models.CharField(choices=[('Author', 'Auteur'), ('Contributor', 'Contributeur')], max_length=30, verbose_name='role'),
        ),
        migrations.AlterField(
            model_name='contributors',
            name='user_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='issues',
            name='priority',
            field=models.CharField(choices=[('Urgent', 'Urgent'), ('Normal', 'Normal'), ('Cool', 'Cool')], max_length=60),
        ),
        migrations.AlterField(
            model_name='issues',
            name='project_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='issueTracker.projects'),
        ),
        migrations.AlterField(
            model_name='issues',
            name='status',
            field=models.CharField(choices=[('A faire', 'A faire'), ('En cours', 'En cours'), ('Terminé', 'Terminé')], max_length=60),
        ),
        migrations.AlterField(
            model_name='issues',
            name='tag',
            field=models.CharField(choices=[('Bug', 'Bug'), ('Tache', 'Tache'), ('Amélioration', 'Amélioration')], max_length=60),
        ),
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(max_length=60),
        ),
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(max_length=60, unique=True),
        ),
    ]
