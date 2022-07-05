from django.db import models


class Users(models.Model):
    user_id = models.IntegerField()
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=128)


class Contributors(models.Model):
    user_id = models.IntegerField()
    project_id = models.IntegerField()
    permission = models.ChoiceField()
    role = models.CharField(max_length=128)


class Projects(models.Model):
    project_id = models.IntegerField()
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=256)
    author_user_id = models.ForeignKey(Users, on_delete=models.CASCADE)


class Issues(models.Model):
    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=500)
    tag = models.CharField(max_length=128)
    priority = models.CharField(max_length=128)
    project_id = models.IntegerField()
    status = models.CharField(max_length=128)
    created_time = models.DateTimeField(auto_now_add=True)
    author_user_id = models.ForeignKey(Contributors, on_delete=models.CASCADE)  # Peut-etre pas mettre Cascade
    assignee_user_id = models.ForeignKey(Users, on_delete=models.CASCADE)   # Peut-etre pas mettre Cascade


class Comments(models.Model):
    comment_id = models.IntegerField()
    description = models.CharField(max_length=500)
    created_time = models.DateTimeField(auto_now_add=True)
    author_user_id = models.ForeignKey(Contributors, on_delete=models.CASCADE)  # Peut-etre pas mettre Cascade
    issue_id = models.ForeignKey(Issues, on_delete=models.CASCADE)  # Peut-etre pas mettre Cascade

