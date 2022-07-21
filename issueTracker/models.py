from django.db import models
from django.contrib.auth.models import AbstractUser

from base import settings


class Users(AbstractUser):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(max_length=254)
    username = models.CharField(max_length=60, unique=True)
    password = models.CharField(max_length=60)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class Projects(models.Model):
    PROJECTS_CHOICES = [('Back-end', 'Back-end'), ('Front-end', 'Front-end'),
                        ('iOS', 'iOS'), ('Android', 'Android')]
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=128, choices=PROJECTS_CHOICES)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='author_user_id', on_delete=models.CASCADE, related_name='project')

    def __str__(self):
        return f"{self.title}"


class Contributors(models.Model):
    AUTHOR = 'Author'
    CONTRIBUTOR = 'Contributor'
    CHOICES = [(AUTHOR, 'Auteur'), (CONTRIBUTOR, 'Contributeur')]

    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE, null=True, related_name='contributor_project')
    role = models.CharField(max_length=30, choices=CHOICES, verbose_name='role')


class Issues(models.Model):
    PRIORITY_CHOICES = [('Urgent', 'Urgent'), ('Normal', 'Normal'), ('Cool', 'Cool')]
    STATUS_CHOICES = [('A faire', 'A faire'), ('En cours', 'En cours'), ('Terminé', 'Terminé')]
    TAG_CHOICES = [('Bug', 'Bug'), ('Tache', 'Tache'), ('Amélioration', 'Amélioration')]

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=500)
    tag = models.CharField(max_length=60, choices=TAG_CHOICES)
    priority = models.CharField(max_length=60, choices=PRIORITY_CHOICES)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    status = models.CharField(max_length=60, choices=STATUS_CHOICES)
    created_time = models.DateTimeField(auto_now_add=True)
    # author_user_id = models.ForeignKey(Contributors, on_delete=models.CASCADE)  # Peut-etre pas mettre Cascade
    assignee_user_id = models.ForeignKey(Users, on_delete=models.CASCADE)   # Peut-etre pas mettre Cascade


class Comments(models.Model):
    description = models.CharField(max_length=500)
    created_time = models.DateTimeField(auto_now_add=True)
    author_user_id = models.ForeignKey(Users, on_delete=models.CASCADE)  # Peut-etre pas mettre Cascade
    issue_id = models.ForeignKey(Issues, on_delete=models.CASCADE)  # Peut-etre pas mettre Cascade)
